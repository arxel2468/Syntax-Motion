# Syntax Motion - AI-Powered Animated Video Generator

Syntax Motion is an innovative tool that allows you to create beautiful animated videos using only text prompts. Leveraging the power of AI and mathematical animation (using Manim), Syntax Motion transforms your ideas into visually stunning animations.

## Features

- **Text-to-Animation**: Transform text prompts into mathematical animations
- **Project Management**: Create, organize, and manage multiple animation projects
- **Scene Creation**: Build complex animations scene by scene
- **AI-Generated Code**: View and customize the Manim code used to generate your animations
- **Video Export**: Download your animations as MP4 files

## Tech Stack

### Frontend
- React with TypeScript
- Tailwind CSS for styling
- Zustand for state management
- Axios for API requests

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL database
- Manim for mathematical animations
- OpenAI API for generating animation code

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- PostgreSQL
- Redis (for task queue)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your .env file:
   ```
   cp .env.example .env
   ```
   Update the .env file with your database credentials and OpenAI API key.

5. Run the backend server:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser and visit:
   ```
   http://localhost:3000
   ```

## Project Structure

```
syntax-motion/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── db/           # Database models and setup
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic services
│   │   └── utils/        # Utility functions
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment variables
├── frontend/             # React frontend
│   ├── public/           # Static assets
│   ├── src/              # Source code
│   │   ├── api/          # API service
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── pages/        # Page components
│   │   ├── store/        # Zustand store
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utility functions
│   ├── package.json      # Node dependencies
│   └── tailwind.config.js # Tailwind CSS config
└── README.md             # Project documentation
```

## License

MIT
