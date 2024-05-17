#!/usr/bin/python
"""
Small networkx-ish graph library
"""

class Node():
    def __init__( self, n, label=None ):
        if isinstance( n, Node ):
            self.name = n.name
            self.label = n.label
        else:
            self.name = n
            self.label = label
    def __eq__( self, other ):
        if isinstance( other, Node ):
            return self.name==other.name
        return False
    def __str__( self ):
        return f"Node({self.name}, {self.label})"

class Graph():
    def __init__( self ):
        self.nodes = []
        self.edges = []
        self.neighbours = []

    def add_node( self, n, label=None ):
        newn = Node( n, label=label )
        assert( not newn in self.nodes )
        self.nodes += [newn]
        self.neighbours += [[]]

    def add_edge( self, a, b ):
        ia = self.nodes.index( Node(a) )
        ib = self.nodes.index( Node(b) )
        self.edges += [(ia,ib)]
        self.neighbours[ia] += [ib]
        #self.neighbours[ib] += [ia] # Directed graph

    def remove_node( self, n ):
        ni = self.nodes.index( Node(n) )
        # Just clear neighbours and nodes so we don't have to do more bookkeeping
        self.neighbours[ni] = []
        self.nodes[ni] = None
        for nl in self.neighbours:
            if ni in nl:
                nl.remove(ni)
        self.edges = [e for e in self.edges if not ni in e]

    def has_edge( self, a, b ):
        return (b in self.neighbours[a])

    def adjacencies( self, n ):
        ni = self.nodes.index( Node(n) )
        adj = []
        # Get children
        for nn in self.neighbours[ni]:
            adj += [nn]
        # Get parents
        for i,nn in enumerate(self.neighbours):
            if ni in nn:
                adj += [i]
        return adj

    def children( self, n ):
        ni = self.nodes.index( Node(n) )
        return self.neighbours[ni]

    def parents( self, n ):
        ni = self.nodes.index( Node(n) )
        adj = []
        for i,nn in enumerate(self.neighbours):
            if ni in nn:
                adj += [i]
        return adj

    def rebuild( self ):
        nodes = self.nodes
        edges = self.edges
        self.__init__()
        for n in nodes:
            if n is None:
                continue
            self.add_node( n )
        for e in edges:
            self.add_edge( nodes[e[0]], nodes[e[1]] )

    def __str__( self ):
        s = "nodes=["+", ".join([str(None if n is None else n.label) for n in self.nodes])+"]\n"
        s += "edges=["+", ".join([f"({e[0]}, {e[1]})" for e in self.edges])+"]"
        return s

    def dot( self ):
        import graphviz
        G = graphviz.Digraph()
        for n in self.nodes:
            if n is None:
                continue
            G.node( n.name, n.label )
        for e in self.edges:
            G.edge( self.nodes[e[0]].name, self.nodes[e[1]].name )
        return G
