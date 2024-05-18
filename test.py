#!/usr/bin/python

from ullman import ullman
from graph import Graph
from grammar import RuleGraph, Rule, RuleSet

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

G = Graph()
G.add_node( "start", label="START" )
G.add_node( "internal", label="X" )
G.add_node( "goal", label="GOAL" )
G.add_edge( "start", "internal" )
G.add_edge( "internal", "goal" )

R = RuleSet( [
    Rule( RuleGraph( nodes=["X"] ),
          RuleGraph( nodes=["X", "X"], edges=[(0,1)] ), name="expand", ),
    Rule( RuleGraph( nodes=["X"] ),
          RuleGraph( nodes=["SPLIT", "X", "X"], edges=[(0,1), (0,2)] ), name="split" ),
    Rule( RuleGraph( nodes=["X"] ),
          RuleGraph( nodes=["SPLIT", "X", "X", "MERGE"], edges=[(0,1), (0,2), (1,3), (2,3)] ), name="splitmerge" ),
    Rule( RuleGraph( nodes=["X"] ),
          RuleGraph( nodes=["KEY", "X", "DOOR"], edges=[(0,1), (1,2),(0,2,"opens")] ), limit=1, name="keydoor" ),
    ] )
R.apply( G, 10 )
dot = G.dot()
print( dot )
dot.render()
