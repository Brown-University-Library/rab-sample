
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

import urllib3
urllib3.disable_warnings()

faculty = [
    # 'http://vivo.brown.edu/individual/khansenm',
    # 'http://vivo.brown.edu/individual/embrown',
    # 'http://vivo.brown.edu/individual/jpipher',
    # 'http://vivo.brown.edu/individual/lbrownmd',
    # 'http://vivo.brown.edu/individual/etollmd',
    # 'http://vivo.brown.edu/individual/jvandenb',
    # 'http://vivo.brown.edu/individual/bgenberg',
    # 'http://vivo.brown.edu/individual/mhohenha',
    # 'http://vivo.brown.edu/individual/eterrymo',
    # 'http://vivo.brown.edu/individual/aplette',
    # 'http://vivo.brown.edu/individual/rarenber',
    # 'http://vivo.brown.edu/individual/cfaulkne',
    # 'http://vivo.brown.edu/individual/mklitzke',
    # 'http://vivo.brown.edu/individual/jdibened',
    # 'http://vivo.brown.edu/individual/cvillarr',
    # 'http://vivo.brown.edu/individual/scohenmd',
    # 'http://vivo.brown.edu/individual/mhillstr',
    # 'http://vivo.brown.edu/individual/mdasilva',
    # 'http://vivo.brown.edu/individual/cjsammar',
    # 'http://vivo.brown.edu/individual/lsnadymc',
    # 'http://vivo.brown.edu/individual/pruberto',
    # 'http://vivo.brown.edu/individual/jkuzner',
    # 'http://vivo.brown.edu/individual/pharropm',
    # 'http://vivo.brown.edu/individual/ss74',
    # 'http://vivo.brown.edu/individual/cn8',
    # 'http://vivo.brown.edu/individual/rbhatt',
    # 'http://vivo.brown.edu/individual/dnickel',
    # 'http://vivo.brown.edu/individual/awebb',
    # 'http://vivo.brown.edu/individual/efwalsh',
    # 'http://vivo.brown.edu/individual/ll7',
    # 'http://vivo.brown.edu/individual/kmonchik',
    # 'http://vivo.brown.edu/individual/ewittels',
    # 'http://vivo.brown.edu/individual/egartman',
    # 'http://vivo.brown.edu/individual/ljrubinm',
    # 'http://vivo.brown.edu/individual/ffenghi',
    # 'http://vivo.brown.edu/individual/rpadilla',
    # 'http://vivo.brown.edu/individual/elaposat',
    # 'http://vivo.brown.edu/individual/ccarpent',
    # 'http://vivo.brown.edu/individual/rbungiro',
    # 'http://vivo.brown.edu/individual/sschenna',
    # 'http://vivo.brown.edu/individual/wc53',
    # 'http://vivo.brown.edu/individual/ac184',
    # 'http://vivo.brown.edu/individual/mapomera',
    # 'http://vivo.brown.edu/individual/gdk',
    # 'http://vivo.brown.edu/individual/mfaganmd',
    # 'http://vivo.brown.edu/individual/nlawandy',
    # 'http://vivo.brown.edu/individual/dchronle',
    '<http://vivo.brown.edu/individual/rwestlak>',
    '<http://vivo.brown.edu/individual/rpendse>',
    '<http://vivo.brown.edu/individual/bgenberg>'
]


def traverse(nodes, outFile):
    visited = set()
    loop = 0
    bad = [ 'http://vivo.brown.edu/individual/jalbinam',
            'http://vivo.brown.edu/individual/imilleri',
            'http://vivo.brown.edu/individual/elbloom',
            'http://vivo.brown.edu/individual/ac171',
            'http://vivo.brown.edu/individual/dchatter',
            ]

    with open(outFile, 'w') as f:
        while len(nodes) > 0 and loop < 300:
            node = nodes.pop()
            visited.add(node)
            data = query(node)
            parsed = parseResponse(data)
            filtered = filterData(parsed)
            for line in filtered:
                f.write( '{0} {1} {2} .\n'.format(*line) )
            nbors = pathFinder(filtered)
            # check = [ n for n in nbors if n in bad ]
            # if len(check) > 0:
            #     print node, check
            nodes = nodes + nbors
            nodes = [ n for n in nodes if n not in visited ]
            loop += 1

    print loop


def filterData(data):
    strip_properties =  [
            '<http://vivoweb.org/ontology/core#organizationForPosition>',
            '<http://vivoweb.org/ontology/core#organizationForTraining>',
            '<http://vivoweb.org/ontology/core#hasCollaborator>',
            '<http://vivo.brown.edu/ontology/vivo-brown/hasAffiliation>',
            '<http://vivoweb.org/ontology/core#researchAreaOf>',
            '<http://vivo.brown.edu/ontology/citation#hasContributor>',
            '<http://vivo.brown.edu/ontology/citation#venueFor>',
            # '<http://vivo.brown.edu/ontology/profile#trainingFor>',
            # '<http://vivo.brown.edu/ontology/vivo-brown/cvOf>',
            # '<http://vivoweb.org/ontology/core#webpageOf>',
            # '<http://vivoweb.org/ontology/core#educationalTrainingOf>',
            # '<http://vivoweb.org/ontology/core#positionForPerson>',
            '<http://vivoweb.org/ontology/core#subOrganizationWithin>',
            '<http://vivo.brown.edu/ontology/profile#organizationFor>',
            '<http://vivo.brown.edu/ontology/display#BrownOrg>'
            
        ]
    # strip_properties = {
    #     '<http://xmlns.com/foaf/0.1/Organization>' : [
    #         '<http://vivoweb.org/ontology/core#organizationForPosition>',
    #         '<http://vivoweb.org/ontology/core#organizationForTraining>'
    #     ],
    #     '<http://vivoweb.org/ontology/core#FacultyMember>' : [
    #         '<http://vivoweb.org/ontology/core#hasCollaborator>',
    #         '<http://vivo.brown.edu/ontology/vivo-brown/hasAffiliation>'
    #     ],
    #     '<http://www.w3.org/2004/02/skos/core#Concept>' : [
    #         '<http://vivoweb.org/ontology/core#researchAreaOf>'
    #     ],
    #     '<http://vivo.brown.edu/ontology/citation#Citation>' : [
    #         '<http://vivo.brown.edu/ontology/citation#hasContributor>'
    #     ],
    #     '<http://vivo.brown.edu/ontology/citation#Venue>' : [
    #         '<http://vivo.brown.edu/ontology/citation#venueFor>'
    #     ],
    #     '<http://vivo.brown.edu/ontology/profile#PostdocAppointment>' : [
    #         '<http://vivo.brown.edu/ontology/profile#trainingFor>'
    #     ],
    #     '<http://vivoweb.org/ontology/core#URLLink>' : [
    #         '<http://vivo.brown.edu/ontology/vivo-brown/cvOf>',
    #         '<http://vivoweb.org/ontology/core#webpageOf>'
    #     ],
    #     '<http://vivoweb.org/ontology/core#EducationalTraining>': [
    #         '<http://vivoweb.org/ontology/core#educationalTrainingOf>'
    #     ],
    #     '<http://vivoweb.org/ontology/core#FacultyPosition>' : [
    #         '<http://vivoweb.org/ontology/core#positionForPerson>'
    #     ]
    # }
    # type_data = [ t for t in data 
    #                 if t[1] == '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' and
    #                     t[2] in strip_properties.keys() ]
    # if len(type_data) == 0:
    #     return data
    # rmv = strip_properties[type_data[0][2]]
    return [ t for t in data if t[1] not in strip_properties ]

def pathFinder(data):
    skip = [ '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
            '<http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType>',
            '<http://vitro.mannlib.cornell.edu/ns/vitro/public#mostSpecificType>',
            '<http://vivoweb.org/ontology/core#dateTimePrecision>' ]
    return [ t[2] for t in data if t[2].startswith('<') and
                t[1] not in skip ]

def parse_ntriple(row):
    s = row[:row.index(' ')]
    row = row[row.index(' ') + 1:]
    p = row[:row.index(' ')]
    row = row[row.index(' ') + 1:]
    o = row[:row.rindex(" .")]
    return (s,p,o)

def parseResponse(resp):
    if resp == '':
        return []
    triples = resp.splitlines()
    if triples[-1] == '':
        triples = triples[:-1]
    return [ parse_ntriple(t) for t in triples ]

def query(uri):
    query = """
    CONSTRUCT {{ {0} ?p ?o. }}
    WHERE {{ {0} ?p ?o .}}
    """.format(uri)
    headers = {'Accept': 'text/plain', 'charset':'utf-8'} 
    data = { 'email': config.email, 'password': config.passw, 'query': query }
    resp = requests.post(config.query_url, data=data, headers=headers)
    if resp.status_code == 200:
        return resp.text
    else:
        print resp.text
        return ''

if __name__ == '__main__':
    # with open('data/genberg.nt', 'r') as f:
    #     nt = f.read()
    # parsed = parseResponse(nt)
    # filtered = filterData(parsed)
    # print pathFinder(filtered)
    traverse(faculty, 'data/sample.nt')