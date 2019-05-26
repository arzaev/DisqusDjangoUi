FROM python:3.7

COPY ./projectUI /projectUI

WORKDIR /projectUI

RUN pip install -r requirements.txt

COPY ./docker/python/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8007

