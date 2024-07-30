FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv pkg-config default-libmysqlclient-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the image
COPY app.py /app
COPY templates /app
COPY static /app
CMD ["python", "app.py"]
