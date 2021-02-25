FROM python:3.9

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -U -r requirements.txt && python app/scripts/update.py

CMD ["python", "-u", "run.py"]