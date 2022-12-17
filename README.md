
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

## Problem statement

Navigation systems optimize for the shortest or fastest route. However, they do not consider elevation gain. Let’s say you are hiking or biking from one location to another. You may want to literally go the extra mile if that saves you a couple thousand feet in elevation gain. Likewise, you may want to maximize elevation gain if you are looking for an intense yet time-constrained workout. The high-level goal of this project is to develop a software system that determines, given a start and an end location, a route that maximizes or minimizes elevation gain, while limiting the total distance between the two locations to x% of the shortest path.

##  Steps to run the project.

### You can access our application in multiple ways:

#### 1. Using localhost

1. Clone our repo using ````git clone git@github.com:alokrkmv/project_EleNA.git````
2. Start the server using ````bash run.sh````
3. Once the server is up and running. Client can be accessed from ````src/main/client/index.html````

#### 2. Did someone say container!!!

We know docker is the new craze and to make sure that our application is machine independent we have a docker based solution for both our client and server hosted on docker hub. Follow the steps below to run the application using docker.
1. Make sure that you have docker installed
2. pull the docker server image using ````docker pull alokrkmv12/elena_server:0.3````
3. Start the docker server container using ````docker run -d -p 8000:8000 --name elena_server_container alokrkmv12/elena_server:0.3````
4. Docker server will be up and running on *localhost:8000*
5.  pull the docker client image using ````docker pull alokrkmv12/elena_client:0.1````
6. Start the docker client container using ````docker run -d -p 81:80 --name elena_client_container alokrkmv12/elena_client:0.1````
7. Docker client will be up and running on *localhost:81/index.html*

#### 3. Too much tech Jargans I just want to try the app!!!

Don't feel like setting up on local, just want to try our code!! Well we have got you covered. We have an entire cloud based solution for our application. Our entire application is hosted on cloud with our server hosted on heroku and client on Netlify.

To access our cloud based application just visit: ````https://sensational-squirrel-4f30da.netlify.app````

## Testing and evaluation

We have an exhaustive test suite for our application to make sure that our application is robust. We both unit test suite written using *pytest* and integration test suite using *postman test suite runner*

#### Unit test for server:

1. To run our unit test suite change your directory to ````src/main/server/test/unit_tests````
2. you can run the entire test suit using the bash file ````bash run_test_suit.sh````

#### Unit test results:

![Unit test result](https://github.com/alokrkmv/project_EleNA/tree/main/src/main/server/test/unit_tests/test_results)


#### Integration test for server:
Integration test for the server test the entire server at the API level. We are validating response body, status, madantory keys in response etc in our integration test.
1. To run our integration test suit import the postman collection inside ````src/main/server/test/integration_tests```` into postman 
2. Just send the post request through postman and test runner will automatically run all integration test cases.

#### Integration test results:

![Integration test result](https://github.com/alokrkmv/project_EleNA/blob/main/src/main/server/test/integration_tests/output.png)


## Why our EleNa

We know there are a lot of EleNas out there so why choose ours. Well we have some exclusive features for you.

-   We are calculating routes using two different algorithms, Dijkstra and A*, and then our algorithm picker chooses the most optimized route from the routes returned by the two algorithms.
    
-   We have integrated Google’s Place Autocomplete API to facilitate adding source and destination for the user and produce accurate results.
    
-   Our application is completely deployed on cloud with server being deployed on Heroku and front end being deployed on Netlify which enables anyone to use our EleNa with almost no hassle of application setup. You can acces the application here: [Application](https://sensational-squirrel-4f30da.netlify.app/) , apart from running it on local machines.
    
-   We have also deployed our application’s detailed documentation here: [Documentation](https://cute-donut-3ca29f.netlify.app/)
    
-   The application is also containerized to make it machine independent and easier to set up. The image is available here: [Docker Image](https://hub.docker.com/repository/docker/alokrkmv12/elena_server)
    
-   Our application is tested on a exhaustive test suit with more than 90% test coverage for our unit test and an integration test suit for api  level testing which ensures that our application is robust and reliable.
    

Our application is open source and code repository can be accessed here: [Github](https://github.com/alokrkmv/project_EleNA) 

### Documentations

1 ![functional_doc](https://cute-donut-3ca29f.netlify.app/)

2  ![design_doc](https://github.com/alokrkmv/lab-1-the_bazar/blob/main/src/Documentation/Design%20Doc.pdf)
  
3 ![user_doc](https://github.com/alokrkmv/project_EleNA/blob/main/Documentation/User_Manual.pdf)
  
4 ![evaluation_doc](https://github.com/alokrkmv/project_EleNA/blob/main/Documentation/Evaluation_Document.pdf)

5 ![Presentation](https://github.com/alokrkmv/project_EleNA/blob/main/Documentation/520%20Final%20Presentation.pptx)

6 ![Demo Video](https://github.com/alokrkmv/project_EleNA/blob/main/Documentation/Video_Demonstration.mp4)

    
  

