

FROM python:3.10-slim

WORKDIR /app

# Copy the Python application
COPY . /app/

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "HoeWarmIsHetInDelft.py"]
