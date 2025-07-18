# SneakerPedia

## Overview

Sneakerpedia is a portfolio project built using a 'traditional' Django stack. It serves as a web application to archive and display sneakers and their related information, such as brand, designer, and release year. The project demonstrates core Django skills, including models, views, templates, user authentication, API design and testing.

![Screenshot of Homepage](./.github/images/snp_home-min.png)

![Screenshot of Detail Page](./.github/images/snp_detail-min.png)

## Stack
- Django
- Django Rest Framework
- Tailwind
- Alpine JS

## API

The project includes an API, that allows access to sneaker data via a GET request. The docs can be viewed at http://127.0.0.1:8000/api/schema/redoc/ when the project is running.


## Local Development Setup

1.  Clone the repo, and cd into it:

    ```shell
    $ git clone <repo-url>
    $ cd <path/to/repo>
    ```

2.  Ensure you have docker installed, and that it is running.
3.  Add environment variables for the following:
    * `SECRET_KEY` (Secret key used by Django)
    * `DJANGO_DEBUG` (set to `True` for development)

    For production, you'll also want to add the relevant variables for your database and email provider, which are used when `DEBUG` is set to `False` (see settings).

4.  Build and start up the local server:

    ```shell
    $ docker-compose up --build
    ```

5.  Apply migrations to the database:

    ```shell
    $ docker-compose exec web python manage.py migrate
    ```

6.  Create a superuser:

    ```shell
    $ docker-compose exec web python manage.py createsuperuser
    ```

7.  Navigate to http://127.0.0.1:8000/ in your browser.

## Seed Data

The project includes a management command to populate the database with initial seed data.

1.  **Download Seed Images:** Download the required sneaker images.
2.  **Place Images:** Unzip and place the images into the `media/seed_images/` directory at the project root.
3.  **Run Seed Script:** Execute the following command to run the seed script. This will populate the brands and sneakers from the provided CSV file and link them to the images.
    ```shell
    $ docker-compose exec web python manage.py seed_data
    ```

## Tests

To run the test suite:

```shell
$ docker-compose exec web python manage.py test
```