# 🤖 MCP Q&A Chatbot

A modern, responsive Q&A chatbot specialized in answering questions about Model Context Protocol (MCP) using Google's Gemini API.

## ✨ Features

- **🧠 MCP Expertise**: Specialized knowledge about Model Context Protocol
- **🎨 Modern UI**: Clean, responsive interface built with React + Tailwind CSS
- **🚀 AI-Powered**: Uses Google Gemini API for intelligent responses
- **⚡ Fast API**: Backend powered by FastAPI for optimal performance
- **🔄 Real-time**: Instant responses with loading states and error handling

## 🛠️ Technologies Used

### Frontend
- **React 19** - Modern React framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **PostCSS** - CSS post-processor

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini API** - AI language model
- **Uvicorn** - ASGI web server
- **CORS** - Cross-Origin Resource Sharing

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

### 1. Setup Backend

```bash
# Navigate to backend directory
cd Week4/Day1/q1/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_actual_gemini_api_key_here" > .env
```

### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd Week4/Day1/q1/frontend

# Install dependencies
npm install

# Install additional required dependencies (if not already installed)
npm install -D postcss autoprefixer
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd Week4/Day1/q1/backend
# Activate virtual environment first
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd Week4/Day1/q1/frontend
npm run dev
```

### 4. Access the Application

Open your browser and navigate to: `http://localhost:5173`

## 📁 Project Structure

```
Week4/Day1/q1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── llm_utils.py         # Gemini API integration
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (create this)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main application component
│   │   ├── ChatBox.jsx      # Chat interface component
│   │   ├── main.jsx         # React entry point
│   │   ├── App.css          # Custom styles and animations
│   │   └── index.css        # Tailwind CSS imports
│   ├── package.json         # Node.js dependencies
│   ├── postcss.config.js    # PostCSS configuration
│   ├── tailwind.config.js   # Tailwind CSS configuration
│   └── index.html           # HTML template
└── README.md                # This file
```

## 🎯 How to Use

1. **Start both servers** (backend on port 8000, frontend on port 5173)
2. **Open the web interface** at `http://localhost:5173`
3. **Type your MCP question** in the textarea
4. **Click "Ask Gemini"** to get an AI-powered response
5. **View the answer** in the response area below

## 💡 Example Questions

- "What is Model Context Protocol?"
- "How do I implement MCP resources?"
- "What are the differences between MCP tools and prompts?"
- "How to set up an MCP server?"
- "Best practices for MCP implementation?"
- "How does MCP handle authentication?"

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Frontend Configuration

The frontend is configured to connect to the backend at `http://localhost:8000`. If you change the backend port, update the API URL in `src/ChatBox.jsx`.

## 🎨 Styling Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Gradient Backgrounds**: Modern visual design
- **Smooth Animations**: Enhanced user experience
- **Focus States**: Proper accessibility support
- **Loading States**: Visual feedback during API calls

## 🛠️ Troubleshooting

### Common Issues

1. **"Tailwind styles not working"**
   - Ensure `postcss.config.js` exists in the frontend directory
   - Check that `tailwindcss` and `autoprefixer` are installed
   - Verify `npm run dev` is running without errors

2. **"Port 8000 already in use"**
   ```bash
   uvicorn main:app --reload --port 8001
   ```
   Then update the API URL in `ChatBox.jsx` to `http://localhost:8001`

3. **"Gemini API Error"**
   - Verify your API key is correct in the `.env` file
   - Check that your API key has proper permissions
   - Ensure Google Cloud billing is enabled

4. **"Frontend not loading properly"**
   - Check browser console for errors
   - Ensure all npm dependencies are installed
   - Try clearing browser cache and restarting the dev server

5. **"CORS Issues"**
   - Backend is configured for `localhost:5173`
   - If using a different port, update CORS settings in `main.py`

### Development Tips

- Use browser developer tools to inspect network requests
- Check the terminal for both frontend and backend error messages
- The backend logs all API requests for debugging

## 🔄 Development Workflow

1. **Make changes** to React components in `src/`
2. **Hot reload** automatically updates the browser
3. **Check browser console** for any JavaScript errors
4. **Test API endpoints** using the chat interface
5. **Monitor backend logs** for API call debugging

## 📚 Dependencies

### Frontend Dependencies
- `react` - UI library
- `react-dom` - DOM renderer
- `tailwindcss` - CSS framework
- `postcss` - CSS processor
- `autoprefixer` - CSS vendor prefixes

### Backend Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variables
- `google-generativeai` - Gemini API client

## 🌟 Next Steps

- [ ] Add conversation history
- [ ] Implement real-time web scraping for MCP content
- [ ] Add vector database for better context retrieval
- [ ] Implement user authentication
- [ ] Add more sophisticated prompt engineering
- [ ] Deploy to production

## 📝 License

This project is for educational purposes as part of the Misogi assignment.

---

**Happy Coding!** 🚀

For questions or issues, please check the troubleshooting section above.
