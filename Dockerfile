From python:3.11
LABEL MAINTAINER = "Amir Lotfi | saelozahra.ir"
ENV PYTHONUNBUFFERED 1
run mkdir /movasat
WORKDIR /movasat
COPY . /movasat
ADD requirements.txt / movasat/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --no-input
CMD ["gunicorn" , "--chdir" , "movasat" , "--bind" , ":8004" , "movasat.wsgi:application"]