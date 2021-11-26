FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY trackerdcs/ .

ENV PYTHONUNBUFFERED 1

# CMD [ "python", "dummy/hv.py", "hv", "mosquitto"]
