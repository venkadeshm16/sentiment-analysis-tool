FROM python:3.10.0-alpine
COPY python /python
COPY requirements.txt /python
WORKDIR /python
RUN pip3 install -r requirements.txt
CMD ["python", "app.py"]