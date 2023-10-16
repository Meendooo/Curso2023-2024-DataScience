# -*- coding: utf-8 -*-
"""Copia de Task07 Alberto.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gRGlJJvy3log4FoDPYkUbuie6xJyojEY

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

print("RDFLib")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

print("SPARQL")
q1 = prepareQuery('''
    SELECT ?subClass
    WHERE {
      ?subClass rdfs:subClassOf ns:LivingThing
    }
    ''',
    initNs = {"rdfs": rdfs, "ns": ns}
)

for r in g.query(q1):
  print(r.subClass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

q2 = prepareQuery('''
    SELECT ?individual
    WHERE {
      {
        ?individual rdf:type ns:Person.
      } UNION {
        ?x rdfs:subClassOf ns:Person.
        ?individual rdf:type ?x
      }
    }
    ''',
    initNs = {"rdfs": rdfs, "rdf": rdf, "ns": ns}
)

for r in g.query(q2):
  print(r.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

print("SPARQL")
q3 = prepareQuery('''
    SELECT ?individual ?property ?x
    WHERE {
      {
        ?individual rdf:type ns:LivingThing.
        ?individual ?property ?x
      } UNION {
        ?individual rdf:type ?y.
        ?individual ?property ?x.
        ?y rdfs:subClassOf ns:LivingThing
      }
    }
    ''',
    initNs = {"rdfs": rdfs, "rdf": rdf, "ns": ns}
)

for r in g.query(q3):
  print(r)

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

from rdflib import FOAF
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

q4 = prepareQuery('''
  SELECT ?individual ?name
  WHERE {
    ?individual FOAF:knows ns:RockySmith.
    ?individual <http://www.w3.org/2001/vcard-rdf/3.0/Given> ?name
  }
  ''',
  initNs = {"FOAF": FOAF, "VCARD": VCARD, "ns": ns}
)

for r in g.query(q4):
  print(r.name)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

q5 = prepareQuery('''
  SELECT ?entity
  WHERE {
    ?entity FOAF:knows ?entity2
  }
  GROUP BY ?entity
  HAVING (COUNT(?entity2) >= 2)
  ''',
  initNs = {"FOAF":FOAF}
)

for r in g.query(q5):
  print(r.entity)