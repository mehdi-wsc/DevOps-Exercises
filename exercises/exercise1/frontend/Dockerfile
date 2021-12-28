ARG API_URL=http://localhost:5000
FROM node:14
WORKDIR /src
COPY . / /src/
ENV API_URL=$API_URL
RUN npm install
RUN npm run build

FROM nginx
COPY --from=0 /src/dist /usr/share/nginx/html
