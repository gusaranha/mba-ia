# C#/Java/PHP usam chaves {}
# Python usa indentação (4 espaços)

if True:
    print("Isso está dentro do bloco if")
    print("Também está dentro do bloco if")
print("Isso está fora do bloco if")


# Java: public int somar(int a, int b) { return a + b; }
# Python:
def somar(a,b):
    return a + b


def somar_tipado(a: int, b: int) -> int:
    return a + b


# C#: for (int i = 0; i < 10; i++)
# Python:
for i in range(10):
    print(i)

# C#: foreach (var item in lista)
# Python:
for item in numeros:
    print(item)

# Java: public class Pessoa { }
# Python:
class Pessoa:
    def __init__(self, nome):
        self.nome = nome

    def apresentar(self):
        print(f"Olá, meu nome é {self.nome}.")

# Ao invés de loop tradicional
quadrados = []
for n in range(10):
    quadrados.append(n ** 2)

# Usando list comprehension
quadrados = [n ** 2 for n in range(10)]

# Equivalente a "using" em C#
# Fecha arquivo automaticamente
with open("arquivo.txt", "r") as arquivo:
    conteudo = arquivo.read()
    print(conteudo)

# === MÚLTIPLA ATRIBUIÇÃO ===
a, b, c = 1, 2, 3

a, b = b, a  # troca valores