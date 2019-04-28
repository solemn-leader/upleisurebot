# base imageIt seems that docker (1.12.0-rc3-beta18) is using an instance of postgres for something (I killed the service and it forced docker to restart). To fix it, I changed my docker-compose ports section from 5432:5432 to just 5432 and let docker choose the port automatically.


FROM python:3.7
# tell terminal not to use buffer
ENV PYTHONUNBUFFERED 1
# create base directory
RUN mkdir /bot
# set working directory
WORKDIR /bot
# add code to working directory
ADD . /bot/
# install all necessary dependencies
RUN pip install -r requirements.txt
# run tests and main file
CMD bash -c "./start.sh"