
"""
SELECT ?p (SAMPLE(?t) as ?type) (COUNT(?p) as ?c) (SAMPLE(?z) as ?samp) 
WHERE {
    <http://vivo.brown.edu/individual/org-brown-univ-dept3> ?p ?o .
    OPTIONAL {?p a ?t .}
    BIND(IF(isURI(?o), ?o, "") as ?z)
}
GROUP BY ?p
ORDER BY ?type DESC(?c)
"""

import sys
import requests
import config.development as config

faculty = [
    'http://vivo.brown.edu/individual/khansenm',
    'http://vivo.brown.edu/individual/embrown',
    'http://vivo.brown.edu/individual/jpipher',
    'http://vivo.brown.edu/individual/lbrownmd',
    'http://vivo.brown.edu/individual/etollmd',
    'http://vivo.brown.edu/individual/jvandenb',
    'http://vivo.brown.edu/individual/bgenberg',
    'http://vivo.brown.edu/individual/mhohenha',
    'http://vivo.brown.edu/individual/eterrymo',
    'http://vivo.brown.edu/individual/aplette',
    'http://vivo.brown.edu/individual/rarenber',
    'http://vivo.brown.edu/individual/cfaulkne',
    'http://vivo.brown.edu/individual/mklitzke',
    'http://vivo.brown.edu/individual/jdibened',
    'http://vivo.brown.edu/individual/cvillarr',
    'http://vivo.brown.edu/individual/scohenmd',
    'http://vivo.brown.edu/individual/mhillstr',
    'http://vivo.brown.edu/individual/mdasilva',
    'http://vivo.brown.edu/individual/cjsammar',
    'http://vivo.brown.edu/individual/lsnadymc',
    'http://vivo.brown.edu/individual/pruberto',
    'http://vivo.brown.edu/individual/jkuzner',
    'http://vivo.brown.edu/individual/pharropm',
    'http://vivo.brown.edu/individual/ss74',
    'http://vivo.brown.edu/individual/cn8',
    'http://vivo.brown.edu/individual/rbhatt',
    'http://vivo.brown.edu/individual/dnickel',
    'http://vivo.brown.edu/individual/awebb',
    'http://vivo.brown.edu/individual/efwalsh',
    'http://vivo.brown.edu/individual/ll7',
    'http://vivo.brown.edu/individual/kmonchik',
    'http://vivo.brown.edu/individual/ewittels',
    'http://vivo.brown.edu/individual/egartman',
    'http://vivo.brown.edu/individual/ljrubinm',
    'http://vivo.brown.edu/individual/ffenghi',
    'http://vivo.brown.edu/individual/rpadilla',
    'http://vivo.brown.edu/individual/elaposat',
    'http://vivo.brown.edu/individual/ccarpent',
    'http://vivo.brown.edu/individual/rbungiro',
    'http://vivo.brown.edu/individual/sschenna',
    'http://vivo.brown.edu/individual/wc53',
    'http://vivo.brown.edu/individual/ac184',
    'http://vivo.brown.edu/individual/mapomera',
    'http://vivo.brown.edu/individual/gdk',
    'http://vivo.brown.edu/individual/mfaganmd',
    'http://vivo.brown.edu/individual/nlawandy',
    'http://vivo.brown.edu/individual/dchronle',
    'http://vivo.brown.edu/individual/rwestlak',
    'http://vivo.brown.edu/individual/rpendse',
    'http://vivo.brown.edu/individual/nkouttab'
]

# orgs = [
#     'http://vivo.brown.edu/individual/org-brown-univ-dept70',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept602',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept604',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept6',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept29',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept140',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept254',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept362',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept13',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept24',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept221',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept263',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept20',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept266',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept231',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept15',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept42',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept41',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept31',
#     'http://vivo.brown.edu/individual/org-brown-univ-dept14'
# ]

def traverse(nodes):
    data = query(nodes.pop())
    filtered = filterData(data)
    nbors = pathfinder(filtered)
    nodes = nodesnbors
    if not nodes:
        return filtered
    else:
        return filtered + traverse(nodes)

def parse_ntriple(row):
    s = row[:row.index(' ')]
    row = row[row.index(' ') + 1:]
    p = row[:row.index(' ')]
    row = row[row.index(' ') + 1:]
    o = row[:row.rindex(" .")]
    # o = row[:]
    return (s,p,o)

# def split_ntriples(nt):
#     delim = ' .\n'
#     line_end = nt.index(delim)
#     idx = nt.index(delim)
#     parsed = nt[:idx]
#     if nt[idx + len(delim):] == '\n':
#         return [ parsed ]
#     else:
#         return [parsed ] + split_ntriples(nt[idx + len(delim):])

def query(uri):
    query = """
    CONSTRUCT {{ <{0}> ?p ?o. }}
    WHERE {{ <{0}> ?p ?o .}}
    """.format(uri)
    headers = {'Accept': 'text/plain', 'charset':'utf-8'} 
    data = { 'email': config.email, 'password': config.passw, 'query': query }
    resp = requests.post(config.query_url, data=data, headers=headers)
    if resp.status_code == 200:
        triples = resp.text.splitlines()
        return [ parse_ntriple(t) for t in triples ]
    else:
        return []

if __name__ == '__main__':
    shortid = sys.argv[1]
    print query('http://vivo.brown.edu/individual/' + shortid)
    # with open('data/genberg.nt','r') as f:
    #     nt = f.read()
    # for line in nt.splitlines():
    #     if line == '\n':
    #         break
    #     print parse_ntriple(line)