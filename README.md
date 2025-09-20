# FieldOps - Field Service Coordination Platform

## Project Overview

FieldOps is a backend platform to manage, assign, and track service tasks between Users (Customers), Field Workers, and Admins.

## Features

- User registration and authentication (JWT)
- Role-based access control (Admin, Worker, User)
- Service request creation and management
- Task assignment and tracking
- Dashboard summaries for each role

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Authentication:** JWT
- **ORM:** SQLAlchemy

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.9+
- Docker and Docker Compose

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/your_username_/fieldops.git
    cd fieldops
    ```
2.  **Create a virtual environment and activate it**
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Set up environment variables**
    - Create a `.env` file in the root directory.
    - Copy the contents of `.env` to a new file and fill in the values.
5.  **Start the database**
    ```sh
    docker-compose up -d
    ```
6.  **Run database migrations**
    ```sh
    alembic upgrade head
    ```
7.  **Run the application**
    ```sh
    uvicorn app.main:app --reload
    ```

The application will be available at `http://localhost:8000`. The API documentation can be found at `http://localhost:8000/docs`.
