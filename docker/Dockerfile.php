FROM php:8.2-fpm

# Install required dependencies
RUN docker-php-ext-install pdo pdo_mysql

# Set working directory
WORKDIR /var/www/html