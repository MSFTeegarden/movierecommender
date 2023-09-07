FROM python:3.9
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . .
ENV OPENAI_ENDPOINT=https:<your-endpoint>
ENV OPENAI_KEY=<your-azure-openai-key>
ENV DEPLOYMENT_NAME=<your-deployment-name>
ENV MODEL_NAME=<your-model-name>
ENV REDIS_ENDPOINT=<your-redis-endpoint>
ENV REDIS_PASSWORD=<your-redis-password>
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
