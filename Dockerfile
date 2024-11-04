FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Set environment variable for Streamlit to run in headless mode
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Create a directory for storing uploaded files
RUN mkdir -p /app/uploads

# Make sure the entrypoint script has the correct line endings
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh && \
    sed -i 's/\r$//' entrypoint.sh

# Use the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]