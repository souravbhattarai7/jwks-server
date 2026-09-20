JWKS Server

A basic RESTful JSON Web Key Set (JWKS) server built with Python and FastAPI.

Features
Generates RSA key pairs.
Gives each key a unique kid.
Stores an expiration time for each key.
Returns unexpired public keys through /jwks.
Creates valid JWTs through /auth.
Creates an expired JWT through /auth?expired=true.
Uses RS256 to sign JWTs.
Includes the key ID (kid) in the JWT header.
Includes automated tests with pytest.
Uses Ruff for code linting.
Requirements
Python 3.14+
FastAPI
Uvicorn
PyJWT
Cryptography
Pytest
Pytest-Cov
Ruff
Setup

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the required packages:

python3 -m pip install fastapi uvicorn pyjwt cryptography pytest pytest-cov ruff httpx2
Running the Server

Start the server with:

python3 -m uvicorn app.main:app --port 8080

The server runs at:

http://127.0.0.1:8080
API Endpoints
GET /jwks

Returns the currently active public RSA key in JWKS format.

Example:

curl http://127.0.0.1:8080/jwks
POST /auth

Creates a JWT signed with the active RSA private key.

curl -X POST http://127.0.0.1:8080/auth
POST /auth?expired=true

Creates a JWT signed with the expired RSA key.

curl -X POST "http://127.0.0.1:8080/auth?expired=true"

The expired key is not included in the /jwks response.

Testing

Run the test suite with:

python3 -m pytest

Run tests with coverage:

python3 -m pytest --cov=app --cov-report=term-missing

The current test suite contains 6 tests and achieved 100% code coverage.

Linting

Run Ruff with:

python3 -m ruff check .
Project Structure
jwks-server/
├── app/
│   ├── __init__.py
│   ├── keys.py
│   └── main.py
├── tests/
│   └── test_server.py
├── venv/
└── README.md