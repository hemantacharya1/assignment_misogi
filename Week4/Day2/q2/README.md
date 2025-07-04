# Smart Meeting Assistant with AI Scheduling (MCP Server)

A Python-based intelligent meeting management system that provides AI-powered scheduling, conflict detection, and meeting optimization using Gemini AI. Built as an MCP (Model Context Protocol) server with 8 tools.

## Features

- **Intelligent Meeting Scheduling**: Create meetings with automatic conflict detection
- **AI-Powered Time Slot Recommendations**: Find optimal meeting times based on participant availability
- **Meeting Pattern Analysis**: Analyze meeting behaviors and productivity trends
- **Smart Agenda Generation**: AI-generated meeting agendas based on topic and participants
- **Workload Balancing**: Calculate and balance meeting workloads across team members
- **Effectiveness Scoring**: Score meeting effectiveness and provide improvement suggestions
- **Schedule Optimization**: Get AI-powered recommendations for schedule improvements
- **Multi-timezone Support**: Handle users across India, US, and Europe time zones

## Project Structure

```
Week4/Day2/q2/
├── README.md                    # This file
├── src/
│   └── server.py               # Main application with all 8 methods
├── data/
│   └── sample_content.json     # Sample data with 5 users and 20+ meetings
├── tests/
│   └── test_meeting_tools.py   # Comprehensive test suite
├── pyproject.toml              # Project configuration and dependencies
└── .env                        # Environment variables (create this)
```

## Setup Instructions

### 1. Environment Setup

```bash
# Navigate to project directory
cd Week4/Day2/q2

# Create virtual environment (if not already created)
uv venv

# Activate environment
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Windows Command Prompt:
.venv\Scripts\activate.bat
# On Unix/MacOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install all required packages
uv sync

# Or install manually
uv add google-generativeai python-dotenv pytz python-dateutil pytest fastmcp
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key from**: https://makersuite.google.com/app/apikey

### 4. Run the MCP Server

```bash
# Run as MCP server
python src/server.py

# Run tests
pytest tests/ -v
```

## Available Methods

The Smart Meeting Assistant provides 8 core methods:

### 1. `create_meeting(title, participants, duration, start_time, timezone)`
Schedule new meetings with automatic conflict detection.

**Example:**
```python
result = assistant.create_meeting(
    title="Team Standup",
    participants=["user1", "user2"],
    duration=30,
    start_time="2025-02-01T10:00:00",
    timezone="UTC"
)
```

### 2. `find_optimal_slots(participants, duration, date_range)`
AI-powered time slot recommendations based on participant availability.

**Example:**
```python
result = assistant.find_optimal_slots(
    participants=["user1", "user2", "user3"],
    duration=60,
    date_range="2025-02-01"
)
```

### 3. `detect_scheduling_conflicts(user_id, start_time, end_time)`
Identify scheduling conflicts for a specific user.

**Example:**
```python
result = assistant.detect_scheduling_conflicts(
    user_id="user1",
    start_time="2025-02-01T10:00:00",
    end_time="2025-02-01T11:00:00"
)
```

### 4. `analyze_meeting_patterns(user_id, period)`
Analyze meeting behaviors and productivity trends.

**Example:**
```python
result = assistant.analyze_meeting_patterns(
    user_id="user1",
    period="month"
)
```

### 5. `generate_agenda_suggestions(meeting_topic, participants, duration)`
AI-generated meeting agendas based on topic and participants.

**Example:**
```python
result = assistant.generate_agenda_suggestions(
    meeting_topic="Product Planning",
    participants=["user1", "user2", "user3"],
    duration=60
)
```

### 6. `calculate_workload_balance(team_members)`
Calculate meeting workload distribution across team members.

**Example:**
```python
result = assistant.calculate_workload_balance(
    team_members=["user1", "user2", "user3", "user4", "user5"]
)
```

### 7. `score_meeting_effectiveness(meeting_id)`
Score meeting effectiveness and provide improvement suggestions.

**Example:**
```python
result = assistant.score_meeting_effectiveness(
    meeting_id="meeting1"
)
```

### 8. `optimize_meeting_schedule(user_id)`
Get AI-powered recommendations for schedule optimization.

**Example:**
```python
result = assistant.optimize_meeting_schedule(
    user_id="user1"
)
```

## Sample Data

The system includes realistic sample data with:

- **5 Users** across different time zones:
  - Priya Sharma (CEO, India - Asia/Kolkata)
  - John Smith (Engineering Manager, US - America/New_York)
  - Maria Garcia (Product Manager, Europe - Europe/Berlin)
  - David Wilson (Senior Developer, US - America/Los_Angeles)
  - Raj Patel (Sales Director, India - Asia/Kolkata)

- **20+ Meetings** with various types:
  - 1:1 meetings
  - Team meetings
  - Client calls
  - All-hands meetings
  - Technical reviews
  - Strategy sessions

## Response Format

All methods return standardized JSON responses:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Method-specific data
  }
}
```

For errors:
```json
{
  "success": false,
  "error": "Error description",
  "data": null
}
```

## AI Integration

The system uses **Gemini Flash 1.5** for AI-powered features:

- **Agenda Generation**: Creates detailed meeting agendas based on topic and participants
- **Meeting Analysis**: Provides insights into meeting patterns and productivity
- **Schedule Optimization**: Suggests improvements for better work-life balance
- **Effectiveness Scoring**: Evaluates meeting quality and provides recommendations

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_meeting_tools.py::TestSmartMeetingAssistant::test_create_meeting_success -v

# Run with coverage
pytest tests/ --cov=src
```

## Usage Examples

### Complete Workflow Example

```python
from src.server import SmartMeetingAssistant

# Initialize the assistant
assistant = SmartMeetingAssistant()

# 1. Find optimal time slots
slots = assistant.find_optimal_slots(
    participants=["user1", "user2"],
    duration=60,
    date_range="2025-02-01"
)

# 2. Create meeting using suggested slot
if slots["success"] and slots["data"]["suggestions"]:
    best_slot = slots["data"]["suggestions"][0]
    
    meeting = assistant.create_meeting(
        title="Product Planning Meeting",
        participants=["user1", "user2"],
        duration=60,
        start_time=best_slot["start_time"]
    )
    
    # 3. Generate agenda
    agenda = assistant.generate_agenda_suggestions(
        meeting_topic="Product Planning",
        participants=["user1", "user2"],
        duration=60
    )
    
    # 4. Check workload balance
    workload = assistant.calculate_workload_balance(
        team_members=["user1", "user2"]
    )
    
    print("Meeting created successfully!")
    print(f"Meeting ID: {meeting['data']['id']}")
    print(f"Workload balance: {workload['data']}")
```

## Limitations

- **AI Features**: Require valid Gemini API key for full functionality
- **Time Zones**: Currently supports India, US, and Europe time zones
- **Data Storage**: Uses JSON file storage (not suitable for production)
- **Concurrency**: No concurrent access protection

## Future Enhancements

- Integration with calendar APIs (Google Calendar, Outlook)
- Real-time notifications and reminders
- Advanced ML models for better recommendations
- Database storage for production use
- Web API interface for external integrations

## Contributing

1. Ensure all tests pass: `pytest tests/ -v`
2. Follow the existing code style and patterns
3. Add tests for new features
4. Update documentation for any API changes

## License

This project is for educational purposes as part of the assignment structure.
