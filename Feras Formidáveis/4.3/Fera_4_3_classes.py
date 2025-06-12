import random
import math
# pandas, numpy, sklearn não são usados diretamente nas classes Valor, Neuronio, Camada, MLP que você mostrou,
# mas podem ser usados para carregar e preparar os dados antes.

class Valor:
    def __init__(self, data, parents=(), op=""):
        self.data = data
        self.parents = parents
        self.op = op
        self.grad = 0.0
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Valor) else Valor(other)
        out = Valor(self.data + other.data, (self, other), "+")
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Valor) else Valor(other)
        out = Valor(self.data * other.data, (self, other), "*")
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def exp(self):
        e = math.exp(self.data)
        out = Valor(e, (self,), "exp")
        def _backward():
            self.grad += e * out.grad
        out._backward = _backward
        return out

    def log(self):
        eps = 1e-15 # Evitar log(0)
        x_data = max(self.data, eps)
        out = Valor(math.log(x_data), (self,), "log")
        def _backward():
            # Certifique-se que x_data não é zero para evitar divisão por zero no gradiente
            self.grad += (1.0 / x_data if x_data != 0 else float('inf')) * out.grad
        out._backward = _backward
        return out

    def __pow__(self, power):
        assert not isinstance(power, Valor), "A potência não pode ser um objeto Valor para __pow__"
        # Lidar com 0 elevado a potência negativa que resulta em infinito
        if self.data == 0 and power < 0:
            # print(f"Aviso: Tentativa de calcular 0^{power}. Retornando Valor(float('inf')).")
            # A abordagem aqui é retornar um valor grande, mas o gradiente pode ser problemático.
            # Alternativamente, poderia lançar um erro ou retornar um Valor especial.
            # No contexto de 1/other, se other for 0, isso será ativado.
            result_data = float('inf')
        else:
            result_data = self.data**power

        out = Valor(result_data, (self,), f"**{power}")

        def _backward():
            grad_local = 0.0
            if self.data == 0:
                if power == 1: grad_local = 1.0 # (0^1)' = 1 * 0^0 (assumindo 0^0 = 1 para gradientes)
                elif power > 1: grad_local = 0.0 # (0^2)' = 2 * 0^1 = 0
                # Se power < 1 (e não 0), ou power == 0, o gradiente é problemático ou infinito.
                # Para 0**power onde power < 0, o gradiente é infinito.
                # Para 0**0, o gradiente é indefinido.
                # Simplificaremos, mas isso pode precisar de tratamento mais robusto.
                elif power < 0: grad_local = float('inf') # Sinal dependeria do out.grad
            elif result_data != float('inf'): # Se não tivemos o caso de 0**negativo
                 # Evitar self.data**(power-1) se self.data for 0 e power-1 < 0
                 if self.data != 0 or (power -1) >= 0:
                    grad_local = power * (self.data**(power - 1))
                 else: # self.data == 0 e power-1 < 0
                    grad_local = float('inf')

            self.grad += grad_local * out.grad
        out._backward = _backward
        return out


    def __neg__(self): return self * -1
    def __sub__(self, other): return self + (-other)
    def __radd__(self, other): return self + other
    def __rmul__(self, other): return self * other

    def __truediv__(self, other):
        other_val = other if isinstance(other, Valor) else Valor(other)
        # if other_val.data == 0:
            # print(f"Aviso: Tentativa de divisão por {other_val.data} em __truediv__")
            # A lógica de 0**-1 em __pow__ será acionada se other_val.data for 0.
        return self * other_val**-1

    def relu(self):
        out = Valor(self.data if self.data > 0 else 0.0, (self,), "relu")
        def _backward():
            self.grad += (1.0 if self.data > 0 else 0.0) * out.grad # Correção: usar self.data para condição
        out._backward = _backward
        return out

    def sig(self):
        # Implementação numericamente mais estável
        if self.data >= 0:
            s_data = 1.0 / (1.0 + math.exp(-self.data))
        else:
            s_data = math.exp(self.data) / (1.0 + math.exp(self.data))
        out = Valor(s_data, (self,), "sig")
        def _backward():
            self.grad += out.data * (1.0 - out.data) * out.grad # out.data é s_data
        out._backward = _backward
        return out

    def backward(self):
        topo = []
        visited = set()
        def build(v):
            if v not in visited:
                visited.add(v)
                for p in v.parents:
                    build(p)
                topo.append(v)
        build(self)
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()

class Neuronio:
    def __init__(self, num_entradas):
        # He initialization para ReLU, ou Xavier/Glorot para Sigmoid.
        # Para Sigmoid, std = math.sqrt(1.0 / num_entradas) seria mais comum.
        # Como a ativação é definida na camada, vamos manter um genérico por enquanto.
        std = math.sqrt(1.0 / num_entradas) if num_entradas > 0 else 1.0
        self.bias = Valor(0.0)
        self.pesos = [Valor(random.uniform(-std, std)) for _ in range(num_entradas)] # Ou random.gauss(0,std)

    def __call__(self, entrada):
        # A ativação será aplicada na Camada
        soma = self.bias # Começa com o bias
        for x_i, w_i in zip(entrada, self.pesos):
            x_val = x_i if isinstance(x_i, Valor) else Valor(x_i)
            soma = soma + x_val * w_i
        return soma

    def params(self):
        return self.pesos + [self.bias]

class Camada:
    def __init__(self, num_neuronios, num_entradas):
        self.neuronios = [Neuronio(num_entradas) for _ in range(num_neuronios)]
        # self.dropout_rate será atribuído pela MLP

    def __call__(self, entrada, use_relu=True, training=False, dropout_rate=0.0):
        saidas_lineares = [neuronio(entrada) for neuronio in self.neuronios]

        if use_relu:
            saidas_ativadas = [s.relu() for s in saidas_lineares]
        else:
            saidas_ativadas = [s.sig() for s in saidas_lineares]

        if training and dropout_rate > 0:
            saidas_com_dropout = []
            prob_manter = 1.0 - dropout_rate
            
            if prob_manter == 0: # Caso extremo de dropout_rate = 1.0
                final_outputs = [Valor(0.0) for _ in saidas_ativadas]
                # VERIFICAÇÃO SIMPLES
                if any(s_orig.data != 0.0 for s_orig in saidas_ativadas):
                    print(f"    [DROPOUT Camada c/ {len(self.neuronios)} neurônios, taxa 1.0] ATIVO: Todos neurônios zerados.")
                return final_outputs[0] if len(final_outputs) == 1 else final_outputs

            escala = Valor(1.0 / prob_manter)
            neuronio_ativo_foi_zerado = False # Flag para verificação

            for i, s_a in enumerate(saidas_ativadas):
                if random.random() < prob_manter:
                    saidas_com_dropout.append(s_a * escala) 
                else:
                    saidas_com_dropout.append(Valor(0.0))
                    if s_a.data != 0.0: # Verifica se um neurônio que estava ativo foi zerado
                        neuronio_ativo_foi_zerado = True
            
            final_outputs = saidas_com_dropout
            
            
        else:
            final_outputs = saidas_ativadas
        
        return final_outputs[0] if len(final_outputs) == 1 else final_outputs

    def params(self):
        return [p for neuronio in self.neuronios for p in neuronio.params()]

class MLP:
    def __init__(self, num_entradas, tamanhos_camadas_config):
        """
        num_entradas: Número de features de entrada.
        tamanhos_camadas_config: Lista de tuplas ou dicionários, onde cada um representa uma camada.
                                 Exemplo: [(16, 0.2), (16, 0.2), (1, 0.0)]
                                 Cada tupla/dict: (num_neuronios, taxa_dropout_para_esta_camada_APÓS_ATIVAÇÃO)
                                 A taxa de dropout da última camada (saída) geralmente é 0.0.
        """
        self.camadas = []
        num_in_atual = num_entradas
        
        for i, config in enumerate(tamanhos_camadas_config):
            if isinstance(config, tuple) and len(config) == 2:
                num_neuronios, taxa_dropout = config
            elif isinstance(config, dict):
                num_neuronios = config['neuronios']
                taxa_dropout = config.get('dropout', 0.0)
            else: # Apenas número de neurônios, dropout padrão 0
                num_neuronios = config
                taxa_dropout = 0.0
            
            camada = Camada(num_neuronios, num_in_atual)
            camada.dropout_rate = taxa_dropout # Armazena a taxa de dropout na camada
            self.camadas.append(camada)
            num_in_atual = num_neuronios


    def __call__(self, entrada, training=False):
        """
        entrada: Lista de valores de entrada (números ou objetos Valor).
        training: Booleano, True para modo de treino.
        """
        x = entrada
        for i, camada in enumerate(self.camadas):
            # ReLU para todas as camadas ocultas, Sigmoid para a camada de saída
            # (assumindo classificação binária ou saída entre 0 e 1 para a última camada)
            use_relu = (i < len(self.camadas) - 1)
            
            # A taxa de dropout já está armazenada no objeto 'camada'
            x = camada(x, use_relu=use_relu, training=training, dropout_rate=camada.dropout_rate)
        return x

    def params(self):
        return [p for camada in self.camadas for p in camada.params()]

def cross_entropy(saidas_reais_batch, saidas_preditas_batch):
    # Assegura que saidas_reais_batch e saidas_preditas_batch são listas de listas/valores
    if not any(isinstance(el, list) for el in saidas_preditas_batch) and isinstance(saidas_preditas_batch[0],Valor) : # Se for lista de Valores (batch de predições únicas)
        saidas_preditas_batch = [[p] for p in saidas_preditas_batch]

    if not any(isinstance(el, list) for el in saidas_reais_batch): # Se for lista de números (batch de rótulos únicos)
         saidas_reais_batch = [[y] for y in saidas_reais_batch]


    soma_perda_total = Valor(0.0)
    num_exemplos_processados = 0

    for y_true_list, y_pred_list in zip(saidas_reais_batch, saidas_preditas_batch):
        if len(y_true_list) != len(y_pred_list):
            raise ValueError(f"Incompatibilidade no número de saídas para um exemplo. Reais: {len(y_true_list)}, Preditas: {len(y_pred_list)}")

        perda_exemplo = Valor(0.0)
        for y_t, y_p in zip(y_true_list, y_pred_list):
            y_true_val = y_t if isinstance(y_t, Valor) else Valor(y_t)
            
            # y_p já deve ser um objeto Valor da saída da rede
            # A classe Valor.log() já tem um épsilon para evitar log(0)
            termo1 = y_true_val * y_p.log()
            termo2 = (Valor(1.0) - y_true_val) * (Valor(1.0) - y_p).log()
            perda_exemplo = perda_exemplo + (termo1 + termo2)
        
        soma_perda_total = soma_perda_total + perda_exemplo
        num_exemplos_processados += 1
    
    if num_exemplos_processados == 0:
        return Valor(0.0)
        
    return soma_perda_total * Valor(-1.0 / num_exemplos_processados)