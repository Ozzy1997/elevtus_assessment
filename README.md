# elevtus_assessment



# FastAPI Candidate Management API

This repository contains a FastAPI application for managing candidate profiles. The application includes CRUD operations for users and candidates, search functionality, and report generation.

## Features

- **Health Check Endpoint**: Verify the server status.
- **User Management**: Create and manage users.
- **Candidate Management**: CRUD operations for candidate profiles.
- **Search Functionality**: Search for candidates based on various fields.
- **Report Generation**: Generate a CSV report of all candidates' information.
- **Authorization**: Only authorized users can access candidate-related endpoints.
- **Data Validation**: Validate request models using Pydantic.
- **Testing**: Test-driven development (TDD) to ensure code functionality.
- **Organized Code Structure**: Follows OOP principles and uses Service/Repository Design Pattern.

## Prerequisites

- Python 3.8 or higher
- MongoDB

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Ozzy1997/elevtus_assessment
    cd https://github.com/Ozzy1997/elevtus_assessment
    ```

2. **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the following environment variables:
    ```plaintext
    MONGODB_URI=<your-mongodb-uri>
    SECRET_KEY=<your-secret-key>
    ```

## Running the Application

1. **Start MongoDB**:
    Ensure MongoDB is running on your local machine or accessible through the specified URI.

2. **Run the FastAPI Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

3. **Access the API**:
    Open your browser and go to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Endpoints

- **Health Check**: `GET /health`
- **User Management**:
  - `POST /user`
  - `GET /user/{email}`
  - `PUT was not requested and can be easily implemented`
  - `DELETE was not requested and can be easily implemented`
- **Candidate Management**:
  - `POST /candidate`
  - `GET /candidate/get_by_id`
  - `PUT /candidate/`
  - `DELETE /candidate/{candidate_id}`
- **Search Candidates**: `GET /all-candidates`
  - Fetch all candidates from the database. Optionally, you can provide a search query to filter results.
  - The search query can be a simple text search or a specific field search in the format `field:value`.
  - Examples:
    - `search_query=John` will search across all text-indexed fields for 'John'.
    - `search_query=email:john@example.com` will search for candidates with the email 'john@example.com'.
- **Generate Report**: `GET /generate-report`
