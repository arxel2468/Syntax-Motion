# Syntax Motion - AI-Powered Animated Video Generator

## Overview

Syntax Motion is a web application that transforms natural language descriptions into animated educational videos using AI and Python's Manim library. Users can create multi-scene projects, each scene being an animation generated from a text prompt.

## Features

- **User Authentication**: Secure login and registration system
- **Project Management**: Create, view, update, and delete animation projects
- **Scene Generation**: Convert text prompts into Manim animation code
- **Video Rendering**: Automatically render animations into downloadable videos
- **Real-time Status Updates**: Track the progress of animation generation
- **Code Viewing**: See the generated Manim code for each animation

## Tech Stack

### Backend
- **Language**: Python
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Animation**: Manim (Mathematical Animation Engine)
- **AI**: Groq API for code generation
- **Authentication**: JWT tokens

### Frontend
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios

## Installation and Setup

### Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm
- PostgreSQL
- Redis (optional, for future task queue implementation)
- Groq API key

### Backend Setup

1. Clone the repository and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Manim dependencies:
   ```bash
   apt-get update && apt-get install -y \
       ffmpeg \
       libcairo2-dev \
       libpango1.0-dev \
       libglib2.0-0 \
       libffi-dev \
       texlive texlive-latex-extra
   ```

5. Set up environment variables in a `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/syntax_motion
   SECRET_KEY=your_secret_key
   GROQ_API_KEY=your_groq_api_key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   MEDIA_ROOT=/path/to/store/media
   ```

6. Create the database:
   ```bash
   createdb syntax_motion
   ```

7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file:
   ```
   VITE_API_URL=http://localhost:8000/api/v1
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## Usage Guide

### 1. Authentication

- Register a new account or log in with existing credentials
- JWT tokens are stored in local storage and automatically used for API requests

### 2. Project Management

- Create a new project from the dashboard or projects page
- View a list of your projects
- Edit or delete projects as needed

### 3. Creating Animations

- In a project, add a new scene by providing a text prompt
- The system will automatically generate Manim code and render the animation
- The animation process goes through multiple phases:
  - **Pending**: Initial state after creation
  - **Processing**: AI is generating code and rendering the animation
  - **Completed**: Animation is ready for viewing
  - **Failed**: If there was an error in generation or rendering

### 4. Viewing and Downloading

- Watch the generated animations directly in the browser
- View the generated Manim code
- Download animations as MP4 files

## Architecture

### Backend Components

1. **API Layer**: FastAPI routes and endpoints
2. **Service Layer**: Business logic for animation generation
3. **Data Layer**: Database models and schemas
4. **Authentication**: JWT-based user authentication

### Frontend Components

1. **Pages**: Main UI views (Dashboard, Projects, Scenes)
2. **Components**: Reusable UI elements (Forms, Cards, Video Player)
3. **State Management**: Zustand stores for data
4. **API Client**: Axios-based service for backend communication

### Animation Generation Pipeline

1. User submits a text prompt for an animation
2. The backend processes the prompt and sends it to the Groq API
3. Groq generates Manim code based on the prompt
4. The code is saved and executed in a safe environment
5. Manim renders the animation to an MP4 file
6. The video is made available for viewing and download

## Future Enhancements

- **Voice-over Integration**: Add narration to animations
- **Timeline Editor**: Arrange multiple scenes with timing controls
- **Templates Gallery**: Pre-made animation templates
- **Collaborative Editing**: Allow teams to work on projects together
- **Advanced Animation Controls**: More customization options for animations
- **Export Options**: Various formats and quality settings

## Troubleshooting

### Common Issues

1. **Video Generation Fails**:
   - Check if Manim dependencies are properly installed
   - Examine the logs for Python errors
   - Try a simpler prompt

2. **API Authentication Errors**:
   - Clear browser storage and log in again
   - Check if your session has expired

3. **Database Connection Issues**:
   - Verify PostgreSQL is running
   - Check database credentials in .env file

## API Documentation

The backend provides a Swagger UI at `/docs` endpoint for exploring and testing the API.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 