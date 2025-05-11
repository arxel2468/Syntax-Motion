FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Manim
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
