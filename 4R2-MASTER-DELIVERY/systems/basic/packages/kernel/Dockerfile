FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api_fastapi.py .
COPY kernel_1240421.py .
COPY requirements.txt .
COPY src ./src
EXPOSE 8000
CMD ["uvicorn", "api_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
