# ToDo: need to get IP dynamically
sparql_endoint = "http://172.17.0.2:3030"
neo4j_endpoint = "bolt://172.17.0.3:7687"
# sparql_endoint = "http://0.0.0.0:3030"
# neo4j_endpoint = "bolt://0.0.0.0:7687"
wikidata_endpoint = f"{sparql_endoint}/wikidata/query"
politiquices_endpoint = f"{sparql_endoint}/politiquices/query"
live_wikidata = "https://query.wikidata.org/sparql"
ps_logo = "/static/images/Logo_do_Partido_Socialista(Portugal).png"
no_image = "/static/images/no_picture.jpg"
static_data = "app/static/json/"
entities_batch_size = 16    # number of entity cards to read in batch when scrolling down
