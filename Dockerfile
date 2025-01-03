FROM python:3.8-slim
WORKDIR /app
COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "backend/app.py"]