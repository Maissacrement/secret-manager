FROM alpine

COPY ./incron/ /etc
RUN apk update && apk add --no-cache incron 
