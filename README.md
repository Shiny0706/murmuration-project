# Survey Data Explorer

A complete solution for exploring and analyzing AI sentiment survey data.

## Project Overview

This project provides a system to:
1. Upload and process CSV survey data
2. Explore survey responses through an API
3. Visualize survey results through an interactive interface

The system is designed to help analyze a mix of human and AI-generated survey responses on artificial intelligence sentiment.

## Components

### Backend

- FastAPI-based RESTful API
- SQLite database for data storage
- API endpoints for survey data access
- CSV upload functionality

### Frontend

- React-based UI
- Survey data upload interface
- Interactive data visualization with Chart.js
- Filtering and grouping capabilities

### Infrastructure 

- Docker containerization
- Docker Compose for local development
- Terraform configuration for AWS deployment

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.9+ (for local backend development)
- Terraform (for infrastructure provisioning)

### Local Development

1. Clone the repository
2. Start the development environment:

```bash
docker-compose up
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Setup (Without Docker)

#### Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `GET /surveys`: All survey responses
- `GET /surveys/{survey_name}`: Filtered by survey
- `GET /questions/{question_id}`: Responses to a specific question
- `POST /upload`: Upload CSV files to refresh survey data

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── database/     # Database models and connection
│   │   ├── models/       # Data models
│   │   └── routers/      # API endpoints
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── store/        # Redux Store
│   ├── Dockerfile
│   └── package.json
├── infrastructure/       # Terraform configuration
├── docker-compose.yml
└── README.md
```

## Sample Data

A sample CSV file (`sample_survey_data.csv`) is included in the repository to demonstrate the expected format for survey data uploads.

## Author

Project created as part of a technical assessment. 