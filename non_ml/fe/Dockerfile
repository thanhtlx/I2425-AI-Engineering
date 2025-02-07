# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Expose port 3000
EXPOSE 3000
RUN npx update-browserslist-db@latest
# Run the app
CMD ["npm", "run", "dev","--", "--host"] 