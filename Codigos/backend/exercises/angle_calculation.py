"""
@file angle_calculation.py
@brief Fornece uma função para calcular o ângulo entre três pontos 2D.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import math

def calculate_angle(a, b, c):
    """Calcula o ângulo formado por três pontos (a, b, c), com 'b' sendo o vértice.

    A função calcula o ângulo usando o produto escalar dos vetores BA e BC.
    Garante que o valor do cosseno esteja no intervalo [-1.0, 1.0] para evitar
    erros de domínio matemático.

    :param (list) a: As coordenadas [x, y] do primeiro ponto.
    :param (list) b: As coordenadas [x, y] do ponto do vértice.
    :param (list) c: As coordenadas [x, y] do terceiro ponto.
    :return (float): O ângulo em graus, variando de 0 a 180. Retorna 0 se um dos vetores for nulo.
    """
    # Calcula os vetores BA (de B para A) e BC (de B para C)
    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]

    # Produto escalar dos vetores
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]

    # Magnitude (comprimento) dos vetores
    magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    # Evita divisão por zero se um dos pontos for coincidente com o vértice
    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    # Calcula o cosseno do ângulo
    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

    # Garante que o valor esteja no intervalo [-1, 1] para a função acos
    cosine_angle = max(min(cosine_angle, 1.0), -1.0)
    
    # Converte o ângulo de radianos para graus
    angle = math.degrees(math.acos(cosine_angle))
    return angle
