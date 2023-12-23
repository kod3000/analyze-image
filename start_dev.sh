#!/bin/bash

#  backend Start
echo "Starting Django backend..."
cd analyze_image
python manage.py runserver &
DJANGO_PID=$!
cd ..

#  frontend Start
echo "Starting Angular frontend..."
cd frontend
ng serve &
ANGULAR_PID=$!

# Wait for any process to exit
wait -n

# Kill the other process
kill $DJANGO_PID
kill $ANGULAR_PID
