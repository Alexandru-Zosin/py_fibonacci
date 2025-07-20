requirements.txt -> Python dependencies
Dockerfile -> How to build image
docker-compose.yaml -> How to orchestrate multiple containers
* the image is already defined by oracle-xe
a container is built off an image
-------------------------
Kernel/Operating System: You can have a Windows host and container which uses 
an image with a Linux (like Ubuntu 22) base but a Python virtual environment uses 
the host operating system. The only thing a Python venv isolates is itself:
 Python (pip and stuff).

- also, there is MORE than just Python dependencies. A docker encapsulates the 
entire OS. (With a Docker image, you can swap out the entire OS -
 install and run Python on Ubuntu, Debian, Alpine, even Windows Server Core.
There are Docker images out there with every combination of OS and Python versions
 you can think of, ready to pull down and use on any system with Docker installed.)

Network Setup: A Docker container is isolated and will, by default, 
not be able to access other containers and other things in the "real" network. 
A Python virtual environment can since it's just like a regular but isolated
 folder for a project.

---
Best practice:
- we NEVER share .venv with teammates. What WE DO is share
packages you have installed and they install it for their environments  
Containers (docker ones) are a good solution to this.

Virtual environments bake in absolute paths and OS-specific binaries,
 so they break on a colleague’s machine or CI runner.


1. requirements.txt: packages & versions
2. Dockerfile: python version, file mounts, networking
3. Makefile: build & run of the docker container, passing environment variables

- a single Dockerfile... but with a caveat*
- everyone clones from github and copy . to add app's code and dependencies 
into the container
- every developer runs their own instance of the database,
in isolation from any other developer's concurrent hacking (local sandbox)
----
*
We asked ourselves if we should use Docker when we can work with virtual environments,
but this answer:

"   For me, I enjoy the fact that I don't have to install apache,
mysql, mongodb, nginx, oracle, etc on my laptop to work different projects.
I just write a docker-compose file and spin it up and I have an entire environment
(usually a replicate of my current client's production environment, and if not, 
it will be their environment because I can just pass the containers to them).

    And when I am done, I just turn it off and I don't have all those apps installed
that I may never use again." 

made us do it and just modify to mount the code locally when developing.


--- In essence, the dockerfile should only change between dev/prod from the pov of
mounting the code locally or not.

"you definitely want to have only one dockerfile for both/all environments 
(dev,qa,stg,etc). Separate dockerfiles is a bad practice. 
If you are mounting your code locally when developing, that's fine.

Have the dockerfile COPY your app code to it's destination and ship that to your 
registry once built. For local development you'll run that same container 
image with the addition of args/config to mount your local code, superseding 
the code the COPY command added in."