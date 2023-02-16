FROM python:3.10

WORKDIR /oc_lettings

ENV DEBUG=False
ENV PORT=8000

ADD . /oc_lettings

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /oc_lettings

EXPOSE 8000

CMD gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT