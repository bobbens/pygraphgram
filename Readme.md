A small test for grammar rewriting for procedural content generation.
Heavily inspired by [graphgram](https://github.com/ihh/graphgram).
This is more of a learning experience / demo / playground than a serious library or software.

### Features
* Ullman's Subgraph Isomorphism Algorithm for matching
* Double Pushout Algorithm for rewriting
* Grammar based on Neighbourhood Controlled Embedding Directed graph with Boundary Constraint (B-dNCE)
* Simplified embedding rules for input / output edges
* graphviz visualization support

### Usage
You can test the main script with:
```
$ python test.py
```
It should print some output and generate a pdf document showing an example generated graph.

### Files
* `graph.py`: Simple directed graph representation
* `ullman.py`: Simple implementation of Ullman's Subgraph Isomorphism Algorithm
* `grammar.py`: Contains the grammar definitions and double pushout rewriting algorithm
* `test.py`: Code demo showing all features
