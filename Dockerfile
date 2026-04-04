# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies first (better Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 7860

# Start the server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]