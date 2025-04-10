The Fireguard project is a group assignment for the ADA502 - Cloud Computing course at HVL, utilizing an API built with FastAPI.

# Technologies
- **Python**: Programming language used to develop the API.
- **FastAPI**: Framework for building the API with Python.
- **PostgreSql**: Database for storing data.
- **Pydantic**: Library used for validating data.
- **Docker**: Used for containerizing the application.
- **Docker-compose**: Used to manage multiple Docker containers (Two containers; API and database).
- **Postman**: USed for testing API endpoints and sending HTTP requests (GET, POST, PUT, DELETE)

# Setup
## Pre-requisites
- **Python**: v. 3.12 is used for this project. URL: https://www.python.org/downloads/. Follow the instructions and add install directory to environment variables (PATH).
- **Docker/ Docker Desktop**: Docker desktop is only necessary on windows or ios systems to host and run docker containers as Docker relies on linux kernel features. URL: https://www.docker.com/products/docker-desktop/. Follow the instructions to download docker desktop. When installing Docker Desktop, both Docker and WSL are installed which is essensial to run docker containers. To verify Docker and WSL installations, we use the following commands in cmd:

Docker:
```docker --version```

WSL:
```wsl -l -v```

## Installing Dependencies
1. **Clone the project repository**: The project is obviously required on your computer in order to run it locally. Now open cmd and navigate to your desired directory for this project using ```cd <dir>```, followed by ```git clone https://github.com/ADA502-Group5/ADA502-FireGuard.git```. Congratz now you have access to the fireguard project.
2. **Install Python dependencies**: Let's intsall dependencies using ```poetry``` or ```pip```.

```poetry install```

or

```pip install -r requirements.txt```
requirements.txt contains the dependencies/ libraries that are required for the project to run. It lists all packages and versions that the project depends on. 

## Running the Application
**Run with docker compose**: To start the application using Docker Compose, the Docker Desktop needs to be open and then simply run:

   ```docker-compose up --build```

This will build the Docker containers and start PostgreSQL and API services in the docker environments. The API will be accessible at ```http://localhost:8080``` (port: 8080) which can be opened in any browser. The docker containers can now be ran directly from docker desktop in the future, however if you reconfigure the docker files, the docker containers need to be rebuilt.

# API Endpoints
- **GET/checkhealth**: Checks if the API is alive. Easy to check whether the application runs correctly or not.
- **GET/locations/{location}**: Fetches all registrations for a specified location.
- **POST/locations/{location}**: Creates new registration for a specified location.
- **DELETE/locations/{location}**: Deletes old registration for a specified location.

This part is not complete yet...
