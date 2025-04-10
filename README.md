The Fireguard project is a group assignment for the ADA502 - Cloud Computing course at HVL, utilizing an API built with FastAPI.

# Technologies
- **Python**: Programming language used to develop the API.
- **FastAPI**: Framework for building the API with Python.
- **PostgreSql**: Database for storing data.
- **Pydantic**: Library used for validating data.
- **Docker**: Used for containerizing the application.
- **Docker-compose**: Used to manage multiple Docker containers (Two containers; API and database).

# Setup
## Pre-requisites
- **Python**: v. 3.12 is used for this project. URL: https://www.python.org/downloads/. Follow the instructions and add install directory to environment variables (PATH).
- **Docker/ Docker Desktop**: Docker desktop is only necessary on windows or ios systems to host and run docker containers as Docker relies on linux kernel features. URL: https://www.docker.com/products/docker-desktop/. Follow the instructions to download docker desktop. When installing Docker Desktop, both Docker and WSL are installed which is essensial to run docker containers. To verify Docker and WSL installations, we use the following commands in cmd:

Docker:
```docker --version```

WSL:
```wsl -l -v```

## Installing Dependencies
1. **Clone the project repository**: The project is obviously required on your computer in order to run it locally. Now open cmd and navigate to your desired directory for this project using

```cd <dir>```

, followed by 

```git clone https://github.com/ADA502-Group5/ADA502-FireGuard.git```

Congratz now you have access to the fireguard project.
