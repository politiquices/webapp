# start by pulling the python image
FROM python:3.9-alpine

# copy the requirements file into the image
COPY webapp/requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

ENV PYTHONPATH=/app

RUN python webapp/generate_caches.py

# configure the container to run in an executed manner
# ENTRYPOINT [ "/bin/sh" ]

EXPOSE 5030

CMD python webapp/app/politiquices_app.py