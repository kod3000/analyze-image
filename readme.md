
## Analyze Image Proof of Concept



The following project is a fullstack application that
allows users to upload images and gives them analysis on the image
by leveraging OpenAI's Vision Preview API.

The project is built using the following technologies:

- Angular 14 with Angular Material and Tailwind CSS
- Django 5.0
- Docker


To run the application locally, you will need to have docker installed.

# To install docker

    https://docs.docker.com/get-docker/

Once docker is installed, you can run the following command to build the application

# To run 
    
    
    docker-compose up

# To Access the application

Once docker is running, you can access the frontend and backend using the following urls

        // frontend
        http://localhost:8484/

        // backend
        http://localhost:8484/api/health/status


# Developer Notes


## Frontend

The frontend is originally meant to be an admin dashboard for the app.

This way there is an overview of all the images that have been uploaded,
with the accompanying analysis.

Furthermore, the frontend should allow the admin user to rate
the analysis as correct or incorrect.

This way, the admin user can train the model to be more accurate.

Other things to note about the frontend:

- currently the frontend is building as dev, not prod

The Angular frontend can be built for development using the following command

    ng serve

*more information is available in the frontend readme file*


----


## Backend


The backend is a simple Django application that exposes a REST API


Some things to note about the backend:

- a rate limit should be implemented to prevent abuse via gateway api
- the api should be secured with a token (this was not done due to time constraints)


The backend can be run using the following command

    python manage.py runserver

*more information is available in the backend readme file*