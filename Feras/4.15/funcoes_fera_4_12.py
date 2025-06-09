import random

###############################################################################
#                                    Palíndromo                              #
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

def cruzamento_uniforme_com_vogal(pai, mae, chance_de_cruzamento):
    vogais = {"a", "e", "i", "o", "u"}

    if random.random() >= chance_de_cruzamento:
        return pai[:], mae[:]

    filho1 = []
    filho2 = []

    # Contadores para saber se cada filho já tem vogal
    vogal_filho1 = 0
    vogal_filho2 = 0

    for gene_pai, gene_mae in zip(pai, mae):
        pai_eh_vogal = gene_pai.lower() in vogais
        mae_eh_vogal = gene_mae.lower() in vogais

        # Caso ambos genes sejam vogais: distribui normalmente (sorteio)
        if pai_eh_vogal and mae_eh_vogal:
            if random.choice([True, False]):
                filho1.append(gene_pai)
                filho2.append(gene_mae)
            else:
                filho1.append(gene_mae)
                filho2.append(gene_pai)

            vogal_filho1 += 1
            vogal_filho2 += 1

        # Se só o pai tem vogal
        elif pai_eh_vogal and not mae_eh_vogal:
            # Se filho1 ainda não tem vogal, ele recebe a vogal do pai
            if vogal_filho1 == 0:
                filho1.append(gene_pai)
                filho2.append(gene_mae)
                vogal_filho1 += 1
            # Caso contrário filho2 recebe a vogal, filho1 o outro gene
            elif vogal_filho2 == 0:
                filho1.append(gene_mae)
                filho2.append(gene_pai)
                vogal_filho2 += 1
            else:
                # Ambos tem vogal, pode distribuir aleatoriamente
                if random.choice([True, False]):
                    filho1.append(gene_pai)
                    filho2.append(gene_mae)
                else:
                    filho1.append(gene_mae)
                    filho2.append(gene_pai)

        # Se só a mãe tem vogal (mesma lógica)
        elif mae_eh_vogal and not pai_eh_vogal:
            if vogal_filho1 == 0:
                filho1.append(gene_mae)
                filho2.append(gene_pai)
                vogal_filho1 += 1
            elif vogal_filho2 == 0:
                filho1.append(gene_pai)
                filho2.append(gene_mae)
                vogal_filho2 += 1
            else:
                if random.choice([True, False]):
                    filho1.append(gene_pai)
                    filho2.append(gene_mae)
                else:
                    filho1.append(gene_mae)
                    filho2.append(gene_pai)

        # Nenhum gene é vogal, troca normal
        else:
            if random.choice([True, False]):
                filho1.append(gene_pai)
                filho2.append(gene_mae)
            else:
                filho1.append(gene_mae)
                filho2.append(gene_pai)

    return filho1, filho2


###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto, garantindo ao menos uma vogal por indivíduo.

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes
    """
    vogais = {"a", "e", "i", "o", "u"}

    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            # Contar vogais no indivíduo
            indices_vogais = [i for i, letra in enumerate(individuo) if letra.lower() in vogais]
            
            
            tentativas = 0
            while True:
                    gene = random.randint(0, len(individuo) - 1)
                    
                    # Se há apenas uma vogal e o gene sorteado é ela, rejeita
                    if len(indices_vogais) == 1 and gene == indices_vogais[0]:
                        tentativas += 1
                        if tentativas > 100:
                            break  # evita loop infinito
                        continue
                    
                    # Realiza o salto
                    valor_gene = individuo[gene]
                    indice_letra = valores_possiveis.index(valor_gene)
                    indice_letra += random.choice([1, -1])
                    indice_letra %= len(valores_possiveis)
                    
                    nova_letra = valores_possiveis[indice_letra]

                    # Verifica se após a troca, ainda há ao menos uma vogal
                    if len(indices_vogais) > 1 or nova_letra.lower() in vogais:
                        individuo[gene] = nova_letra
                        break
        

            
def mutacao_simples(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação simples no problema do palíndromo, evitando que, se existe apenas uma vogal, ela seja mutada.

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes
    """

    vogais = {"a", "e", "i", "o", "u"}

    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            indices_vogais = [i for i, letra in enumerate(individuo) if letra.lower() in vogais]

            tentativas = 0
            while True:
                gene = random.randint(0, len(individuo) - 1)

                # Se há apenas uma vogal e o gene sorteado é ela, rejeita
                if len(indices_vogais) == 1 and gene == indices_vogais[0]:
                    tentativas += 1
                    if tentativas > 10:
                        break  # evita loop infinito
                    continue

                # Realiza a mutação
                valor_gene = individuo[gene]
                valores_sorteio = set(valores_possiveis) - set([valor_gene])
                nova_letra = random.choice(list(valores_sorteio))

                # Verifica se após a troca, ainda há ao menos uma vogal
                if len(indices_vogais) > 1 or nova_letra.lower() in vogais:
                    individuo[gene] = nova_letra
                    break

        

            

def migracao(populacoes, num_migrantes):
    NUM_ILHAS = len(populacoes)
    migrantes_por_ilha = []
    
    # Seleciona migrantes de cada ilha
    for i in range(NUM_ILHAS):
        fitness = funcao_objetivo_pop_palindromo(populacoes[i])
        # seleciona os melhores migrantes (por exemplo)
        indices_melhores = sorted(range(len(fitness)), key=lambda x: fitness[x])[:num_migrantes]
        migrantes = [populacoes[i][idx] for idx in indices_melhores]
        migrantes_por_ilha.append(migrantes)
    
    # Envia migrantes para ilha vizinha (circular)
    for i in range(NUM_ILHAS):
        ilha_destino = (i + 1) % NUM_ILHAS
        # substitui os piores da ilha destino por migrantes da ilha i
        fitness_destino = funcao_objetivo_pop_palindromo(populacoes[ilha_destino])
        indices_piores = sorted(range(len(fitness_destino)), key=lambda x: fitness_destino[x], reverse=True)[:num_migrantes]
        
        for idx, migrante in zip(indices_piores, migrantes_por_ilha[i]):
            populacoes[ilha_destino][idx] = migrante
