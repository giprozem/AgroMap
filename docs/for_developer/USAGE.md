# Usage

Here are the main instructions for using the `agromap_backend` application.

## Setting environment variables

To work correctly, you need to configure the following environment variables in the `.env` file:

Fill in `Your Value` with the appropriate values you want to use for each variable.

```shell
    POSTGRES_DB=Your Value
    POSTGRES_USER=Your Value
    POSTGRES_PASSWORD=Your Value
    POSTGRES_HOST=Your Value
    POSTGRES_PORT=Your Value
    ALLOWED_HOSTS=Your Value
    SECRET_KEY=Your Value
    SCI_HUB_USERNAME_V2=Your Value
    SCI_HUB_PASSWORD_V2=Your Value
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
