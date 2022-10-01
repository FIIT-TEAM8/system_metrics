FROM python:3.9-alpine

WORKDIR /metrics_app

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 5005

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5005"]