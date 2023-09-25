# Usage

Here are the main instructions for using the `agromap_backend` application.

## Setting environment variables

To work correctly, you need to configure the following environment variables in the `.env` file:

Fill in `Your Value` with the appropriate values you want to use for each variable.

```shell
   POSTGRES_DB=POSTGRES_DB
   POSTGRES_USER=POSTGRES_USER
   POSTGRES_PASSWORD=POSTGRES_PASSWORD
   POSTGRES_HOST=POSTGRES_HOST
   POSTGRES_PORT=POSTGRES_PORT
   ALLOWED_HOSTS=ALLOWED_HOSTS
   SECRET_KEY=SECRET_KEY
   SCI_HUB_USERNAME_V2=username_dataspace_copernicus
   SCI_HUB_PASSWORD_V2=password_dataspace_copernicus
   CSRF_TRUSTED_ORIGINS=CSRF_TRUSTED_ORIGINS
   KAFKA_HOST_PORT=ip_address:port
   USERNAME_GEOSERVER=USERNAME_GEOSERVER
   PASSWORD_GEOSERVER=PASSWORD_GEOSERVER
   URL_GEOSERVER=URL_GEOSERVER
   KAFKA_HOST_PORT=ip_address:port
   VET_SERVICE_URL=VET_SERVICE_URL
```

## Starting the application

1. First, you should clone the repository to your machine. If you haven't done this yet, execute the following command:
    ```
    git clone https://github.com/giprozem/AgroMap.git
    ```

2. Navigate into the project folder:

    ```
    cd backend
    ```

3. Run Docker Compose:

    ```
    docker-compose up -d --build
    ```

   This will start all necessary services listed in your `docker-compose.yml`, including your Django app, PostGIS
   database, and others.

## Working with the application

1. To enter the application, open a web browser and navigate to `http://localhost:8111`.

2. Here, you will find your application interface and you can begin to work.


## Launch unit tests:

1. Run command:

    ```
    docker compose exec web coverage run manage.py test
    ```

2. Tests' report:

    ```
    docker compose exec web coverage report -i
    ```
