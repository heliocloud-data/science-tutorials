FROM alpine:3
ARG PUBLIC_REPO=""

RUN mkdir -p /heliocloud/science-tutorials

COPY . /heliocloud/science-tutorials

RUN \
  if [ "${PUBLIC_REPO}" != "" ]; then \
    sed "s#url =.*#url = ${PUBLIC_REPO}#" -i /heliocloud/science-tutorials/.git/config ; \
    cat /heliocloud/science-tutorials/.git/config; \
  fi
