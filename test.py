#!/usr/bin/python

from ullman import ullman
from graph import Graph, Node

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
