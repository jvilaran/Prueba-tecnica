# Usar una imagen de Node.js
FROM node:16

# Copiar los archivos de dependencias y luego instalar
COPY package.json package-lock.json ./
RUN npm install

# Copiar el resto del código de la aplicación
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Exponer el puerto del servidor de Vue (si usas `vite` o `webpack-dev-server`)
EXPOSE 8080

# Comando para correr el servidor de Vue.js
CMD ["npm", "run", "serve"]
