#!/bin/bash -xe

python3 create_book.py &

python3 delete_book.py &

python3 manage.py test

python3 manage.py runserver 0.0.0.0:9000
