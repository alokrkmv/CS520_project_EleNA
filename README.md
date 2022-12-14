# project_EleNA

Problem Statement:

The application provides an optimized path between a source and destination taking the users elevation preference into consideration. The application is espically useful for hikers and bikers to whom elevation of the path is of prime importance while chosing a path for travelling.

Architecture:
The application is structured as a client-server architecture.

  Client functionality: 
  - Accept source, desitination, elevation preference, maximum alloweable deviation from shortest path.
  - Render a visually appealing map on the UI marking the most optimized path between the source and destination.
  
  Server functionality:
  - Convert the source and destination to Latitudes and Longitudes representation for further processing along with elevation information.
  - Generating a map involviding the source, destination and their genographic neighbourhood.
  - Using above inputs to determine the optimized path and returning a unique path with associated details.


Docker commands

docker image build -t elena_image .

docker run -d -p 8000:8000 --name elena_container elena_image

docker pull alokrkmv12/elena_image:latest