# AI-Powered Animated Video Generator

## Overview
A web platform that transforms natural language prompts into educational animated videos. The system leverages LLMs to generate animation code, executes it in a secure sandbox, and produces downloadable video content. Users can create multi-scene projects with optional voice-overs.

## Core Features
- Natural language to animation conversion
- Multi-scene project management
- Real-time video preview
- Voice-over integration
- Timeline-based scene arrangement
- Secure code execution

## Technical Architecture

### Backend Stack
- **Language**: Python
- **Framework**: FastAPI
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL
- **Animation**: Manim
- **LLM**: OpenAI GPT API
- **Container**: Docker
- **Auth**: JWT/OAuth

### Frontend Stack
- **Framework**: React + Vite
- **Language**: TypeScript
- **API**: Axios
- **Video**: react-player
- **State**: Zustand
- **UI**: Chakra UI/Material UI
- **Drag & Drop**: react-beautiful-dnd

### Infrastructure
- **DevOps**: Docker Compose
- **Config**: Environment variables (.env)
- **Deployment**: Docker Compose (local), Kubernetes (production)

## Project Structure
```
ai-animated-video-generator/
├── backend/          # Python FastAPI backend
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React + Vite frontend
│   ├── src/
│   ├── index.html
│   └── vite.config.ts
├── docker-compose.yml
├── .env
└── README.md
```

## Core Components

### Entities
1. **User**
   - Authentication
   - Project management
   - Scene creation

2. **Project**
   - Scene collection
   - Timeline management
   - Video composition

3. **Scene**
   - Prompt processing
   - Code generation
   - Video rendering

4. **Video**
   - Output management
   - Preview generation
   - Download handling

5. **VoiceOver** (Optional)
   - Audio integration
   - Scene synchronization

### Database Schema

#### User
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| username | VARCHAR | Unique |
| email | VARCHAR | Unique |
| password_hash | VARCHAR | Hashed |
| created_at | TIMESTAMP | Creation time |

#### Project
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| user_id | UUID | Foreign Key |
| title | VARCHAR | Project name |
| created_at | TIMESTAMP | Creation time |

#### Scene
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| project_id | UUID | Foreign Key |
| prompt | TEXT | User input |
| code | TEXT | Generated code |
| video_url | VARCHAR | Video location |
| order | INT | Scene position |
| status | ENUM | Processing state |
| created_at | TIMESTAMP | Creation time |

#### Video
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| scene_id | UUID | Foreign Key |
| file_path | VARCHAR | Storage path |
| duration | FLOAT | Length (seconds) |
| created_at | TIMESTAMP | Creation time |

#### VoiceOver
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary Key |
| scene_id | UUID | Foreign Key |
| file_path | VARCHAR | Audio path |
| created_at | TIMESTAMP | Creation time |

## Development Setup

### Environment Configuration
1. Clone repository
2. Configure `.env` files
3. Set up Docker Compose

### Backend Development
1. Initialize FastAPI project
2. Set up PostgreSQL with SQLAlchemy
3. Configure Celery with Redis
4. Implement LLM integration
5. Set up Docker sandbox
6. Configure authentication

### Frontend Development
1. Create React + Vite project
2. Set up TypeScript
3. Configure Zustand store
4. Implement video player
5. Create timeline interface
6. Set up API integration

### Running the Project
```bash
# Start all services
docker-compose up --build

# Access points
Frontend: http://localhost:5173
Backend API: http://localhost:8000
```

## User Flow Example
1. User logs in
2. Creates new project
3. Adds scene with prompt
4. Previews generated video
5. Adds more scenes
6. Arranges timeline
7. Downloads final video

## Security Considerations
- Secure code execution
- API key protection
- User authentication
- Input validation
- Rate limiting
- Resource quotas