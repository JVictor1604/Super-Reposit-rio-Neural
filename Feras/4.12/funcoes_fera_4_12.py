import random

###############################################################################
#                                    Senha                                    #
###############################################################################


def gene_palindromo(letras_possiveis):
    """Sorteia uma letra.
    Args:
      letras: letras possíveis de serem sorteadas.
    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_palindromo(tamanho_palindromo, letras_possiveis):
    """
    Cria um candidato para o problema dos palindromos.

    Args:
        tamanho_minimo_senha (int): Tamanho mínimo do palíndromo.
        tamanho_maximo_senha (int): Tamanho máximo do palíndromo.
        letras_possiveis (list): Lista de caracteres possíveis para compor o palíndromo.

    Returns:
        list: Um candidato representado por uma lista de caracteres.
    """
    candidato = []

    for _ in range(tamanho_palindromo):
        candidato.append(gene_palindromo(letras_possiveis))

    return candidato



def populacao_palindromo(tamanho_populacao, tamanho_palindromo, letras_possiveis):
    """Cria população inicial no problema do palíndromo

    Args
      tamanho_populacao: tamanho da população.
      tamanho_palíndromo: inteiro representando o tamanho do palíndromo.
      letras_possiveis: letras possíveis de serem sorteadas.
    """
    populacao = []

    for _ in range(tamanho_populacao):
        vogais = {"a", "e", "i", "o", "u"}
        candidato = ""

        while not any(letra in vogais for letra in candidato):
            candidato = cria_candidato_palindromo(tamanho_palindromo, letras_possiveis)

        populacao.append(candidato)

    return populacao


def funcao_objetivo_palindromo(candidato):
    """Computa a funcao objetivo de um candidato no problema dos palindromos

    Args:
      candidato: um palpite para um possível palíndromo
    """

    distancia = 0

    for i in range(len(candidato) // 2):
        distancia += abs(ord(candidato[i]) - ord(candidato[-i - 1]))

    return distancia


def funcao_objetivo_pop_palindromo(populacao):
    """Computa a funcao objetivo de uma populaçao no problema dos palíndromos.

    Args:
      populacao: lista contendo os individuos do problema
      senha_verdadeira: a senha que você está tentando descobrir

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_palindromo(individuo))
    return fitness


###############################################################################
#                                   Seleção                                   #
###############################################################################

def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

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

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


###############################################################################
#                                  Cruzamento                                 #
###############################################################################

def cruzamento_uniforme(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento uniforme
    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento
    """
    if random.random() < chance_de_cruzamento:
        filho1 = []
        filho2 = []
        
        parte_da_mae = mae
        parte_do_pai = pai
        
        if pai > mae:
            parte_do_pai = pai[:len(mae)]
        elif mae > pai:
            parte_da_mae = mae[:len(pai)]
           

        for gene_pai, gene_mae in zip(parte_do_pai, parte_da_mae):
            if random.choice([True, False]):
                filho1.append(gene_pai)
                filho2.append(gene_mae)
            else:
                filho1.append(gene_mae)
                filho2.append(gene_pai)
                      
        if pai > mae:
           filho2 += pai[len(mae):]
        elif mae > pai:
            filho2 += mae[len(pai):]

        return filho1, filho2
    else:
        return pai, mae



###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            if len(individuo) > 1:
                gene = random.randint(0, len(individuo) -1)
            else: 
                gene = 0
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]
            
            
def mutacao_insecao_delecao(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            if random.choice([True, False]):
                individuo.append(random.choice(valores_possiveis))
            else:
                if len(individuo) > 1:
                    individuo.pop(random.randint(0, len(individuo) - 1))

def mutacao_simples(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação simples

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            if len(individuo) > 1:
                gene = random.randint(0, len(individuo) -1)
            else: 
                gene = 0
            valor_gene = individuo[gene]
            valores_sorteio = set(valores_possiveis) - set([valor_gene])
            individuo[gene] = random.choice(list(valores_sorteio))


            


def mutacao_simples_cb(populacao, chance_de_mutacao):
    """Realiza mutação simples no problema das caixas binárias

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            individuo[gene] = 0 if individuo[gene] == 1 else 1


def mutacao_sucessiva_cb(populacao, chance_de_mutacao, chance_mutacao_gene):
    """Realiza mutação simples no problema das caixas binárias

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      chance_mutacao_gene: float entre 0 e 1 representando a chance de mutação de cada gene

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            for gene in range(len(individuo)):
                if random.random() < chance_mutacao_gene:
                    individuo[gene] = 0 if individuo[gene] == 1 else 1


def mutacao_simples_cnb(populacao, chance_de_mutacao, valor_max):
    """Realiza mutação simples no problema das caixas não-binárias

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valor_max: inteiro represtando o valor máximo das caixas

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            valores_possiveis = list(range(valor_max + 1))
            valores_possiveis.remove(valor_gene)
            individuo[gene] = random.choice(valores_possiveis)


def mutacao_sucessiva_cnb(
    populacao, chance_de_mutacao, chance_mutacao_gene, valor_max
):
    """Realiza mutação simples no problema das caixas não-binárias

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      chance_mutacao_gene: float entre 0 e 1 representando a chance de mutação de cada gene
      valor_max: inteiro represtando o valor máximo das caixas

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            for gene in range(len(individuo)):
                if random.random() < chance_mutacao_gene:
                    valores_possiveis = list(range(valor_max + 1))
                    valor_gene = individuo[gene]
                    valores_possiveis.remove(valor_gene)
                    individuo[gene] = random.choice(valores_possiveis)
