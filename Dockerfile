FROM mcr.microsoft.com/devcontainers/python:3.8

RUN pip install tensorflow tensorflowjs keras flask gunicorn
RUN pip install tensorflow_addons

WORKDIR /home/vscode

EXPOSE 8080

CMD ["./entrypoint.sh"]
