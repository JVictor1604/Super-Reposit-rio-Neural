import random

def cria_candidato_liga(Elementos_Possiveis, tamanho_liga, limite=100, Valor_minimo=5):
    """
        Cria um candidato para o problema das  ligas, considerando a soma 
        dos pesos igual a 'limite' para cada candidato e peso mínimo por elemento.
        
        Args:
          Elementos_Possiveis: Dicionário contendo os possíveis elementos a serem usados e o valor associado a cada um deles.
          tamanho_liga: inteiro que representa o número de elementos de cada indivíduo.
          limite = peso total que a soma dos elementos da liga deve atingir para que o indivíduo seja considerado válido
          Valor_minimo: menor valor aceito para o peso de cada elemento da liga.

    """
   
    candidato = {}

    # Escolhe os elementos da liga
    elementos = random.sample(list(Elementos_Possiveis.keys()), tamanho_liga)

    # Sorteia pesos válidos cuja soma = limite e cada peso ≥ Valor_minimo
    pesos = []
    peso_total = 0

    for i in range(tamanho_liga - 1):
        restante = limite - peso_total - (Valor_minimo * (tamanho-liga - i - 1))
        peso = random.randint(Valor_minimo, restante)
        pesos.append(peso)
        peso_total += peso

    # Último peso fecha exatamente o total
    pesos.append(limite - peso_total)

    # Embaralha os pesos para não ficarem sempre na mesma ordem
    random.shuffle(pesos)

    for chave, peso in zip(elementos, pesos):
        candidato[chave] = {"Peso": peso , "Valor": peso* Elementos_Possiveis[chave] }
    
    return candidato

 
def cria_populacao_liga(tamanho_pop, tamanho_liga, Elementos_Possiveis, limite = 100, Valor_minimo = 5):
    """
        Cria uma população para o problema das ligas ternárias.

        Args:
          tamanho_pop: tamanho da população
          tamanho_liga: inteiro que representa o número de elementos de cada indivíduo.
          elementos_possiveis: Dicionário contendo os possíveis elementos a serem usados e o valor associado a cada um deles.
          limite = Peso total necessário para a liga ser adequada. 

    """
    
    populacao = []
    for _ in range(tamanho_pop):
        populacao.append(cria_candidato_liga(Elementos_Possiveis, tamanho_liga))
    return populacao


def funcao_objetivo_liga(candidato):
    """
        Computa a função objetivo no problema das ligas ternárias.

        Args:
          candidato: uma dicionário contendo os elementos, pesos e valores das ligas ternárias do problema.

    """
    
    valor_total = 0
    
    for elemento in candidato:
        valor_total += candidato[elemento]["Valor"]
        
    return valor_total 

    
def funcao_objetivo_pop_liga(populacao):
    """
        Computa a função objetivo para a população de indivíduos das ligas ternárias.

        Args:
          populacao: um lista  contendo os indivíduos do problema.

    """    
    
    
    fitness = []
    
    for candidato in populacao:
        fitness.append(funcao_objetivo_liga(candidato))
                    
    return fitness


def calcula_liga(candidato):
    """
        Computa o peso e o valor total de uma liga

        Args:
          candidato: dicionário representando quais elementos estão na mochila, 
          seu peso e o valor associado a esse peso e elemento.
 
    """
    
    peso = 0
    valor = 0
    elementos = list(candidato.keys())

    for nome_item in elementos:
            peso += candidato[nome_item]["Peso"]
            valor += candidato[nome_item]["Valor"]
    return peso, valor

                       
def selecao_torneio_max(populacao, fitness, tamanho_torneio):
    """
        Faz a seleção de uma população usando torneio.

        Nota: da forma que está implementada, só funciona em problemas de
        maximização.

        Args:
          populacao: lista contendo os individuos do problema
          fitness: lista contendo os valores computados da funcao objetivo
          tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        max_fitness = max(fitness_sorteados)
        indice_max_fitness = fitness_sorteados.index(max_fitness)
        individuo_selecionado = sorteados[indice_max_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados

           
     

def mutacao_elementos_liga(populacao, chance_de_mutacao, elementos_possiveis):
    '''
        Realiza uma mutação nos elementos de indivíduos em uma população de ligas.


        Args:
          populacao: lista de indivíduos, onde cada indivíduo é um dicionário contendo elementos da liga e seus respectivos pesos e valores.
          chance_de_mutacao: probabilidade (float entre 0 e 1) de que cada indivíduo da população sofra mutação.
          elementos_possiveis: Dicionário contendo os possíveis elementos a serem usados e o valor associado a cada um deles.
    '''
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            elementos = list(individuo.keys())
            elementos_possiveis_lista = list(elementos_possiveis.keys())
            elemento_mutado = random.sample(elementos,1)[0]
            elemento_novo = random.sample(elementos_possiveis_lista,1)[0]
            individuo[elemento_novo] = individuo.pop(elemento_mutado)
            individuo[elemento_novo]["Valor"] =  elementos_possiveis[elemento_novo]* individuo[elemento_novo]["Peso"]                       

def mutacao_pesos_liga(populacao, chance_de_mutacao):
    '''
        Realiza uma mutação nos pesos dos elementos de indivíduos em uma população de ligas.


        Args:
          populacao: lista de indivíduos, onde cada indivíduo é um dicionário contendo elementos da liga e seus respectivos pesos e valores.
          chance_de_mutacao: probabilidade (float entre 0 e 1) de que cada indivíduo da população sofra mutação.
    '''
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            elementos = list(individuo.keys())
 
            elementos_usados = random.sample(elementos, 2)

            elemento_1 = elementos_usados[0]
            elemento_2 = elementos_usados[1]

            while individuo[elemento_1]["Peso"] < 10:
                elementos_usados = random.sample(elementos, 2)

                elemento_1 = elementos_usados[0]
                elemento_2 = elementos_usados[1]
 
            peso_removido = random.randint(1,5)
 
            individuo[elemento_1]["Peso"] = individuo[elemento_1]["Peso"] - peso_removido
            individuo[elemento_2]["Peso"] = individuo[elemento_2]["Peso"] + peso_removido                 
                       
                       
def cruzamento_uniforme_dicionario(pai, mae, chance_de_cruzamento, elementos_possiveis):
    '''
        Realiza o cruzamento uniforme entre dois indivíduos representados por dicionários de elementos.

        Neste cruzamento, para cada elemento do indivíduo (gene), a função decide aleatoriamente se cada filho
        herdará o gene do pai ou da mãe. Em alguns casos, ocorre uma troca de genes entre os pais,
        mantendo os pesos mas recalculando os valores com base na tabela de elementos possíveis.

        O objetivo é gerar diversidade genética preservando a estrutura dos indivíduos, que representam ligas
        compostas por elementos com pesos e valores.

        Parâmetros:
        - pai: dicionário representando um indivíduo da população.
        - mae: dicionário representando outro indivíduo com a mesma estrutura.
        - chance_de_cruzamento: float entre 0 e 1 representando a probabilidade de o cruzamento ocorrer.
        - elementos_possiveis: dicionário contendo os elementos disponíveis e seu valor por grama.
          Usado para recalcular o valor ao trocar o gene entre os indivíduos. 
    '''
    
    
    if random.random() < chance_de_cruzamento:
        filho1 = {}
        filho2 = {}

        genes_pai = list(pai.items())
        genes_mae = list(mae.items())

        tamanho = min(len(genes_pai), len(genes_mae))

        for i in range(tamanho):
            (gene_pai, dados_pai) = genes_pai[i]
            (gene_mae, dados_mae) = genes_mae[i]

            if random.choice([True, False]):
                # Filho 1 herda o valor do pai, mas com o peso do pai
                filho1[gene_pai] = {
                    "Peso": dados_pai["Peso"],
                    "Valor": dados_pai["Valor"] 
                }
                # Filho 2 herda o valor da mãe, mas com o peso da mãe
                filho2[gene_mae] = {
                    "Peso": dados_mae["Peso"],
                    "Valor": dados_mae["Valor"] 
                }
            else:
                # Troca os valores, mas mantém os pesos fixos
                filho1[gene_mae] = {
                    "Peso": dados_pai["Peso"],  # Peso do pai
                    "Valor": dados_pai["Peso"] * elementos_possiveis[gene_mae] # Valor da mãe
                }
                filho2[gene_pai] = {
                    "Peso": dados_mae["Peso"],  # Peso da mãe
                    "Valor": dados_mae["Peso"] * elementos_possiveis[gene_pai]
                }

        return filho1, filho2
    else:
        return pai.copy(), mae.copy()
