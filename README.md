# PokeAPI - FastAPI Project

## Overview

This project is a FastAPI-based application that interacts with the PokéAPI. It is designed to be fast, scalable, and efficient, utilizing Redis for caching API responses and Jenkins for automated deployment.

## Installation & Setup

### Setting Up the Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jillazquez/pokeApi.git
   cd pokeApi
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scriptsctivate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Installing Required Tools

#### Install FastAPI and Uvicorn
```bash
pip install fastapi uvicorn
```

#### Install Redis
On Ubuntu:
```bash
sudo apt update && sudo apt install redis-server
```
Start Redis:
```bash
sudo systemctl start redis
```

#### Install Docker
On Ubuntu:
```bash
sudo apt update
sudo apt install docker.io
```
Verify installation:
```bash
docker --version
```

#### Install Docker Compose
```bash
sudo apt install docker-compose
```
Verify installation:
```bash
docker-compose --version
```

#### Install Jenkins
```bash
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
```
```bash
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
```
```bash
sudo apt update && sudo apt install jenkins
```
Start Jenkins:
```bash
sudo systemctl start jenkins
```

## Usage

### Running the Application

To start the application, run on Jenkins:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://localhost:8000`.

### Endpoints

- `GET /pokemon/{name}` - Fetches Pokémon data.
- `GET /cached-pokemon/{name}` - Fetches Pokémon data with Redis caching.

## Testing

### Running Unit Tests

This project uses `pytest` for testing. To run the tests, execute:
```bash
pytest tests/
```

## Deployment

### Jenkins & Docker Deployment

The application is deployed using Jenkins, which manages two containers:

- **Application Container** - Runs the FastAPI application.
- **Redis Container** - Stores cached responses.

To build and deploy, use Jenkins with a `Dockerfile` and `docker-compose.yml`.

## Architecture

### Technology Stack

- **FastAPI** - High-performance Python web framework.
- **Redis** - Used for caching API responses.
- **Pytest** - Testing framework.
- **Jenkins** - Continuous integration and deployment.
- **Sentry** - Catch errors while using the project.
- **Docker & Docker Compose** - Containerized deployment.
