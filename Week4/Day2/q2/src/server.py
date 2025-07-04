"""
Smart Meeting Assistant MCP Server
AI-powered meeting scheduling and management system
"""

import json
import os
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any
import pytz
from dateutil import parser
import google.generativeai as genai
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

mcp = FastMCP("Smart Meeting Assistant")

class SmartMeetingAssistant:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_content.json')
        self.load_data()
        self.setup_gemini()
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"users": [], "meetings": []}
    
    def save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def setup_gemini(self):
        """Setup Gemini AI client"""
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.gemini_model = None
            print("Warning: GEMINI_API_KEY not found. AI features will be limited.")
    
    def ask_gemini(self, prompt: str) -> str:
        """Ask Gemini AI for response"""
        if not self.gemini_model:
            return "AI service unavailable"
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI service error: {str(e)}"
    
    def create_meeting(self, title: str, participants: List[str], duration: int, 
                      start_time: str, timezone: str = "UTC") -> Dict[str, Any]:
        """Schedule new meeting with conflict detection"""
        try:
            # Validate participants
            valid_users = [user['id'] for user in self.data['users']]
            invalid_participants = [p for p in participants if p not in valid_users]
            
            if invalid_participants:
                return {
                    "success": False,
                    "error": f"Invalid participants: {invalid_participants}",
                    "data": None
                }
            
            # Parse start time
            start_dt = parser.parse(start_time)
            end_dt = start_dt + timedelta(minutes=duration)
            
            # Check for conflicts
            conflicts = self.detect_scheduling_conflicts_internal(participants, start_dt, end_dt)
            
            if conflicts:
                return {
                    "success": False,
                    "error": "Scheduling conflicts detected",
                    "data": {"conflicts": conflicts}
                }
            
            # Create meeting
            meeting_id = f"meeting_{len(self.data['meetings']) + 1}"
            meeting = {
                "id": meeting_id,
                "title": title,
                "organizer": participants[0],
                "participants": participants,
                "start_time": start_dt.isoformat(),
                "end_time": end_dt.isoformat(),
                "timezone": timezone,
                "status": "scheduled"
            }
            
            self.data['meetings'].append(meeting)
            self.save_data()
            
            return {
                "success": True,
                "message": f"Meeting '{title}' scheduled successfully",
                "data": meeting
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create meeting: {str(e)}",
                "data": None
            }
    
    def find_optimal_slots(self, participants: List[str], duration: int, 
                          date_range: str) -> Dict[str, Any]:
        """AI-powered time slot recommendations"""
        try:
            participant_data = [user for user in self.data['users'] if user['id'] in participants]
            
            if not participant_data:
                return {
                    "success": False,
                    "error": "No valid participants found",
                    "data": None
                }
            
            # Generate suggestions for next 7 days
            start_date = parser.parse(date_range).date()
            suggestions = []
            
            for day_offset in range(7):
                current_date = start_date + timedelta(days=day_offset)
                
                # Check working hours (9 AM to 5 PM)
                for hour in range(9, 17):
                    slot_start = datetime.combine(current_date, time(hour, 0))
                    slot_end = slot_start + timedelta(minutes=duration)
                    
                    # Check if slot is free
                    if not self.detect_scheduling_conflicts_internal(participants, slot_start, slot_end):
                        suggestions.append({
                            "start_time": slot_start.isoformat(),
                            "end_time": slot_end.isoformat(),
                            "score": self.calculate_slot_score(slot_start, len(participants))
                        })
            
            # Sort by score and return top 5
            suggestions.sort(key=lambda x: x['score'], reverse=True)
            
            return {
                "success": True,
                "message": f"Found {len(suggestions[:5])} optimal time slots",
                "data": {"suggestions": suggestions[:5]}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to find optimal slots: {str(e)}",
                "data": None
            }
    
    def detect_scheduling_conflicts(self, user_id: str, start_time: str, 
                                  end_time: str) -> Dict[str, Any]:
        """Detect scheduling conflicts for a user"""
        try:
            start_dt = parser.parse(start_time)
            end_dt = parser.parse(end_time)
            
            conflicts = self.detect_scheduling_conflicts_internal([user_id], start_dt, end_dt)
            
            return {
                "success": True,
                "message": f"Found {len(conflicts)} conflicts" if conflicts else "No conflicts found",
                "data": {"conflicts": conflicts, "user_id": user_id}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to detect conflicts: {str(e)}",
                "data": None
            }
    
    def analyze_meeting_patterns(self, user_id: str, period: str = "month") -> Dict[str, Any]:
        """Analyze meeting patterns for a user"""
        try:
            user_meetings = [m for m in self.data['meetings'] if user_id in m['participants']]
            
            if not user_meetings:
                return {
                    "success": False,
                    "error": "No meetings found for user",
                    "data": None
                }
            
            # Basic statistics
            total_meetings = len(user_meetings)
            meeting_types = {}
            total_duration = 0
            
            for meeting in user_meetings:
                meeting_type = meeting.get('type', 'general')
                meeting_types[meeting_type] = meeting_types.get(meeting_type, 0) + 1
                
                start = parser.parse(meeting['start_time'])
                end = parser.parse(meeting['end_time'])
                duration = (end - start).total_seconds() / 60
                total_duration += duration
            
            avg_duration = total_duration / total_meetings if total_meetings > 0 else 0
            
            return {
                "success": True,
                "message": f"Analysis completed for {period} period",
                "data": {
                    "user_id": user_id,
                    "period": period,
                    "total_meetings": total_meetings,
                    "average_duration_minutes": round(avg_duration, 1),
                    "meeting_types": meeting_types
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to analyze patterns: {str(e)}",
                "data": None
            }
    
    def generate_agenda_suggestions(self, meeting_topic: str, participants: List[str], 
                                  duration: int = 60) -> Dict[str, Any]:
        """Generate AI-powered agenda suggestions"""
        try:
            participant_data = [user for user in self.data['users'] if user['id'] in participants]
            
            if self.gemini_model:
                prompt = f"""Generate a meeting agenda for:
                Topic: {meeting_topic}
                Duration: {duration} minutes
                Participants: {len(participants)} people
                
                Return as JSON with agenda items and time allocations."""
                
                ai_response = self.ask_gemini(prompt)
                
                return {
                    "success": True,
                    "message": "AI agenda generated successfully",
                    "data": {
                        "meeting_topic": meeting_topic,
                        "duration_minutes": duration,
                        "ai_agenda": ai_response
                    }
                }
            else:
                # Fallback agenda
                agenda = {
                    "items": [
                        {"item": "Welcome and introductions", "time": 5},
                        {"item": f"Discussion: {meeting_topic}", "time": duration - 15},
                        {"item": "Action items and wrap-up", "time": 10}
                    ]
                }
                
                return {
                    "success": True,
                    "message": "Basic agenda generated",
                    "data": {"agenda": agenda}
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate agenda: {str(e)}",
                "data": None
            }
    
    def calculate_workload_balance(self, team_members: List[str]) -> Dict[str, Any]:
        """Calculate meeting workload balance"""
        try:
            workload_data = {}
            
            for user_id in team_members:
                user_meetings = [m for m in self.data['meetings'] if user_id in m['participants']]
                
                total_time = 0
                for meeting in user_meetings:
                    start = parser.parse(meeting['start_time'])
                    end = parser.parse(meeting['end_time'])
                    duration = (end - start).total_seconds() / 3600
                    total_time += duration
                
                user_data = next((u for u in self.data['users'] if u['id'] == user_id), None)
                
                workload_data[user_id] = {
                    "name": user_data['name'] if user_data else "Unknown",
                    "total_meeting_hours": round(total_time, 2),
                    "total_meetings": len(user_meetings)
                }
            
            return {
                "success": True,
                "message": "Workload analysis completed",
                "data": {"workload": workload_data}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to calculate workload: {str(e)}",
                "data": None
            }
    
    def score_meeting_effectiveness(self, meeting_id: str) -> Dict[str, Any]:
        """Score meeting effectiveness"""
        try:
            meeting = next((m for m in self.data['meetings'] if m['id'] == meeting_id), None)
            
            if not meeting:
                return {
                    "success": False,
                    "error": "Meeting not found",
                    "data": None
                }
            
            # Basic scoring
            score = 75  # Base score
            duration = (parser.parse(meeting['end_time']) - parser.parse(meeting['start_time'])).total_seconds() / 60
            
            if duration > 60:
                score -= 10
            if len(meeting['participants']) > 5:
                score -= 5
            
            return {
                "success": True,
                "message": "Meeting effectiveness scored",
                "data": {
                    "meeting_id": meeting_id,
                    "effectiveness_score": score,
                    "meeting_title": meeting['title']
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to score meeting: {str(e)}",
                "data": None
            }
    
    def optimize_meeting_schedule(self, user_id: str) -> Dict[str, Any]:
        """Optimize meeting schedule for a user"""
        try:
            user_meetings = [m for m in self.data['meetings'] if user_id in m['participants']]
            
            recommendations = []
            
            # Check for overloaded days
            daily_meetings = {}
            for meeting in user_meetings:
                date = parser.parse(meeting['start_time']).date()
                if date not in daily_meetings:
                    daily_meetings[date] = 0
                daily_meetings[date] += 1
            
            for date, count in daily_meetings.items():
                if count > 5:
                    recommendations.append(f"Too many meetings on {date}: {count} meetings")
            
            if not recommendations:
                recommendations.append("Schedule looks well balanced")
            
            return {
                "success": True,
                "message": "Schedule optimization completed",
                "data": {
                    "user_id": user_id,
                    "recommendations": recommendations,
                    "total_meetings": len(user_meetings)
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to optimize schedule: {str(e)}",
                "data": None
            }
    
    # Helper methods
    def detect_scheduling_conflicts_internal(self, participants: List[str], 
                                           start_time: datetime, end_time: datetime) -> List[Dict]:
        """Internal method to detect scheduling conflicts"""
        conflicts = []
        
        for participant in participants:
            participant_meetings = [m for m in self.data['meetings'] 
                                  if participant in m['participants'] and m['status'] == 'scheduled']
            
            for meeting in participant_meetings:
                meeting_start = parser.parse(meeting['start_time'])
                meeting_end = parser.parse(meeting['end_time'])
                
                if (start_time < meeting_end and end_time > meeting_start):
                    conflicts.append({
                        "participant": participant,
                        "conflicting_meeting": meeting['title'],
                        "conflict_time": f"{meeting_start.isoformat()} - {meeting_end.isoformat()}"
                    })
        
        return conflicts
    
    def calculate_slot_score(self, slot_time: datetime, participant_count: int) -> int:
        """Calculate score for a time slot"""
        score = 50
        
        # Prefer mid-morning and mid-afternoon
        hour = slot_time.hour
        if 10 <= hour <= 11 or 14 <= hour <= 15:
            score += 20
        
        # Prefer fewer participants
        if participant_count <= 3:
            score += 10
        
        return score


# Initialize the assistant
assistant = SmartMeetingAssistant()

# MCP Tool definitions
@mcp.tool()
def create_meeting_tool(title: str, participants: List[str], duration: int, 
                       start_time: str, timezone: str = "UTC") -> Dict[str, Any]:
    """Schedule new meeting with conflict detection"""
    return assistant.create_meeting(title, participants, duration, start_time, timezone)

@mcp.tool()
def find_optimal_slots_tool(participants: List[str], duration: int, 
                           date_range: str) -> Dict[str, Any]:
    """Find AI-powered optimal time slot recommendations"""
    return assistant.find_optimal_slots(participants, duration, date_range)

@mcp.tool()
def detect_scheduling_conflicts_tool(user_id: str, start_time: str, 
                                   end_time: str) -> Dict[str, Any]:
    """Detect scheduling conflicts for a user"""
    return assistant.detect_scheduling_conflicts(user_id, start_time, end_time)

@mcp.tool()
def analyze_meeting_patterns_tool(user_id: str, period: str = "month") -> Dict[str, Any]:
    """Analyze meeting patterns and behaviors for a user"""
    return assistant.analyze_meeting_patterns(user_id, period)

@mcp.tool()
def generate_agenda_suggestions_tool(meeting_topic: str, participants: List[str], 
                                   duration: int = 60) -> Dict[str, Any]:
    """Generate AI-powered meeting agenda suggestions"""
    return assistant.generate_agenda_suggestions(meeting_topic, participants, duration)

@mcp.tool()
def calculate_workload_balance_tool(team_members: List[str]) -> Dict[str, Any]:
    """Calculate meeting workload balance across team members"""
    return assistant.calculate_workload_balance(team_members)

@mcp.tool()
def score_meeting_effectiveness_tool(meeting_id: str) -> Dict[str, Any]:
    """Score meeting effectiveness and provide improvement suggestions"""
    return assistant.score_meeting_effectiveness(meeting_id)

@mcp.tool()
def optimize_meeting_schedule_tool(user_id: str) -> Dict[str, Any]:
    """Get AI-powered schedule optimization recommendations"""
    return assistant.optimize_meeting_schedule(user_id)


def main():
    """Main function - runs MCP server"""
    print("🚀 Smart Meeting Assistant MCP Server initialized!")
    print("Available MCP tools:")
    print("1. create_meeting_tool")
    print("2. find_optimal_slots_tool")
    print("3. detect_scheduling_conflicts_tool")
    print("4. analyze_meeting_patterns_tool")
    print("5. generate_agenda_suggestions_tool")
    print("6. calculate_workload_balance_tool")
    print("7. score_meeting_effectiveness_tool")
    print("8. optimize_meeting_schedule_tool")


if __name__ == "__main__":
    mcp.run()