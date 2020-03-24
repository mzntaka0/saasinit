FROM nginx
RUN rm -f /etc/nginx/conf.d/*

ADD drf.conf /etc/nginx/conf.d/drf.conf
ADD uwsgi_params /etc/nginx/uwsgi_params
ADD nginx.conf /etc/nginx/nginx.conf
ADD mime.types /etc/nginx/mime.types

CMD /usr/sbin/nginx -g 'daemon off;' -c /etc/nginx/nginx.conf
