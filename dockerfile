FROM postgres:lastest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=coffeeandtv
ENV POSTGRES_DB=GTJ_GO

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432