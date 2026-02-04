FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements files
COPY clickhouse/requirements.txt /app/clickhouse/requirements.txt
COPY data_source/requirements.txt /app/data_source/requirements.txt

# Install all requirements
RUN pip install --no-cache-dir -r clickhouse/requirements.txt && \
    pip install --no-cache-dir -r data_source/requirements.txt

# Copy setup scripts and necessary files
COPY clickhouse/setup.py /app/clickhouse/setup.py
COPY data_source/setup.py /app/data_source/setup.py
COPY data_source/files /app/data_source/files

# Default command (can be overridden)
CMD ["python", "--version"]
