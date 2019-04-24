# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?list ?listLabel WHERE {
?list wdt:P31 wd:Q13406463;
rdfs:label ?listLabel.
FILTER(LANG(?listLabel) = "[AUTO_LANGUAGE]").
FILTER(REGEX(STR(?listLabel), "list of UK top.+?singles in*", "i")).
}"""


def get_results(endpoint_url, query):
	sparql = SPARQLWrapper(endpoint_url)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()


results = get_results(endpoint_url, query)

print(results)

#for result in results["results"]["bindings"]:
#	print(result)