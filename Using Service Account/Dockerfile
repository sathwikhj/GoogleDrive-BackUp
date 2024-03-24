FROM python
ENV TZ=Asia/Kolkata
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
COPY main.py /app/main.py
COPY credentials.json /app/credentials.json
WORKDIR /app
CMD ["python", "main.py"]
