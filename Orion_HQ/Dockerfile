# 1. Start with a lightweight Python base
FROM python:3.11-slim-bookworm

# 2. Install SDR drivers for the PlutoSDR
RUN apt-get update && apt-get install -y \
    libiio0 \
    libiio-utils \
    python3-libiio \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Copy and install your requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your project code
COPY . .

# 6. Launch the mission
CMD ["python", "-u", "main.py"]
