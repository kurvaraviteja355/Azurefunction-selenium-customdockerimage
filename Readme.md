# Python Azurefunction function with selenium using custom docker image 

The base Azure function does contain the necessary chrome or firefox packages to run the selenium to scrape the websites. This project gives an idea of how to create the custom docker image using selenium

## Prerequisites
* Docker Desktop
* Azure Container Registry
* Azure CLI(Optional)
* Azure function CLI
* Visual Studio 


## Create the custom docker image according to your requirements

Create the empty folder for project in required directory and open the Visual studio and select the Azure function CLI terminal
give the following command to create the docker file 


$ func init --docker
select the a worker runtime i.e. select the prefered language 
the command will create the docker file and some other requirement news 
$ func new 
name the function and select the type of the function that you required 
The project template is created, go to that directory and edit the docker file  and python file

## Build the docker image
build the docker image 
$ docker login
give the your credentials to login

$ docker build --tag <DockerID>/<imagename> .
This will build the docker image 

You can push the docker image to your Docker hub repo or Azure Container Registory
to docker hub
$ docker push <DockerID>/<imagename>
to Azure Conatiner container registry
$ docker -tag <Dockerid>/<imagename> <azureconatinerloginserver>/<imagename>
$ dcoker push <azureconatinerloginserver>/<imagename> 

## Create the Azure function with Docker container  with App Service plan not with consumption plan
After you creating the function open the function and select the Deployment setting, then select from where you can deploy the deploy the Custom docker image i.e either **Docker Hub** or **Azure container Registry** 

$Save the setting 
Now you successfully built and deployed the Azure function. Contragulations 







