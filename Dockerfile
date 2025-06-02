# Use a slim Python base image for efficiency
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files to the container
COPY . .

# Expose port 8000 for the API
EXPOSE 8000

# Run the FastAPI app with uvicorn, binding to all interfaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]