FROM node:latest AS frontend-build

WORKDIR /build

COPY . .

RUN npm install
RUN npm run build 

FROM nginx:alpine

WORKDIR /app

COPY --from=frontend-build /build/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN apk update --no-cache && apk add --no-cache ca-certificates

EXPOSE 80

ENTRYPOINT [ "nginx", "-g", "daemon off;" ]

