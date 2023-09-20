FROM node:18-alpine as builder
WORKDIR /app
ADD *.json ./
RUN npm install

ADD ./public ./public
ADD ./src ./src

RUN npm run build

FROM nginx:1.20.1-alpine
RUN apk --no-cache add curl
RUN curl -L https://github.com/a8m/envsubst/releases/download/v1.1.0/envsubst-`uname -s`-`uname -m` -o envsubst && \
    chmod +x envsubst && \
    mv envsubst /usr/local/bin
RUN mkdir -p /etc/nginx/conf.d/
COPY ./nginx.config /etc/nginx/nginx.template
RUN chown -R nginx:nginx /etc/nginx/conf.d/
CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/nginx.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
COPY --from=builder /app/build /usr/share/nginx/html