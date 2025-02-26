# PokeAPI - FastAPI Project

## Overview

This project is a FastAPI-based application that interacts with the PokéAPI. It is designed to be fast, scalable, and efficient, utilizing Redis for caching API responses and Jenkins for automated deployment.

## Installation & Setup

<details>
  <summary><b>Setting Up the Environment</b></summary>

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jillazquez/pokeApi.git
   cd pokeApi
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
</details>

## Usage

<details>
  <summary><b>Running the Application</b></summary>

To start the application, run:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at `http://localhost:8000`.
</details>

<details>
  <summary><b>Endpoints</b></summary>

- `GET /pokemon/{name}` - Fetches Pokémon data.
- `GET /cached-pokemon/{name}` - Fetches Pokémon data with Redis caching.
</details>

## Testing

<details>
  <summary><b>Running Unit Tests</b></summary>

This project uses `pytest` for testing. To run the tests, execute:
```bash
pytest tests/
```
</details>

## Deployment

<details>
  <summary><b>Jenkins & Docker Deployment</b></summary>

The application is deployed using Jenkins, which manages two containers:

- **Application Container** - Runs the FastAPI application.
- **Redis Container** - Stores cached responses.

To build and deploy, use Jenkins with a `Dockerfile` and `docker-compose.yml`.
</details>

## Architecture

<details>
  <summary><b>Technology Stack</b></summary>

- **FastAPI** - High-performance Python web framework.
- **Redis** - Used for caching API responses.
- **Pytest** - Testing framework.
- **Jenkins** - Continuous integration and deployment.
</details>

## Contribution

<details>
  <summary><b>How to Contribute</b></summary>

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push the changes:
   ```bash
   git push origin feature/new-feature
   ```
5. Open a Pull Request.
</details>