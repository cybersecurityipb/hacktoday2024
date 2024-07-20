FROM python:3.10-slim-buster

RUN groupadd -r nobody

WORKDIR /app    
COPY ./src /app
COPY ./flag /flag.txt
RUN pip3 install  --ignore-installed -r requirements.txt

USER nobody
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]