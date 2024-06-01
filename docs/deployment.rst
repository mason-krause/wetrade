.. _deployment:

==================================
Deploying your ``wetrade`` app
==================================

Because of the flexibility and portability it provides, we recommended 
deploying ``wetrade`` applications with Docker, and we've included some 
information to make this as easy as possible for people without previous Docker
experience. 

++++++++++++++++++++++++++++++++++++++
Editing your Dockerfile
++++++++++++++++++++++++++++++++++++++

If you created your application using the *new-project* script detailed in 
:ref:`getting_started`, you'll see a *Dockerfile* file in your app directory. 
This file details the configuration of your Docker image may look something 
like this:

**Dockerfile**

.. code-block:: dockerfile

  FROM python

  ENV GOOGLE_APPLICATION_CREDENTIALS gcloud-creds.json
  ENV TZ America/New_York

  WORKDIR /app

  COPY . .

  RUN apt update && apt install -y libdbus-glib-1-2 chromium
  RUN pip install -r requirements.txt
  RUN playwright install firefox

  CMD [ "python", "./main.py" ]

Walking through the file, we're first starting with Docker's preconfigured python
image. We're then setting a couple environment variables to set our Google Cloud
credentials path and specify we're in Eastern Standard Time. From there, we're 
setting the '/app' directory as our main directory and copying our application 
code into this location (our WORKDIR). We're then installing our dependencies 
and setting **python ./main.py** (our application entry point) as the command 
to run when starting our Docker image.

This template provides a starting point for Dockerizing a ``wetrade`` app, and
You can modify these settings based on the needs of your application,

++++++++++++++++++++++++++++++++++++++
Building a Docker Image
++++++++++++++++++++++++++++++++++++++

After you've set up your Dockerfile, you can build an image with the *docker 
build* command:

.. code-block:: shell

  docker build -t your-image-name .

++++++++++++++++++++++++++++++++++++++
Running a Docker Image
++++++++++++++++++++++++++++++++++++++

After creating your image, you can run your image using the *docker run*
command:

.. code-block:: shell

  docker run your-image-name

If you're running your program daily, you can set up a recurring task to run
your docker image each morning. 

++++++++++++++++++++++++++++++++++++++
Other info
++++++++++++++++++++++++++++++++++++++

---------------------------------------------------
Fun with Docker Compose
---------------------------------------------------

After you've set up your Dockerfile, you can a companion tool called **docker 
compose** to run multiple trading accounts with a single command. 

You'll first need to create a simple *docker-compose.yml*

**docker-compose.yml**

.. code-block:: yaml

  services:
    my-first-account:
      container_name: my-first-account
      image: your-image-name
    my-second-account:
      container_name: my-second-account
      image: another-image

Then you can build all your images with one command:

.. code-block:: shell

  docker compose -f docker-compose.yml build

And run these accounts together on your preferred schedule:

.. code-block:: shell

  docker compose -f docker-compose.yml up

You can also run your docker compose in detached mode and access your terminal
output with Docker logging:

.. code-block:: shell

  docker compose -f docker-compose.yml up -d

---------------------------------------------------
Docker logging
---------------------------------------------------

By default Docker logs will hold on to all of the terminal output (stdout) 
of your containers indefinitely or until you choose to manually clear them 
out. The example below demonstrates how you can access the logs for a specific
container over a specific time period. 

.. code-block:: shell

  docker logs --since=2024-04-10T13:00:00 --until=2024-04-10T14:00:00 my-first-account

As you can tell, this isn't the most user friendly method for reviewing logs,
but it doesn't require any configuration and can help keep track of exceptions
that you're unable to catch manually. For more comprehensive logging, we
recommend using :ref:`Google Cloud <gcloud>`.