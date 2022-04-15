## Launch WebApp

### 1 SPARQL endpoint
    
Make sure both .ttl files are in /SPARQL-endpoint/fuseki-docker/fuseki-data
- `politiquices.ttl`
- `wikidata_org.ttl.bz2`

      cd politiquices/SPARQL-endpoint
      make sparql

- Docker running: `fuseki-docker`

### 2 Launch Web server

    # might need to udpate the webapp/lib/config.py file
    cd politiquices/webapp
    make web

    # docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
  
- Docker running: `webapp`

    # without Docker
    check `lib/config.py`
    cd politiquices/webapp/webapp
    python generate_caches.py
    cp static/json/CHAVE-Publico_94_95.jsonl
    
    # flask dev-server
    cd webapp 
    python app/politiquices_app.py

    # nginx
    screen -SU
    cd /home/dsbatista/webapp/webapp

    sudo systemctl restart nginx

    # https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04
    
    # Runs on port 5000 as an example
    # PYTHONPATH=/home/dsbatista uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app
    
    # Runs on a local socket in production, with uWSGI application waiting for requests on the socket file
    PYTHONPATH=/home/dsbatista uwsgi -s myapp.sock -w wsgi:app --chmod-socket=666 --master --processes 6 --threads 1

    # nginx redirects http:80/443 to this local socket, config:
    /etc/nginx/sites-available/politiquices

    ufw firewall
 
    https://larsee.com/blog/2020/06/awstats-on-ubuntu-20-04-with-nginx/
    

    
    
    




