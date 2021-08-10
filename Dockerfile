ARG PYTHON_VERSION=3.9.5

###
# DEVELOPMENT IMAGE
#
# This image has no code baked in since the code will be mounted into it
# by docker-comopse.
###

FROM python:${PYTHON_VERSION} as development

###
# BUILDER IMAGE
#
# This builds upon the development image, installs modules, builds the code,
# and runs the main script.
###

FROM development as builder

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --timeout 1000 -r requirements.txt

COPY . ./

CMD [ "python3", "main.py" ]

