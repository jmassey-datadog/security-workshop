FROM python

# copy over attack scripts
COPY ./ /opt/attacker

# install python requirements
RUN pip install -r /opt/attacker/requirements.txt

WORKDIR /opt/attacker/

# set command to run attack script
CMD python /opt/attacker/logins_attack.py