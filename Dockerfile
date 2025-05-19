FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt;
COPY main.py .
ENV TZ=Asia/Shanghai
ENV PYTHONPATH="/app:$PYTHONPATH"
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
