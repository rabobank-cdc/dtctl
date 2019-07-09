# Python 3.7 required
FROM python:3.7-alpine

# Install GCC (Needed for PyCryptoDomex)
RUN apk add build-base

# Add repository files to image
ADD . /opt/dtctl

# Switch to work directory
WORKDIR /opt/dtctl

# Install application
RUN python setup.py install

# Configure endpoint
ENTRYPOINT ["dtctl"]
