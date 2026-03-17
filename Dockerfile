FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=""
EXPOSE 7860

CMD ["streamlit", "run", "time_proj.py", "--server.port=7860", "--server.address=0.0.0.0"]
