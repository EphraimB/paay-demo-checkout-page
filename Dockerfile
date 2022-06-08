FROM python:3.10.4

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it
EXPOSE 5000

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist

# Install any needed packages specified in requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install flask-mysql
RUN pip install cryptography

COPY . .

ENV FLASK_DEBUG 1

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]