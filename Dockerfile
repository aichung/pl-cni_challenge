# Docker file for cni_challenge ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-cni_challenge .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-cni_challenge .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-cni_challenge
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-cni_challenge
#



FROM fnndsc/ubuntu-python3:latest
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/cni_challenge"
COPY ["cni_challenge", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["cni_challenge.py", "--help"]