from knowledge_base import *
from logical_agents import *

# First Example
input('Press ENTER to run the fisrt example')

statements = [Clause('alarm',['tampering']),
              Clause('alarm',['fire']),
              Clause('smoke',['fire']),
              Assumable('fire'),
              Assumable('tampering'),]
kb = KBA(statements)
ag = LogicalAgent(kb)
print(ag.explain(['alarm']))

# Second Example
input('Press ENTER to run the second example')
statements = [Clause('bronquite',['gripe']),
              Clause('bronquite',['fumante']),
              Clause('tosse',['bronquite']),
              Clause('chiado',['bronquite']),
              Clause('febre',['gripe']),
              Clause('febre',['infecção']),
              Clause('false',['fumante','não_fumante']),
              Assumable('não_fumante'),
              Assumable('gripe'),
              Assumable('infecção')]

kb = KBA(statements)

kb = KBA(statements)
ag = LogicalAgent(kb)
print(ag.explain(['chiado','febre']))