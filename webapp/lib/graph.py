from collections import defaultdict

from webapp.webapp.lib.cache import wiki_id_info
from webapp.webapp.lib.utils import get_short_name
from webapp.webapp.lib.sparql_queries import query_sparql


def get_entity_network_sparql(wiki_id, relation, freq_min, freq_max, year_from, year_to):

    if relation == "APOIA":
        rel_type_a = "ent1_supports_ent2"
        rel_type_b = "ent1_supports_ent2"

    if relation == "ACUSA":
        rel_type_a = "ent1_opposes_ent2"
        rel_type_b = "ent1_opposes_ent2"

    if relation == "ACUSA|APOIA":
        rel_type_a = "ent1_supports_ent2"
        rel_type_b = "ent1_opposes_ent2"

    query = f"""
    SELECT DISTINCT ?date ?rel_type ?ent1 ?arquivo_doc WHERE 
    {{
      ?rel politiquices:type ?rel_type;
           politiquices:ent1 ?ent1;
           politiquices:ent2 wd:Q1442096;
           politiquices:url ?arquivo_doc.
      ?arquivo_doc dc:title ?title ;
                   dc:date ?date . FILTER(YEAR(?date)>=1994 && YEAR(?date)<=2022)
      FILTER(?rel_type='{rel_type_a}' || ?rel_type='{rel_type_b}')
    }}
    ORDER BY DESC(?date)
    """

    results = query_sparql(query, "politiquices")

    edges = []
    nodes_in_graph = []
    edges_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    nodes_info = {}

    for x in results["results"]["bindings"]:
        date = x["date"]["value"]
        ent1_id = x["ent1"]["value"].split("/")[-1]
        ent2_id = x["ent2"]["value"].split("/")[-1]
        url = x["arquivo_doc"]["value"]
        relation = x["rel_type"]["value"]

        if ent1_id not in nodes_info:
            nodes_info[x["r"].start_node["id"]] = {
                "id": x["r"].start_node["id"],
                "label": get_short_name(x["s"]["id"], wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                },
            }

        edges_agg[relation][ent1_id][ent2_id] += 1

    # add main/central node
    nodes_info[wiki_id] = {
        "id": wiki_id,
        "label": get_short_name(wiki_id, wiki_id_info),
        "color": {
            "border": "#2B7CE9",
            "background": "#97C2FC",
            "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
        },
    }

    # filter nodes, include only those that are connected within the freq filter
    for rel_type, rels in edges_agg.items():
        for s, targets in rels.items():
            for t, freq in targets.items():
                if freq_min <= freq <= freq_max:

                    if "opposes" in rel_type:
                        rel_text = "opõe-se"
                        color = "#FF0000"
                        highlight = "#780000"
                    else:
                        rel_text = "apoia"
                        color = "#44861E"
                        highlight = "#1d4a03"

                    edges.append(
                        {
                            "from": s,
                            "to": t,
                            "id": len(edges) + 1,
                            "color": {
                                "color": color,
                                "highlight": highlight,
                            },
                            "scaling": {"max": 7},
                            "title": rel_text,
                            "value": freq,
                        }
                    )
                    nodes_in_graph.append(s)
                    nodes_in_graph.append(t)

    nodes = [node_info for node_id, node_info in nodes_info.items() if node_id in nodes_in_graph]

    return nodes, edges


def get_network_sparql(relation, year_from, year_to, freq_max, freq_min):

    if relation == "APOIA":
        rel_type_a = "ent1_supports_ent2"
        rel_type_b = "ent1_supports_ent2"

    if relation == "ACUSA":
        rel_type_a = "ent1_opposes_ent2"
        rel_type_b = "ent1_opposes_ent2"

    if relation == "ACUSA|APOIA":
        rel_type_a = "ent1_supports_ent2"
        rel_type_b = "ent1_opposes_ent2"

    query = f"""
        PREFIX politiquices: <http://www.politiquices.pt/>
        PREFIX      rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX        dc: <http://purl.org/dc/elements/1.1/>
        PREFIX 		 ns1: <http://xmlns.com/foaf/0.1/>
        PREFIX		 ns2: <http://www.w3.org/2004/02/skos/core#>
        PREFIX        wd: <http://www.wikidata.org/entity/>

        SELECT DISTINCT ?date ?rel_type ?ent1 ?ent2 ?arquivo_doc WHERE 
        {{
          ?rel politiquices:type ?rel_type;
               politiquices:ent1 ?ent1;
               politiquices:ent2 ?ent2;
               politiquices:url ?arquivo_doc.

          ?arquivo_doc dc:title ?title ;
                       dc:date ?date . FILTER(YEAR(?date)>={year_from} && YEAR(?date)<={year_to})
            FILTER(?rel_type='{rel_type_a}' || ?rel_type='{rel_type_b}')
        }}        
        """
    nodes_info = {}
    edges_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    results = query_sparql(query, "politiquices")

    for x in results["results"]["bindings"]:
        date = x["date"]["value"]
        ent1_id = x["ent1"]["value"].split("/")[-1]
        ent2_id = x["ent2"]["value"].split("/")[-1]
        url = x["arquivo_doc"]["value"]
        relation = x["rel_type"]["value"]

        if ent1_id not in nodes_info:
            nodes_info[ent1_id] = {
                "id": ent1_id,
                "label": get_short_name(ent1_id, wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                },
            }

        if ent2_id not in nodes_info:
            nodes_info[ent2_id] = {
                "id": ent2_id,
                "label": get_short_name(ent2_id, wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                },
            }

        edges_agg[relation][ent1_id][ent2_id] += 1

    # show only edges within: freq_min <= freq <= freq_max and nodes connected to these edges
    edges = []
    nodes_in_graph = []

    tmp_edges = defaultdict(list)
    bidirectional_edges = defaultdict(list)

    for rel_type, rels in edges_agg.items():
        for s, targets in rels.items():
            for t, freq in targets.items():
                if freq_min <= freq <= freq_max:

                    if "opposes" in rel_type:
                        rel_text = "opõe-se"
                        color = "#FF0000"
                        highlight = "#780000"
                    else:
                        rel_text = "apoia"
                        color = "#44861E"
                        highlight = "#1d4a03"

                    edges.append(
                        {
                            "from": s,
                            "to": t,
                            "id": len(edges) + 1,
                            "color": {
                                "color": color,
                                "highlight": highlight,
                            },
                            "scaling": {"max": 7},
                            "title": rel_text,
                            "value": freq,
                        }
                    )
                    nodes_in_graph.append(s)
                    nodes_in_graph.append(t)

                    # extract bi-directional relationship
                    tmp_edges[s].append(t)
                    if s in tmp_edges[t]:
                        bidirectional_edges[s].append(t)

    nodes = [node_info for node_id, node_info in nodes_info.items() if node_id in nodes_in_graph]

    return nodes, edges
