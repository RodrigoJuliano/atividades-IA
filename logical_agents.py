class LogicalAgent():

    def __init__(self,KB):
        self.KB = KB

    def bottom_up(self):
        ''' Implements the botton up proof strategy and returns all the logical consequence odf the KB

        Returns:
            A list with all the logical consequences of KB
        '''
        c = []
        
        askables = [i.atom for i in self.KB.askables]

        while True:
            # Inicialmente encontra todas consequências lógicas
            # sem considerar os askables
            while True:
                c_len_old = len(c)
                # Verifica todas as cláusulas
                for dc in self.KB.clauses:
                    # Se ainda não foi provado e todos átomos do corpo
                    # são consequências lógicas (ou não tem corpo)
                    if not dc.head in c and all(i in c for i in dc.body):
                        # Então o átomo da cabeça também é consequência lógica
                        c.append(dc.head)
                # Para a busca se não encontrou nehuma consequência lógica
                if c_len_old == len(c):
                    break

            # Remove os askables que já foram provados
            askables = [i for i in askables if i not in c]
            
            # Pergunta ao usuário sobre os askables até uma resposta positiva
            c_len_old = len(c)
            while askables:
                askable = askables.pop()
                if self.ask_askable(askable):
                    c.append(askable)
                    break
            
            # Se nenhum askable teve resposta positiva o algoritmo para
            # Caso contrário é feito uma nova verificação
            # (faz um busca completa a cada askable com resposta positiva
            # para fazer um número mínimo de perguntas ao usuário)
            if c_len_old == len(c):
                break
        return c

    def top_down(self,query):
        '''Implements the top down proof strategy. Given a query (the atom that it wants to prove) 
        it returns True if the query is a consequence of the knowledge base. 
        
        Args:
            querry: The atom that should be proved

        Returns: 
            True if the query is a logical consequence of KB, False otherwise

        '''

        return self.__top_down_aux(set(query), [])
    
    def __top_down_aux(self, g, proven):
        # Enquanto houver átomos para provar
        while g:
            # Escolhe um átomo para provar
            atom = g.pop()
            # Se já foi provado, apenas pula para o próximo átomo
            if not atom in proven:
                clauses = self.KB.clauses_for_atom(atom)
                if any(not i.body for i in clauses):
                    # Se alguma das cláusulas não tem corpo,
                    # então ele é uma consequência lógica
                    proven.append(atom)
                else:
                    for c in clauses:
                        # Para cada cláusula com 'atom' como cabeça
                        # cria uma nova instância do problema, subtituindo
                        # o 'atom' pelo corpo da cláusula
                        if self.__top_down_aux(g | set(c.body), proven):
                            return True
                    
                    # Se não obteve uma sulução em nehuma das instâncias
                    # Verifica se 'atom' é askable e pergunta seu valor ao usuário
                    if (any(x.atom == atom for x in self.KB.askables) and
                        self.ask_askable(atom)):
                        proven.append(atom)
                    else:
                        return False
        return True
    
    # TODO
    def explain(self,g):
        '''Implements the process of abductions. It tries to explain the atoms  in the list g using
         the assumable in KB.

        Args:
            g: A set of atoms that should be explained
        
        Returns:
            A list of explanation for the atoms in g
        '''
        # Obtem os conflitos do KB
        conflicts = self.__explain_aux(set(), {'false'}, [])

        # Obtem as explicações de g
        g_as = {a for a in g if a in self.KB.assumables}
        g_not_as = {a for a in g if a not in self.KB.assumables}
        explans = self.__explain_aux(g_as, g_not_as, [])
        
        # Retorna as explicações que não são conflitos
        return [a for a in explans if a not in conflicts]

    def __explain_aux(self, g_as, g_not_as, proven):
        # utiliza o top_down implementado acima com pequenas adaptações

        while g_not_as:
            atom = g_not_as.pop()
            if not atom in proven:
                clauses = self.KB.clauses_for_atom(atom)
                if any(not i.body for i in clauses):
                    proven.append(atom)
                else:
                    explan = []
                    for c in clauses:
                        _g_as = g_as | {a for a in c.body if a in self.KB.assumables}
                        _g_not_as = g_not_as | {a for a in c.body if a not in self.KB.assumables}
                        ats = self.__explain_aux(_g_as, _g_not_as, proven)
                        if ats:
                            explan = explan + ats

                    if explan:
                        return explan
                    elif (any(x.atom == atom for x in self.KB.askables) and
                        self.ask_askable(atom)):
                            proven.append(atom)
                    else:
                        return []
        return [g_as]

    def yes(self, ans):
        return ans.lower() in ['sim','sim.','s','y','yes','yes.']

    def ask_askable(self,askable):
        return self.yes(input('Is ' + askable + ' true? '))