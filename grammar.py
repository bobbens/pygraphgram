#!/usr/bin/python

from ullman import ullman
from graph import Graph, Node
import random

class RuleGraph( Graph ):
    def __init__( self, nodes=[], edges=[] ):
        super().__init__()
        nodelist = []
        for i,n in enumerate(nodes):
            nodelist.append( Node( f"node{i}", label=n) )
        for n in nodelist:
            self.add_node( n )
        for e in edges:
            self.add_edge( nodelist[e[0]], nodelist[e[1]] )

class Rule():
    def __init__( self, lhs, rhs, weight=1, limit=None ):
        self.lhs = lhs
        self.rhs = rhs
        self.weight = weight
        self.limit = None
        self.applied = 0

    def apply( self, G, num=1 ):
        matches = ullman( G, self.lhs )
        random.shuffle(matches)
        for step in range(min(num,len(matches))):
            m = matches[step]
            # Store parents and children
            parents = [G.nodes[i] for i in G.parents( G.nodes[m[0]] ) ]
            children = [G.nodes[i] for i in G.children( G.nodes[m[-1]] ) ]
            # Remove matched nodes
            nodes = []
            for i in m:
                nodes.append( G.nodes[i] )
            for n in nodes:
                G.remove_node(n)
            # Add new nodes
            nodes = []
            for n in self.rhs.nodes:
                name = f"node{len(G.nodes)}"
                newn = Node( name, label=n.label )
                G.add_node( newn )
                nodes.append( newn )
            # Add new edges
            for e in self.rhs.edges:
                G.add_edge( nodes[e[0]], nodes[e[1]] )
            # Reconnect to the rest
            for p in parents:
                G.add_edge( p, nodes[0] )
            for c in children:
                G.add_edge( nodes[-1], c )
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

class Grammar():
    def __init__( self ):
        self.ruleset = []

    def add_rule( self, r,  ):
        self.ruleset += r
