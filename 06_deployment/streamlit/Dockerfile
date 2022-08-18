FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]

CMD ["nflpredictor.py"]0    