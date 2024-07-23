FROM nvidia/cuda:12.5.1-runtime-ubuntu22.04

RUN apt update
RUN apt -yq install python3 python3-pip python-is-python3
RUN pip install tensorflow[with-cuda]
RUN pip install flask gunicorn

WORKDIR /root

EXPOSE 8080

CMD ["./entrypoint.sh"]
