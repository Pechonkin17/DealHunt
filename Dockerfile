FROM python:3.12.8

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4999

CMD ["python", "app.py"]

# docker build -t steam-deals-app .
 #docker run -p 4999:4999 steam-deals-app