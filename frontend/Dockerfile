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
COPY ./nginx.config /etc/nginx/nginx.template
CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/nginx.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
COPY --from=builder /app/build /usr/share/nginx/html




# # так же берём готовый контейнер с node на основе alpine
# FROM node:18-alpine as build
# # Задаем рабочий каталог
# WORKDIR /app
# # Копируем туда наши json файлы
# ADD *.json ./
# # Устанавливаем все пакеты и зависимости указанные в json
# RUN npm install

# # Добавляем каталоги public и src.
# # можно воспользоваться командой COPY . . но если вы синхронизировали node_modules,
# # то будете ждать пока зальётся этот каталог целиком.
# # да и потом могут возникнуть проблемы.
# ADD ./public ./public
# ADD ./src ./src
