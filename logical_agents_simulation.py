from knowledge_base import *
from logical_agents import LogicalAgent


kb = KB([Clause('a',['b','c']),
        Clause('b',['g','e']),
        Clause('b',['d','e']),
        Clause('c',['e']),
        Askable('d'),
        Clause('e'),
        Clause('f',['a','g']) ])

print(kb)

ag = LogicalAgent(kb)

# Derive all the logical consequences of KB
consequences = ag.bottom_up()
print(consequences)

# Prove 'a'
print(ag.top_down(['a']))
