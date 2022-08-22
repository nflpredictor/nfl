FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]

CMD ["nflpredictor_vab.py"]