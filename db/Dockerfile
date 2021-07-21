
FROM mysql
WORKDIR /db_dump
#copying db dump to restore it later
COPY ./f1db.sql /db_dump/
#root password will be randomly generated at the start and printed to stdout
ENV MYSQL_RANDOM_ROOT_PASSWORD=yes
# ENV MYSQL_ROOT_PASSWORD=sperma15
#database created at the start, will be later used to restore from dump
ENV MYSQL_DATABASE=f1
#user with superuser access to previously generated db
ENV MYSQL_USER=django_f1
#default password for previously generated user
ENV MYSQL_PASSWORD=dupadupa##
#informs that those ports should be exposed during runtime eg. "-p 3308:3306"
EXPOSE 3306 33060
