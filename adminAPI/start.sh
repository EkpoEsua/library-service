#!/bin/bash -xe

python3 manage.py test

python3 borrow_book.py &

python3 register_user.py &

python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8000
