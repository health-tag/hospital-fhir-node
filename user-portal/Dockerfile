# stage1 as builder
FROM node:16.14.2-alpine as builder

# copy the package.json to install dependencies
COPY package.json package-lock.json ./

# Install the dependencies and make the folder
RUN npm install && mkdir /react-ui && mv ./node_modules ./react-ui

WORKDIR /react-ui

COPY . .

# Build the project and copy the files
RUN npm run build


FROM nginx:alpine

#!/bin/sh

# Uncomment this section for SSL
# RUN mkdir /etc/nginx/cert
# COPY ./dhparam.pem /etc/nginx/cert/dhparam.pem
# RUN chmod 400 /etc/nginx/cert/dhparam.pem
# COPY ./cert.pem /etc/nginx/cert/cert.pem
# COPY ./private.pem /etc/nginx/cert/private.pem

# Change nginx to nginx-https.conf in case using SSL
COPY ./nginx-http.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stahg 1
COPY --from=builder /react-ui/build /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]
