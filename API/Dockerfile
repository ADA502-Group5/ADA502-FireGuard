FROM python:3.12

# Set working directory
WORKDIR /app

# Copy all files into the container's /app directory
COPY . .

# Install pip dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8080

# Run the FastAPI app
CMD ["python", "main.py"]
