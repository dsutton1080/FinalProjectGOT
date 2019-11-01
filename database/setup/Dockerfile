FROM mariadb:latest
ENV MYSQL_ROOT_PASSWORD='password'
RUN mkdir /setup && cd /setup
COPY . /setup
CMD until nc -z 127.0.0.1 3306; do echo "Waiting for DB"; done && \
    cat /setup/scripts/* > script.sql && \
    mysql -h 127.0.0.1 -u root -p 'password' < script.sql
