FROM python:3.12

# Copy entire codebase into the container
COPY . .

# Install pip dependencies and dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Run the app
CMD ["python", "main.py"]
