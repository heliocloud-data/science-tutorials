FROM alpine:3
ARG PUBLIC_REPO=""
ARG BRANCH=""

RUN apk add git

RUN mkdir -p /heliocloud/science-tutorials

COPY . /heliocloud/science-tutorials

RUN \
  if [ "${PUBLIC_REPO}" != "" ]; then \
    sed "s#url =.*#url = ${PUBLIC_REPO}#" -i /heliocloud/science-tutorials/.git/config ; \
    if [ "${BRANCH}" != "" ]; then \
      cd /heliocloud/science-tutorials && git pull origin ${BRANCH} ; \
    fi; \
    cat /heliocloud/science-tutorials/.git/config; \
  fi
