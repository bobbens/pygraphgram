#!/usr/bin/python

from ullman import ullman
from graph import Graph, Node
import random

nodecounter = 0

class RuleGraph( Graph ):
    def __init__( self, nodes=[], edges=[] ):
        super().__init__()
        nodelist = []
        for i,n in enumerate(nodes):
            nodelist.append( Node( f"node{i}", label=n) )
        for n in nodelist:
            self.add_node( n )
        for e in edges:
            label = None
            if len(e)>2:
                label = e[2]
            self.add_edge( nodelist[e[0]], nodelist[e[1]], label )

class Rule():
    def __init__( self, lhs, rhs, embedin=[(0,0)], embedout=[(-1,-1)], name="unknown", weight=1, limit=None ):
        self.lhs = lhs
        self.rhs = rhs
        self.embedin = embedin
        self.embedout = embedout
        self.weight = weight
        self.limit = limit
        self.applied = 0
        self.name = name

    def apply( self, G, num=1 ):
        global nodecounter
        matches = ullman( G, self.lhs )
        random.shuffle(matches)
        for step in range(min(num,len(matches))):
            m = matches[step]
            # Store parents and children
            embedin = []
            for e in self.embedin:
                parents = [G.nodes[i] for i in G.parents( G.nodes[m[e[0]]] ) ]
                plabels = [G.get_edge_label( p, G.nodes[m[e[0]]] ) for p in parents ]
                embedin += [(parents,plabels)]
            embedout = []
            for e in self.embedout:
                children = [G.nodes[i] for i in G.children( G.nodes[m[e[0]]] ) ]
                clabels = [G.get_edge_label( G.nodes[m[e[0]]], c ) for c in children ]
                embedout += [(children,clabels)]
            # Remove matched nodes
            nodes = []
            for i in m:
                nodes.append( G.nodes[i] )
            for n in nodes:
                G.remove_node(n)
            # Add new nodes
            nodes = []
            for n in self.rhs.nodes:
                name = f"node{nodecounter}"
                nodecounter+=1
                newn = Node( name, label=n.label )
                G.add_node( newn )
                #print(f"add_node {newn}")
                nodes.append( newn )
            # Add new edges
            for e in self.rhs.edges:
                G.add_edge( nodes[e[0]], nodes[e[1]], e[2] )
                #print(f"add_edge {nodes[e[0]]}-{nodes[e[1]]}")
            # Reconnect to the rest
            for i in range(len(self.embedin)):
                e = self.embedin[i]
                ei = embedin[i]
                for j,p in enumerate(ei[0]):
                    G.add_edge( p, nodes[e[1]], ei[1][j] )
                    #print(f"add_edge(parent) {p}-{nodes[e[1]]}")
            for i in range(len(self.embedout)):
                e = self.embedout[i]
                eo = embedout[i]
                for j,c in enumerate(eo[0]):
                    G.add_edge( nodes[e[1]], c, eo[1][i] )
                    #print(f"add_edge(child) {nodes[e[1]]}-{c}")
        self.applied += 1
        G.rebuild()

    def reset( self ):
        self.applied = 0

    def can_apply( self, G ):
        return (self.limit==None or self.applied < self.limit) and len(ullman( G, self.lhs ))>0

class RuleSet():
    def __init__( self, rules=[] ):
        self.rules = rules

    def apply( self, G, num=1 ):
        for step in range(num):
            # Get potential applicable rules
            wmax = 0
            valid_rules = []
            for i,r in enumerate(self.rules):
                if r.can_apply(G):
                    valid_rules.append( r )
                    wmax += r.weight
            if len(valid_rules)<=0:
                break
            # Now sort by weight and apply
            rng = random.random() * wmax
            w = 0
            for r in valid_rules:
                w += r.weight
                if rng <= w:
                    r.apply( G )
                    break
