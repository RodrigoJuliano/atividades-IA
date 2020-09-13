from definitions import Environment
import numpy as np
import matplotlib.pyplot as plt
import copy


class Sudoku(Environment):
    '''Implements a sudoku environment

    '''
    def __init__(self, sudoku, make_arc_cosistent=True):
        ''' Class constructor

        Args:
            sudoku: A matrix representing the sudoku game
            make_arc_cosistent: A flag indicating whether the environment is acr consistent
        '''

        self.sudoku = sudoku
        self.csp = []
        self.make_arc_consistent = make_arc_cosistent

    def initial_percepts(self):

        self.ini_csp()

        if self.make_arc_consistent:
            self.apply_GAC()

        return {'is_viable': None,
                'sudoku': self.sudoku,
                'csp': self.csp}

    def signal(self, action):
        ''' Signals the current state of the problem to the agent 

        Args:
            action: Contains the position that the agent wants to change
                and the value the agent wants to put in that position
        '''

        position = action['position']
        value = action['value']

        viable = is_viable(self.sudoku, position[0], position[1], value)

        return {'is_viable': viable,
                'csp': self.csp,
                'sudoku': self.sudoku}

    def ini_csp(self):
        ''' Builds a CSP representation of the sudoku game 

        '''

        for i in range(len(self.sudoku)):
            self.csp.append([])
            for j in range(len(self.sudoku[0])):
                if self.sudoku[i][j] == 0:
                    constraints = []
                    # Cells in the same column
                    for k in range(len(self.sudoku)):
                        if i != k:
                            constraints.append(DiffConstraint([[i, j], [k, j]]))

                    # Cells in the same row
                    for k in range(len(self.sudoku[0])):
                        if j != k:
                            constraints.append(DiffConstraint([[i, j], [i, k]]))

                    # Different from other cell in the same group
                    ig = (i // 3) * 3
                    jg = (j // 3) * 3

                    for ii in range(0, 3):
                        for jj in range(0, 3):
                            if (ii + ig) != i and (jj + jg) != j:
                                constraints.append(DiffConstraint([[i, j], [(ii + ig), (jj + jg)]]))

                    self.csp[i].append(
                        {'X': [i, j], 'D': [int(n) for n in range(1, 10)], 'C': copy.deepcopy(constraints)})

                else:
                    self.csp[i].append({'X': [i, j], 'D': [self.sudoku[i][j]],
                                        'C': [EqNumConstraint([[i, j], self.sudoku[i][j]])]})

    def apply_GAC(self):
        to_do = [] # lista de arcos que precisam ser analizados
        # Adiciona os arcos iniciais
        for i in range(len(self.csp)):
            for j in range(len(self.csp[i])):
                for c in self.csp[i][j]['C']:
                    # Não precisa verificar EqNumConstraint pois nesses casos o d(X)
                    # já possui apenas um valor que não pode ser removido
                    if type(c) == DiffConstraint:
                        to_do.append((c.scope[0], c))
        
        while to_do:
            x, c = to_do.pop()
            # arcos adicionados após a atualização de um domínio
            # tem o y do lado esquerdo (posição 0 no scope) na restrição
            y = c.scope[1] if c.scope[0] == x else c.scope[0]
            nd = [] # Novo domínio de X
            # Adiciona em nd os valores do d(X) que
            # tem pelo menos um diferente em d(Y)
            for vx in self.csp[x[0]][x[1]]['D']:
                for vy in self.csp[y[0]][y[1]]['D']:
                    if(vx != vy):
                        nd.append(vx)
                        break
            if len(nd) != len(self.csp[x[0]][x[1]]['D']):
                # atualiza X com o novo domínio
                self.csp[x[0]][x[1]]['D'] = copy.deepcopy(nd)
                # adiciona arcos (Z, c) para cada outra restrição de X
                # sendo Z a outra variável envolvida na restrição
                for xc in self.csp[x[0]][x[1]]['C']:
                    if xc != c:
                        to_do.append((xc.scope[1], xc))

def is_viable(sudoku, i, j, v):
    ''' Auxiliary method that verifies whether a value, v, can be assigned to position [i,j] in the sudoku

    Args:
        sudoku: 
        i: row index
        j: column index
        v: value

    Returns:
        True if the move is viable or False, otherwise

    '''

    # Different from other cell in the same row
    for k in range(len(sudoku[0])):
        if k != j and sudoku[i][k] == v:
            return False

    # Different from other cell in the same row
    for k in range(len(sudoku)):
        if k != i and sudoku[k][j] == v:
            return False

    # Different from other cell in the same group
    ig = (i // 3) * 3
    jg = (j // 3) * 3

    for ii in range(0, 3):
        for jj in range(0, 3):
            if (ii + ig) != i and (jj + jg) != j and sudoku[ii + ig][jj + jg] == v:
                return False

    return True



class Constraint:
    ''' Defines the interface for a constraint 
    
    '''


    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def apply(self):
        raise NotImplementedError('apply')


class DiffConstraint(Constraint):
    ''' Implements a non-equality constraint 
    
    '''

    def __init__(self, scope):
        condition = lambda a, b: a != b
        Constraint.__init__(self, scope, condition)

    def __repr__(self):
        return '{} != {}'.format(self.scope[0], self.scope[1])

    def apply(self, sudoku):
        return self.condition(sudoku[self.scope[0][0]][self.scope[0][1]],
                              sudoku[self.scope[1][0]][self.scope[1][1]])


class EqNumConstraint(Constraint):
    ''' Implements a equality constraint 
    
    '''

    def __init__(self, scope):
        condition = lambda a, b: a == b
        Constraint.__init__(self, scope, condition)

    def __repr__(self):
        return '{} == {}'.format(self.scope[0], self.scope[1])

    def apply(self, sudoku):
        return self.condition(sudoku[self.scope[0][0]][self.scope[0][1]],
                              self.scope[1])



