# SIMANTAP Backend
## Description
This is the backend service for the SIMANTAP SIstem Manajemen ANTrian Administrasi dan bimbingan Prodi. An application to help managing [Antrian Administrasi dan Bimbingan Program Studi Teknik Informatika ITERA]. This application using Python FastAPI to serve backend and React to serve frontend [click this link if you wanna check the frontend client of this application] or you can test the fully running application here [insert simantap link here].

## Features
- [Feature 1]: Brief description
- [Feature 2]: Brief description
- [Feature 3]: Brief description

## Getting Started

Follow these steps to set up the project after cloning the repository:

### Prerequisites
Ensure you have the following installed:
- Python (i don't know minimun but i use version 3.12.6)
- pip (i'm using version 25.0.1)
- Postgresql or any SQLdatabase
- Supabase or anything for storage
- Sanity, and Sheer Willpower

### Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BangKumish/backend.git
    cd Project_TA/backend
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Database Migrations with Alembic**:
    - Initialize Alembic:
        ```bash
        alembic init migrations
        ```
    - Configure the `alembic.ini` file and the `env.py` file in the `migrations` directory as needed.
    - Generate a new migration script:
        ```bash
        alembic revision --autogenerate -m "Initial migration"
        ```
    - Apply the migration to the database:
        ```bash
        alembic upgrade head
        ```

5. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

You are now ready to use the backend service for Project_TA.