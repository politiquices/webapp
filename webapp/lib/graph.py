from collections import defaultdict

from lib.cache import wiki_id_info
from lib.neo4j_connect import Neo4jConnection
from lib.utils import get_short_name
from lib.config import neo4j_endpoint


def query_neo4j(query):
    conn = Neo4jConnection(uri=neo4j_endpoint, user="neo4j", pwd="s3cr3t")
    results = conn.query(query)
    conn.close()
    return results


def get_entity_network(wiki_id, relation, freq_min, freq_max, year_from, year_to):
    """
    Get the network up to 'max_hops' for a given entity
    """

    query = f"MATCH (s)-[r:{relation}]->(p:Person {{id:'{wiki_id}'}}) " \
            f"WHERE r.data >= date('{year_from}-01-01') " \
            f"AND r.data <= date('{year_to}-12-31') " \
            f"RETURN s, r, p"
    results = query_neo4j(query)

    edges = []
    nodes_in_graph = []
    edges_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    nodes_info = {}

    # get all nodes and count freq. relationships
    for x in results:
        if x['r'].start_node['id'] not in nodes_info:
            nodes_info[x['r'].start_node['id']] = {
                "id": x['r'].start_node['id'],
                "label": get_short_name(x["s"]["id"], wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                }
            }

        edges_agg[x["r"].type][x["r"].start_node["id"]][x["r"].end_node["id"]] += 1

    # add main/central node
    nodes_info[wiki_id] = {
        "id": wiki_id,
        "label": get_short_name(wiki_id, wiki_id_info),
        "color": {
            "border": "#2B7CE9",
            "background": "#97C2FC",
            "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"}
        }}

    # filter nodes, include only those that are connected within the freq filter
    for rel_type, rels in edges_agg.items():
        for s, targets in rels.items():
            for t, freq in targets.items():
                if freq_min <= freq <= freq_max:
                    if rel_type == "ACUSA":
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

    nodes = [node_info for node_id, node_info in nodes_info.items()
             if node_id in nodes_in_graph]

    return nodes, edges


def get_network(relation, year_from, year_to, freq_max, freq_min):

    query = f"MATCH (s)-[r:{relation}]->(t) " \
            f"WHERE r.data >= date('{year_from}-01-01') AND r.data <= date('{year_to}-12-31') " \
            f"RETURN s, t, r"

    results = query_neo4j(query)

    # build the nodes structure to pass to vis js network replacing the edges with the frequency
    nodes_info = {}
    edges_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for x in results:
        if x["s"].id not in nodes_info:
            nodes_info[x["s"]["id"]] = {
                "id": x["s"]["id"],
                "label": get_short_name(x["s"]["id"], wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                },
            }
        if x["t"].id not in nodes_info:
            nodes_info[x["t"]["id"]] = {
                "id": x["t"]["id"],
                "label": get_short_name(x["t"]["id"], wiki_id_info),
                "color": {
                    "border": "#2B7CE9",
                    "background": "#97C2FC",
                    "highlight": {"border": "#2B7CE9", "background": "#D2E5FF"},
                },
            }
        edges_agg[x["r"].type][x["r"].start_node["id"]][x["r"].end_node["id"]] += 1

    # filter to show only edges within: freq_min <= freq <= freq_max
    # and nodes connected to these edges
    edges = []
    nodes_in_graph = []

    tmp_edges = defaultdict(list)
    bidirectional_edges = defaultdict(list)

    for rel_type, rels in edges_agg.items():
        for s, targets in rels.items():
            for t, freq in targets.items():
                if freq_min <= freq <= freq_max:

                    if rel_type == "ACUSA":
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

    """
    # build a networkx structure to: compute pagerank, compute communities, etc.
    networkx_nodes = []
    networkx_edges = []
    for node, other in bidirectional_edges.items():
        for n in other:
            networkx_edges.append((node, n))

    for edge in networkx_edges:
        networkx_nodes.append(edge[0])
        networkx_nodes.append(edge[1])

    g = nx.Graph()
    g.add_nodes_from(networkx_nodes)
    g.add_edges_from(networkx_edges)

    # set node size as the value of the pagerank
    page_rank_values = nx.pagerank(g)
    for k, v in page_rank_values.items():
        for node in nodes:
            if node["id"] == k:
                node["value"] = 1.0
    """

    return nodes, edges