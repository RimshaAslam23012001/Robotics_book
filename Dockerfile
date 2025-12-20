# Use slim Python image
FROM python:3.12.10-slim

# Set working directory in container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY src ./src
COPY main.py ./main.py
COPY app.py ./app.py

# Expose the port FastAPI will run on
EXPOSE 7860

# Run your FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]
