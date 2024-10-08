dev:
	docker build -t politiquices_webapp .
	docker run -p 5030:5030 -dit politiquices_webapp

web:
	. $${HOME}/politiquices_webapp_venv/bin/activate; \
	cd $${HOME}/politiquices/politiquices/webapp/webapp/app; \
	sudo PYTHONPATH=$${HOME}/politiquices uwsgi --socket 0.0.0.0:80 --protocol=http -w wsgi:app --master --processes 4 --threads 2 --stats 127.0.0.1:9191