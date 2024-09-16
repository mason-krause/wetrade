FROM python

ENV GOOGLE_APPLICATION_CREDENTIALS gcloud-creds.json
ENV TZ America/New_York

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN playwright install --with-deps firefox

CMD [ "python", "./main.py" ]