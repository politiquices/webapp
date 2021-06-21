env:
	# create the python venv
	python3.8 -m venv $${HOME}/politiquices_webapp_venv; . $${HOME}/politiquices_webapp_venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r webapp/requirements.txt; \


cache:
	. $${HOME}/politiquices_webapp_venv/bin/activate; \
	cd $${HOME}/politiquices/webapp/; \
	PYTHONPATH=$${HOME}/politiquices python webapp/generate_caches.py;


dev:
	. $${HOME}/politiquices_webapp_venv/bin/activate; \
	cd $${HOME}/politiquices/webapp/webapp/app; \
	PYTHONPATH=$${HOME}/politiquices FLASK_ENV=development python politiquices_app.py


web:
	. $${HOME}/politiquices_webapp_venv/bin/activate; \
	cd $${HOME}/politiquices/politiquices/webapp/webapp/app; \
	sudo PYTHONPATH=$${HOME}/politiquices uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app --master --processes 4 --threads 2 --stats 127.0.0.1:9191


neo4j:
	. $${HOME}/politiquices_webapp_venv/bin/activate; \
	cd $${HOME}/politiquices/webapp/neo4j_import; \
	PYTHONPATH=$${HOME}/politiquices python compute_graph_metrics.py;

	docker run -dit -p 127.0.0.1:7474:7474 -p 127.0.0.1:7687:7687 -v $${HOME}/politiquices/webapp/neo4j_import/:/var/lib/neo4j/import -e NEO4J_AUTH=neo4j/s3cr3t -e NEO4J_dbms.connector.bolt.address=127.0.0.1::7687 neo4j
	sleep 40s;
	docker exec -ti $$(docker ps | grep 'neo4j' | awk '{ print $$1 }') /var/lib/neo4j/bin/cypher-shell -u neo4j -p s3cr3t -f /var/lib/neo4j/import/load_data.cql
