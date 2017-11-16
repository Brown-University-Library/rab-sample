
query_api =

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

orgs = [
    'http://vivo.brown.edu/individual/org-brown-univ-dept70',
    'http://vivo.brown.edu/individual/org-brown-univ-dept602',
    'http://vivo.brown.edu/individual/org-brown-univ-dept604',
    'http://vivo.brown.edu/individual/org-brown-univ-dept6',
    'http://vivo.brown.edu/individual/org-brown-univ-dept29',
    'http://vivo.brown.edu/individual/org-brown-univ-dept140',
    'http://vivo.brown.edu/individual/org-brown-univ-dept254',
    'http://vivo.brown.edu/individual/org-brown-univ-dept362',
    'http://vivo.brown.edu/individual/org-brown-univ-dept13',
    'http://vivo.brown.edu/individual/org-brown-univ-dept24',
    'http://vivo.brown.edu/individual/org-brown-univ-dept221',
    'http://vivo.brown.edu/individual/org-brown-univ-dept263',
    'http://vivo.brown.edu/individual/org-brown-univ-dept20',
    'http://vivo.brown.edu/individual/org-brown-univ-dept266',
    'http://vivo.brown.edu/individual/org-brown-univ-dept231',
    'http://vivo.brown.edu/individual/org-brown-univ-dept15',
    'http://vivo.brown.edu/individual/org-brown-univ-dept42',
    'http://vivo.brown.edu/individual/org-brown-univ-dept41',
    'http://vivo.brown.edu/individual/org-brown-univ-dept31',
    'http://vivo.brown.edu/individual/org-brown-univ-dept14'
]

def branch(uri):
    query = """
    CONSTRUCT {{ <{0}> ?p ?o. }}
    WHERE {{ <{0}> ?p ?o .}}
    """.format(uri)
    headers = {'Accept': 'application/json', 'charset':'utf-8'} 
    data = { 'email': email, 'password': passw, 'query': query }
    resp = requests.post(query_url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        logger.error('Bad response from Query API: {}'.format(resp.text))
        return []

def leaf(uri):
    query = """
    CONSTRUCT {{ <{0}> ?p ?o. }}
    WHERE {{
        <{0}> ?p ?o .
        ?p a owl:DatatypeProperty .
    }}
    """.format(uri)
    headers = {'Accept': 'application/json', 'charset':'utf-8'} 
    data = { 'email': email, 'password': passw, 'query': query }
    resp = requests.post(query_url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        logger.error('Bad response from Query API: {}'.format(resp.text))
        return []

def object_query(uri, rawData):
    line_pattern = re.compile(uri + )
    obj_line = re.search()

def main():
