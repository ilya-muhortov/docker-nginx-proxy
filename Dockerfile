FROM python:3.12 AS python

RUN pip install --no-cache-dir Jinja2

WORKDIR /data

ADD apps.json generator.py ./
RUN python generator.py


FROM nginx:1.29 AS nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=python /data/stream.conf /etc/nginx/stream.conf
COPY --from=python /data/redirects.conf /etc/nginx/conf.d/redirects.conf

RUN echo "\ninclude /etc/nginx/stream.conf;" >> /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
