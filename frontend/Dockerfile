# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app/frontend

# Copy package.json and install dependencies
COPY package.json /app/frontend

# Install Angular CLI globally
RUN npm install -g @angular/cli
RUN npm install -g @angular-devkit/build-angular --force

# Copy the current directory contents into the container
COPY . /app/frontend

RUN npm install

# Run tests
# RUN ng test --watch=false --browsers=ChromeHeadless

# Expose the port the app runs on
EXPOSE 4200

# Start the app
CMD ["ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
