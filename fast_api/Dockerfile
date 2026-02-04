FROM python:3.12

# Set working directory inside the container
WORKDIR /app
# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI application code and dependencies
COPY . ./fast_api/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
