FROM python:3.10-slim

WORKDIR /python

# System deps for scientific Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python/ .

EXPOSE 5000

CMD ["python", "app.py"]


