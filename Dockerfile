FROM python:3.6

WORKDIR /app
ADD . .

ARG FIREFOX_URL=https://ftp.mozilla.org/pub/firefox/releases/55.0/linux-x86_64/en-US/firefox-55.0.tar.bz2
ARG GECKODRIVER_URL=https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz

RUN apt update && apt -y install curl bzip2 xvfb libpq-dev libxml2-dev libxslt1-dev libgtk-3-dev libdbus-glib-1-dev && \
    curl -L "$FIREFOX_URL" -o /tmp/firefox.tar.bz2 && \
    tar xvf /tmp/firefox.tar.bz2 -C /usr/local && \
    ln -s /usr/local/firefox/firefox /usr/bin/firefox && \
    curl -L "$GECKODRIVER_URL" -o /tmp/geckodriver.tar.gz && \
    tar xvf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    pip install uwsgi pipenv && \
    pipenv install --system && \
    apt -y remove bzip2 curl && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp* && \
    cd /app

# Define environment variable
ENV CLOCKWORK_API_KEY=645c8d6a6c154c4e40f236bf1470960e8127cb44
ENV LICENCE_NUMBER=AZIZ9912044AK9KB
ENV TEST_REF=40399533
ENV PHONE_NUMBER=07984780810

CMD bash
CMD python run.py