FROM python:3.10

WORKDIR /srv

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
        ffmpeg

ADD ./requirements.txt /srv/requirements.txt

RUN pip install -r /srv/requirements.txt

ADD . /srv

CMD ["python", "run.py"]