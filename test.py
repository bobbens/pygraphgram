#!/usr/bin/python

from copy import deepcopy
import random

# Ullman's basic algorithm with minor modifications
def ullman_search( G, S, assignments, candidates, found ):
    n = len(assignments)
    # Make sure edges match for assigned vertices and subgraph
    for edge in S.edges:
        if edge[0]<n and edge[1]<n:
            if not G.has_edge( assignments[edge[0]], assignments[edge[1]] ):
                return False
    # All vertices assigned
    if n==S.n_vertices:
        return True
    # Time to try candidates for next node
    for j in candidates[n]:
        if j not in assignments:
            assignments.append(j)
            if ullman_search( G, S, assignments, candidates, found ):
                # Success, so save copy
                found += [deepcopy(assignments)]
            assignments.pop()

def ullman( G, S ):
    assignments = []
    found = []
    # Prune candidates based on connections, should be simple and fast
    candidates = [None,] * len(S.nodes)
    for sid,sin in enumerate( S.nodes ):
        c = []
        for gid,gin in enumerate( G.nodes ):
            if sin.label!=gin.label:
                continue
            gchildren = G.children(gin)
            for sjd,sjn in enumerate( S.children(sin) ):
                if sjn not in gchildren:
                    continue
            c += [gid]
        candidates[sid] = c
    # Begin search
    ullman_search( G, S, assignments, candidates, found )
    return found

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
        return self.name
class Graph():
    def __init__( self ):
        self.nodes = []
        self.edges = []
        self.neighbours = []
        self.n_vertices = 0

    def add_node( self, n, label=None ):
        self.nodes += [Node( n, label=label )]
        self.neighbours += [[]]
        self.n_vertices = len(self.nodes)

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
        G = Graph()
        for n in self.nodes:
            if n is None:
                continue
            G.add_node( n )
        for e in self.edges:
            G.add_edge( self.nodes[e[0]], self.nodes[e[1]] )
        return G

    def __str__( self ):
        s = "nodes=["+", ".join([str(None if n is None else n.label) for n in self.nodes])+"]\n"
        s += "edges=["+", ".join([f"({e[0]}, {e[1]})" for e in self.edges])+"]"
        return s


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
    def __init__( self, lhs, rhs ):
        self.lhs = lhs
        self.rhs = rhs

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
        return G.rebuild()


G = Graph()
G.add_node( "G0", label="START" )
G.add_node( "G1", label="x" )
G.add_node( "G2", label="x" )
G.add_node( "G3", label="FORK" )
G.add_node( "G4", label="x" )
G.add_node( "G5", label="x" )
G.add_node( "G6", label="x" )
G.add_node( "G7", label="END" )
G.add_edge( "G0", "G1" )
G.add_edge( "G1", "G2" )
G.add_edge( "G2", "G3" )
G.add_edge( "G3", "G4" )
G.add_edge( "G4", "G5" )
G.add_edge( "G5", "G7" )
G.add_edge( "G3", "G6" )
G.add_edge( "G6", "G7" )

S = Graph()
S.add_node( "S0", label="x" )
S.add_node( "S1", label="x" )
S.add_edge( "S0", "S1" )

print( ullman( G, S ) )

LHS = RuleGraph( nodes = ["x"] )
RHS = RuleGraph( nodes = ["x","x"], edges = [(0,1)] )
R = Rule( LHS, RHS )
print( R.apply( G ) )
