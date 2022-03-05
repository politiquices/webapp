## Launch WebApp

### 1 SPARQL endpoint
    
Make sure both .ttl files are in /SPARQL-endpoint/fuseki-docker/fuseki-data
- `politiquices.ttl`
- `wikidata_org.ttl.bz2`

      cd politiquices/SPARQL-endpoint
      make sparql

- Docker running: `fuseki-docker`

### 2 Neo4J endpoint:

    cd politiquices/neo4j
    make graph
    make neo4j

    # might need to udpate the config.py file
    sparql_endoint = "http://172.17.0.2:3030"

    # get ip address of the SPARQL container within the Docker network
    docker ps
    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER_ID

- Docker running: `neo4j`


### 3 Launch Web server

    # might need to udpate the webapp/lib/config.py file
    cd politiquices/webapp
    make web
  
- Docker running: `webapp`


    # without Docker
    cd politiquices/webapp/webapp
    python generate_caches.py
    cd webapp 
    python app/politiquices_app.py

    # ToDo: nginx
    screen -SU 

clear;PYTHONPATH=/home/dsbatista/politiquices uwsgi -s myapp.sock -w wsgi:app --chmod-socket=666 --master --processes 6 --threads 1


    # uwsgi -s myapp.sock -w wsgi:app --chmod-socket=666 --master --processes 6 --threads 1





