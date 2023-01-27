FROM python:3-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard.py .

CMD ["python3", "-u", "dashboard.py"]