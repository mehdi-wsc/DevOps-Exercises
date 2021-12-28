# DevOps-Exercises
DevOps Exercises 


The goal of this Exercises is to assess your capability to deploy on AWS using infrastructure as code and develop utilities to manage it.

It's divided in to 2 parts:
 * Deploy a system with a backend (using postgresql) and a fronted on kubernetes on AWS
 * Develop a tool to auto build and push docker images on updates

You are expected for commit your answer in the answers folder.

## Exercise 1 : Deploy on AWS
The development team did an API in Python and a Frontend in AureliaJS. The API is backed by a Postgresql database.

You are asked to deploy it on AWS with the following requirements :
 * Use kubernetes
 * Use infrastructure as code with terraform to deploy your resources on the cloud
 * Create scripts to ease management and help toward CI automation
 * Any SRE should be able to repeat the deployment process with your documentation

To go further (optional) you can:
 * Create a Gitlab CI file that would manage deployment
 * Add some monitoring
 * Automate applications deployment

You are free to use any cloud resource that is required.

### Guide
The applications to deploy can be found in the exercises/exercise1 folder. There is a backend and a frontend.

To help you understand how the system works, we have added a docker compose file that can be launched locally.

Further more, we added Dockerfiles to build the applications.

With docker compose, the API runs on port 5000, the database on port 5432 and the frontend on port 5001
The frontend needs the API public address at build time to call it.
This can be done by setting API_URL environment variable on build.
Database environment variables settings for backend can be found in the Readme of folder exercises/backend.

To test locally, you need to run in exercises/exercise1 folder
```
docker-compose up
```

## Exercise 2 : Docker images factory
We would like to maintain a library of docker images that can be used for tools or as base images for our developments.

We have chosen to do this in a single git repository where we can find all our Dockerfiles to build our base images.

In the git repository, each folder represents a docker image. Inside each folder, there is at least a Dockerfile and a manifest file that describes image name, image version and image repository address

An example of the git repository can be found in the folder exercises/exercise2.

You are asked to develop a tool in Python or Go to create a build factory with CI system.

To help you here are the expected development steps:
 * The application receives 2 commits sha1 as parameter
 * The first step is to get folders differences between these 2 commits to extract a list of image (folders) that changed
 * For each image that has changed, you need to read the manifest file to understand how you should name the image and where to push it
 * You are not required to build and push the image with docker

To go further (optional), you can add build and push image steps.
