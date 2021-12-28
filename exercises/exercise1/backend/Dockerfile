FROM python:2.7.12

RUN apt-get update -y ; apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apache2 libapache2-mod-wsgi
RUN a2enmod wsgi

RUN mkdir /var/www/app
COPY . /var/www/app

RUN pip install -r /var/www/app/requirements.txt

RUN chown -R www-data:www-data /var/www/app

COPY apache.conf /etc/apache2/sites-available/api.conf
RUN a2ensite api

RUN rm -rf /etc/apache2/sites-available/000-default.conf
RUN rm -rf /etc/apache2/sites-enabled/000-default.conf

RUN service apache2 restart

EXPOSE 80

RUN apt-get clean

ENTRYPOINT ["/bin/bash", "/usr/sbin/apache2ctl", "-D", "FOREGROUND"]