FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY dummy/ .
COPY sensors/ .

ENV PYTHONUNBUFFERED 1

# CMD [ "python", "dummy/hv.py", "hv", "mosquitto"]
