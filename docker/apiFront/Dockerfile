FROM nginx:alpine

# Copier la config nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copier le fichier HTML
COPY index.html /usr/share/nginx/html/

# Exposer le port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
