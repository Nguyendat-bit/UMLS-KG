# Load, Visualize, Query UMLS Knowledge graph with Neo4j 
## Overview
On this repo, you can load UMLS knowledge graph and Visualize with Neo4j and you can use Neo4j python driver to query nodes or relationships what you want.

First, you need to install UMLS dataset and load it into mysql.
<p><img src= 'UMLS and Neo4j/images/visual.png'></p>

## Usage
### Requirement
- python >= 3.9
- pymysql >= 1.0.2
- csv >= 1.0 
- neo4j python driver >= 4.4.5
- Docker 


### Create your graph 
Run this code below:
```python
python build_graph.py --host ${host} --user ${user} --password ${password} --database ${database}
```
Example:
```python
python build_graph.py --host localhost --user root --password root --database umls2022
```
Ouput: 
```
3618459 concepts
7577026 atoms
25004792 relationships
```
### Import UMLS data into Neo4j 
Run this code below:
```command
docker run -it -v /d/umls/2022AA/META:/data -v /d/umls/2022AA/META:/var/lib/neo4j/import neo4j:3.5 bin/neo4j-admin import --nodes=import/MRCONSO.processed.csv /--nodes=import/MRAUI.processed.csv --relationships=import/MRREL.processed.csv
```
In the above script, `--nodes` represents specifying location of node tables used, and `--relationships` represents specifying location of relationship tables. You can specify multiple nodes or relationships table for importing various types of nodes and relationships. 

<img src= 'UMLS and Neo4j/images/neo4j-admin.png'>

<br>
Now you can visualize and query nodes or subgraphs what you want.<br>

Befor to do that, you should shutdown docker container of neo4j image and run this code below: 

```
docker run -it -p7474:7474 -p7687:7687 -v /d/umls/2022AA/META:/data -v /d/umls/2022AA/META:/var/lib/neo4j/import --env NEO4J_AUTH=neo4j/test neo4j:3.5 
```
In the above script, neo4j is `user` and test is `password`.

For example, I will query nodes that have relationship with `CUI` C0000039.
<img src= 'UMLS and Neo4j/images/relation.png'>

### Using Neo4j python driver to query database
First you need to install neo4j package:
```
pip install neo4j
```

Run this code below: 
```python 
import neo4j 
from neo4j import GraphDatabase
graphdb= GraphDatabase.driver(uri= "bolt://localhost:7687", auth=("neo4j", "test"))
session= graphdb.session()
q1="match (p: Concept {CUI: 'C0000039'}) return p"
nodes= session.run(q1)
for node in nodes: 
    print(node)
```
Output: 

```jupyter
<Record p=<Node id=1 labels=frozenset({'Concept'}) properties={'name': '1,2-dipalmitoylphosphatidylcholine', 'CUI': 'C0000039'}>>
```


