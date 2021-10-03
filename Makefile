web:
	docker build -t politiquices_webapp .
	docker run -p 5000:5000 -it politiquices_webapp
