FROM python:3.9
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . .
ENV OPENAI_ENDPOINT=https://ktopenaidemotest.openai.azure.com/
ENV OPENAI_KEY=5b6a98a19bb04816880cebb1759d4527
ENV DEPLOYMENT_NAME=text-embedding-ada-002
ENV MODEL_NAME=text-embedding-ada-002
ENV REDIS_ENDPOINT=redisopenaidemo.southcentralus.redisenterprise.cache.azure.net:10000
ENV REDIS_PASSWORD=UfDkt9EAtFpjogeeT3GDfCluBr9GrkfQuELHvjE8Gb4=
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]