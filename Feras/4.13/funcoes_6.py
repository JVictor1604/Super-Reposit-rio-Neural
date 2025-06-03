import random
import matplotlib.pyplot as plt


###############################################################################
#                               Caixas binárias                               #
###############################################################################




def cria_candidato_liga(n, tamanho_liga, elementos_possiveis):
    """Cria uma lista com n valores com valores 1 igual ao tamanho da liga .

    Args:
      n: inteiro que representa o número de caixas.

    """
    candidato = []
   
    for elemento in range(n):
        if elemento < tamanho_liga:
            candidato.append(1)
        else: 
            candidato.append(0)


    random.shuffle(candidato)
        
    return  candidato


def populacao_cb_liga(tamanho_populacao, n, tamanho_liga):
    """Cria uma população para o problema das caixas binárias.
    Args:
      tamanho: tamanho da população
      n: inteiro que representa o número de caixas de cada indivíduo.

    """
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_cb_liga(n, tamanho_liga))
    return populacao


###############################################################################
#                             Problema da Liga                            #
###############################################################################


def calcula_liga(candidato, itens, ordem_dos_itens):
    """Computa a quantidade de elementos e o valor da liga
    Args:
      candidato: lista representando quais itens estão na mochila
      itens: dicionário com os pesos e valores dos itens
      ordem_dos_itens: ordem dos itens da lista `candidato`

    """
    quantidade = 0
    preco = 0
    for pegou_item_ou_nao, nome_item in zip(candidato, ordem_dos_itens):
        if pegou_item_ou_nao == 1:
            quantidade += itens[nome_item]["quantidade"]
            preco += itens[nome_item]["preco"] * itens[nome_item]["quantidade"]
    return  quantidade, preco


def funcao_objetivo_liga(candidato, itens, ordem_dos_itens, limite):
    """Computa a funcao objetivo de um candidato no problema das ligas tenárias mais cara
    Args:
      candidato: lista representando quais itens estão na mochila
      itens: dicionário com os pesos e valores dos itens
      ordem_dos_itens: ordem dos itens da lista `candidato`
      limite: valor representando o limite de peso da mochila
    """
    quantidade, preco = calcula_liga(candidato, itens, ordem_dos_itens)

   
    if quantidade < limite :
            return preco
    else:
            return 0.01


def funcao_objetivo_pop_liga(populacao, itens, ordem_dos_itens, limite):
    """Computa a fun. objetivo de uma populacao no problema daas ligas mais caras

    Args:
      populacao: lista contendo os individuos do problema
      itens: dicionário com os pesos e valores dos itens
      ordem_dos_itens: ordem dos itens da lista `candidato`
      limite: valor representando o limite de peso da mochila

    """
    fitness = []

    for individuo in populacao:
        fitness.append(
            funcao_objetivo_liga(individuo, itens, ordem_dos_itens, limite)
        )

    return fitness


###############################################################################
#                                   Seleção                                   #
###############################################################################



def selecao_torneio_max(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

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

        for gene_pai, gene_mae in zip(pai, mae):
            if random.choice([True, False]):
                filho1.append(gene_pai)
                filho2.append(gene_mae)
            else:
                filho1.append(gene_mae)
                filho2.append(gene_pai)

        return filho1, filho2
    else:
        return pai, mae



###############################################################################
#                                   Mutação                                   #
###############################################################################



def mutacao_troca(populacao, chance_de_mutacao):
    """Aplica mutacao de troca em um indivíduo

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:

            gene1 = random.randint(0, len(individuo) - 1)
            gene2 = random.randint(0, len(individuo) - 1)

            if individuo[gene1] != individuo[gene2]:
                VALORES_IGUAIS = False
            else: 
                 VALORES_IGUAIS = True

            while gene1 == gene2 or VALORES_IGUAIS:
                gene1 = random.randint(0, len(individuo) - 1)
                gene2 = random.randint(0, len(individuo) - 1)

            individuo[gene1], individuo[gene2] = (
                individuo[gene2],
                individuo[gene1],
            )



