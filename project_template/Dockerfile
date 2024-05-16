FROM python

ENV GOOGLE_APPLICATION_CREDENTIALS gcloud-creds.json
ENV TZ America/New_York

WORKDIR /app

COPY . .

RUN apt update && apt install -y libdbus-glib-1-2 chromium
RUN pip install -r requirements.txt
RUN playwright install firefox

CMD [ "python", "./main.py" ]