FROM infopen/ubuntu-xenial-ssh:0.1.0
MAINTAINER Alexandre Chaussier <a.chaussier@infopen.pro>

# Setting for packages installation
ENV DEBIAN_FRONTEND noninteractive

# Install openssh and lsb-release
RUN apt-get update && \
    apt-get install -y python2.7=2.7.11-7ubuntu1 \
                       python2.7-dev=2.7.11-7ubuntu1
