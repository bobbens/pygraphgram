#!/usr/bin/python
"""
Ullman's basic algorithm with minor modifications
"""

from copy import deepcopy

def search( G, S, assignments, candidates, found ):
    n = len(assignments)
    # Make sure edges match for assigned vertices and subgraph
    for edge in S.edges:
        if edge[0]<n and edge[1]<n:
            if not G.has_edge( assignments[edge[0]], assignments[edge[1]], edge[2] ):
                return False
    # All vertices assigned
    if n==len(S.nodes):
        return True
    # Time to try candidates for next node
    for j in candidates[n]:
        if j not in assignments:
            assignments.append(j)
            if search( G, S, assignments, candidates, found ):
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
    search( G, S, assignments, candidates, found )
    return found
