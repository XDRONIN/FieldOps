# Getting Started

To get the FieldOps application running locally, follow these steps.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose

## Steps

1.  **Clone the Repository**
    ```sh
    git clone https://github.com/your_username_/fieldops.git
    cd fieldops
    ```

2.  **Set Up the Environment**
    - Create a virtual environment: `python -m venv venv`
    - Activate it: `source venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`

3.  **Configure Environment Variables**
    - Create a `.env` file from the `.env.example` file.
    - Update the `.env` file with your database credentials and other settings.

4.  **Launch the Database**
    ```sh
    docker-compose up -d
    ```

5.  **Apply Database Migrations**
    ```sh
    alembic upgrade head
    ```

6.  **Run the Application**
    ```sh
    uvicorn app.main:app --reload
    ```

The API will be accessible at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.
