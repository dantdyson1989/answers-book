FROM python:3.12-slim
WORKDIR /app
COPY answers.json ./
COPY index.html ./
COPY server.py ./
EXPOSE 8000
CMD ["python", "server.py"]
