#this docker file installs the pip and the dependencies for the project
#sudo docker build -f Dockerfile.full -t fintech-full . && sudo docker run --rm -p 8000:8080 --env-file .env fintech-full

FROM python:3.8-slim
WORKDIR /app
COPY req.txt .
#RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

COPY . .
EXPOSE 5000
CMD ["python", "dataRetrieval.py", "&&","python","data_analysis.py"]
