#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}     Syntax Motion - Development Mode     ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Function to check if command exists
command_exists() {
  command -v "$1" &> /dev/null
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Check Python
if command_exists python3; then
  PYTHON_CMD="python3"
elif command_exists python; then
  PYTHON_CMD="python"
else
  echo -e "${RED}Error: Python is not installed. Please install Python 3.10 or higher.${NC}"
  exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d " " -f 2)
echo -e "Python version: ${GREEN}$PYTHON_VERSION${NC}"

# Check Node.js
if ! command_exists node; then
  echo -e "${RED}Error: Node.js is not installed. Please install Node.js 18 or higher.${NC}"
  exit 1
fi

NODE_VERSION=$(node -v)
echo -e "Node.js version: ${GREEN}$NODE_VERSION${NC}"

# Check npm
if ! command_exists npm; then
  echo -e "${RED}Error: npm is not installed. Please install npm.${NC}"
  exit 1
fi

NPM_VERSION=$(npm -v)
echo -e "npm version: ${GREEN}$NPM_VERSION${NC}"

# Check PostgreSQL
if ! command_exists psql; then
  echo -e "${YELLOW}Warning: PostgreSQL CLI (psql) is not found. Make sure PostgreSQL is running.${NC}"
else
  echo -e "PostgreSQL CLI: ${GREEN}installed${NC}"
fi

# Check if Manim is installed
if ! $PYTHON_CMD -c "import manim" &> /dev/null; then
  echo -e "${YELLOW}Warning: Manim is not installed in the current Python environment.${NC}"
  echo -e "This may be ok if you're using a virtual environment for the backend."
else
  echo -e "Manim: ${GREEN}installed${NC}"
fi

echo ""
echo -e "${YELLOW}Starting Backend and Frontend Services...${NC}"
echo ""

# Start backend in background
echo -e "${BLUE}Starting backend server...${NC}"
if [ -d "backend/.venv" ]; then
  echo "Activating virtual environment..."
  # Check the shell for sourcing the right activate script
  if [ -f "backend/.venv/bin/activate" ]; then
    source backend/.venv/bin/activate
  else
    source backend/.venv/Scripts/activate
  fi
else
  echo -e "${YELLOW}Warning: No virtual environment found at backend/.venv${NC}"
  echo -e "Using system Python. It's recommended to create a virtual environment."
fi

cd backend
if [ ! -f ".env" ]; then
  echo -e "${YELLOW}Warning: No .env file found in backend directory.${NC}"
  echo -e "Creating .env from .env.example..."
  cp .env.example .env
  echo -e "${YELLOW}Please update the .env file with your database and API credentials.${NC}"
fi

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Starting backend server..."
$PYTHON_CMD -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}Backend server started! (PID: $BACKEND_PID)${NC}"
echo "Backend available at: http://localhost:8000"

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 5
cd ..

# Start frontend in background
echo -e "${BLUE}Starting frontend server...${NC}"
cd frontend
echo "Installing frontend dependencies..."
npm install

echo "Starting frontend development server..."
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend server started! (PID: $FRONTEND_PID)${NC}"
echo ""

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}    All services started successfully!     ${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "Frontend URL: ${BLUE}http://localhost:3000${NC}"
echo -e "Backend API: ${BLUE}http://localhost:8000${NC}"
echo -e "API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Capture Ctrl+C to clean up processes
trap "echo -e '${YELLOW}Stopping services...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo -e '${GREEN}Services stopped.${NC}'; exit 0" INT

# Keep script running
wait 