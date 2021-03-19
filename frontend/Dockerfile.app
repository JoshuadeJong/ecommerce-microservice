FROM python:3.9

WORKDIR /frontend

RUN mkdir app

COPY .env .env
COPY requirements.txt requirements.txt
COPY run.py run.py
COPY app/. app/.

# Install Requirements
RUN pip install -r requirements.txt

# Start application
ENV PYTHONPATH="/src:${PYTHONPATH}"
CMD ["python3", "run.py"]