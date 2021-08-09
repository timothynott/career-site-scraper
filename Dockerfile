ARG PYTHON_VERSION=3.9.5

###
# DEVELOPMENT IMAGE
#
# This image has no code baked in since the code will be mounted into it
# by docker-comopse.
###

FROM python:${PYTHON_VERSION} as development

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt ./
RUN pip install --timeout 1000 -r requirements.txt

ENV HOST=0.0.0.0 PORT=8080
EXPOSE ${PORT}

CMD exec gunicorn --bind $HOST:$PORT --workers 1 --threads 1 --timeout 0 main:app

###
# BUILDER IMAGE
#
# This builds upon the development image, adding code and doing whatever else
# is necessary to build the complete image.
###

FROM development as builder

COPY . ./
