# Syntax Motion Quick Start Guide

This guide will help you set up and run the Syntax Motion application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python 3.10+ with venv
- Node.js 18+ and npm
- PostgreSQL
- Redis (optional, for advanced features)
- Manim Community Edition

## Backend Setup

1. **Clone the repository and navigate to the project folder**

2. **Set up a Python virtual environment**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**
   - Copy `.env.example` to `.env`
   - Update the `DATABASE_URL` to point to your database
   - Add your `GROQ_API_KEY`

5. **Create the database**
   ```bash
   # In PostgreSQL
   createdb syntax_motion
   
   # Then run migrations
   alembic upgrade head
   ```

6. **Start the backend server**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
   The backend API will be available at http://localhost:8000

## Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## Using the Application

1. **Register a new account** or log in if you already have one

2. **Create a new project** by clicking on the "New Project" button

3. **Add scenes to your project** by clicking on "Add Scene" within your project

4. **Create an animation** by entering a prompt describing what you want to animate

5. **View the generated animation** once processing is complete

## Troubleshooting Common Issues

### Backend Issues

- **Database connection errors**: Make sure PostgreSQL is running and your `DATABASE_URL` is correct
- **Missing GROQ API key**: Ensure you've set up the `GROQ_API_KEY` in your `.env` file
- **Animation generation fails**: Install Manim correctly and check the error message in the scene details

### Frontend Issues

- **API connection errors**: Ensure the backend is running on port 8000
- **Blank pages**: Check the browser console for JavaScript errors

## Example Animations

The `backend/examples` directory contains sample animations you can use as references:

- `fixed_client_server.py` - A client-server interaction animation
- `basic_shapes.py` - Various shape animations with transformations
- `data_graphs.py` - A data visualization example with graphs

## Further Resources

- Check the `docs/MANIM_GUIDE.md` file for detailed information about creating Manim animations
- Visit the [Manim Community documentation](https://docs.manim.community/) for more information on Manim 