# FROM python:3.12-alpine
# RUN pip install --upgrade pip
# ENV PYTHONUNBUFFERED=1
# WORKDIR /python-app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# CMD ["python", "main.py"]
# ENTRYPOINT ["python", "main.py"]

FROM python:3.12-slim
RUN groupadd -r groupflask && useradd -r -g groupflask userflask
RUN pip install --upgrade pip
RUN pip install flask
WORKDIR /app
COPY ./flaskprj .
EXPOSE 4000
USER userflask
VOLUME /app
CMD ["python", "main.py"]
