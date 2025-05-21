# Dockerfile
FROM node:18-alpine

# Install JSON-Server globally
RUN npm install -g json-server

# Create & set working directory inside container
WORKDIR /data

# Copy your mock data in
COPY db.json /data/db.json

# Expose JSON-Server’s default port
EXPOSE 3000

# Launch JSON-Server watching your db.json
CMD ["json-server", "--watch", "/data/db.json", "--port", "3000"]

