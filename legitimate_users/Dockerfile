FROM python

# copy over login scripts
COPY ./ /opt/login

WORKDIR /opt/login

# install python requirements
RUN pip install -r /opt/login/requirements.txt

# set command to run attack script
CMD python /opt/login/logins_legitimate.py