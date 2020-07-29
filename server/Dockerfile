FROM python
COPY ./ /var/www/
WORKDIR /var/www/
RUN pip install -r /var/www/requirements.txt
CMD python /var/www/routes.py