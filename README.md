# Full Stack Boilerplate

This is a boilerplate project with FastAPI backend, React frontend, and Docker infrastructure.

## Project Structure

```
.
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── terraform/         # Infrastructure as Code
├── docker-compose.yml # Docker Compose configuration
└── README.md
```

## Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)
- Terraform (for infrastructure deployment)

## Running with Docker Compose

1. Build and start the services:
```bash
docker-compose up --build
```

2. Access the applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Running with Terraform

1. Initialize Terraform:
```bash
cd terraform
terraform init
```

2. Apply the configuration:
```bash
terraform apply
```

## Development

### Backend Development

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

### Frontend Development

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## Features

- FastAPI backend with SQLite support
- React frontend with Tailwind CSS
- Docker containerization
- Infrastructure as Code with Terraform
- CORS configuration for development
- Hot reloading for both frontend and backend 