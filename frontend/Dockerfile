# build env
FROM node:21.7.1-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . ./
RUN npm run build
# CMD cp -r build result_build

# Эта команда запустит встроенный сервер на Node.js, который будет раздавать
# содержимое директории /app/build на порте 8000
CMD ["npx", "-y", "http-server", "-p", "8000", "/app/build"] 
