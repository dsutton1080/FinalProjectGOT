FROM mariadb:latest
ENV MYSQL_ROOT_PASSWORD='password'
RUN mkdir /setup && cd /setup
COPY . /setup
# CMD sleep 15 && \
#     cat /setup/scripts/* > script.sql && \
#     mysql -h 127.0.0.1 -uroot -ppassword < script.sql
