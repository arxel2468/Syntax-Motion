# Syntax Motion - Quick Start Guide

This guide will help you set up and run the Syntax Motion application locally.

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Groq API key (for AI-powered animation generation)

## Backend Setup

1. **Set up your database**

   Create a database named `syntax_motion`:
   ```bash
   createdb syntax_motion
   ```

2. **Configure environment variables**

   In the `backend` directory, create or edit a `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/syntax_motion
   SECRET_KEY=your_secret_key_here
   GROQ_API_KEY=your_groq_api_key_here
   MEDIA_ROOT=./media
   ```

3. **Activate the virtual environment**

   ```bash
   cd backend
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Install Manim dependencies**

   Ubuntu/Debian:
   ```bash
   sudo apt-get update && sudo apt-get install -y \
       ffmpeg \
       libcairo2-dev \
       libpango1.0-dev \
       libglib2.0-0 \
       libffi-dev \
       texlive texlive-latex-extra
   ```

   macOS:
   ```bash
   brew install cairo libpango ffmpeg
   ```

6. **Run the backend**

   ```bash
   uvicorn app.main:app --reload
   ```

   The backend will be available at http://localhost:8000

## Frontend Setup

1. **Install dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment variables**

   Create or edit a `.env` file in the `frontend` directory:
   ```
   VITE_API_URL=http://localhost:8000/api/v1
   ```

3. **Run the frontend**

   ```bash
   npm run dev
   ```

   The frontend will be available at http://localhost:3000

## Using the Application

1. Register or login with your credentials
2. Create a new project from the dashboard
3. Add scenes by providing natural language descriptions
4. Wait for the AI to generate animations (this may take a few minutes per scene)
5. View, play, and download your animations

## Video Directories

By default, generated videos are stored in:
```
backend/media/videos/
```

You can change this by modifying the `MEDIA_ROOT` in your `.env` file.

## Troubleshooting

- If you see authentication errors, make sure you're logged in
- If video generation fails, ensure all Manim dependencies are installed
- For any backend errors, check the terminal running the backend server 