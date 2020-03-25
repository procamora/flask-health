FROM python:3.7-alpine@sha256:6787773ef4c6f728e82efd591d605e04e2b38ebcf39bf42da8d2b12527caa65b

COPY requirements.txt /root
COPY health.py /root

WORKDIR /root

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "-u", "health.py"] 
