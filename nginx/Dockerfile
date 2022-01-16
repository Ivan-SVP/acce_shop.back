FROM nginx:mainline as base

# set www-data group to nginx give permission to app.socket
RUN usermod -a -G www-data nginx
