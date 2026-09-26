from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

from func import *
from ext1 import *
from ext2 import *


# Base implementation
gramatica = cargar_gramatica(DATA_DIR / 'cnf_input.txt')

for g in gramatica:
    print()
    print()
    print(f"Gramatica {g}:")
    print(f"Reglas: {gramatica[g]['reglas']}")

    print()
    print(f"Esta en forma normal de Chomsky (CNF): {es_cnf(gramatica[g]['reglas'])}")

    if not es_cnf(gramatica[g]['reglas']):
        print("Convertida a CNF:")
        g = convertir_cnf(gramatica[g]['reglas'])
        print(g)

    for palabra in gramatica[g]['palabras']:
        print(f" Pertenece la palabra {palabra} a la gramatica {g}: {cky(gramatica[g]['reglas'], palabra)}")


# Extension 1: CNF conversion
print()
print()
print('*' * 50)
print('Extension 1')
print('*' * 50)

gramatica_ext1 = cargar_gramatica(DATA_DIR / 'ext1_input.txt')
print(gramatica_ext1)

for g in gramatica_ext1:
    print()
    print()
    print(f"Gramatica {g}:")
    print(f"Reglas: {gramatica_ext1[g]['reglas']}")

    print()
    print(f"Esta en forma normal de Chomsky (CNF): {es_cnf(gramatica_ext1[g]['reglas'])}")

    if not es_cnf(gramatica_ext1[g]['reglas']):
        print("Convertida a CNF:")
        gmod = convertir_cnf(gramatica_ext1[g]['reglas'])
        print(gmod)



# Extension 2: probabilistic CKY
print()
print()
print('*' * 50)
print('Extension 2')
print('*' * 50)

gramatica_ext2 = cargar_gramatica2(DATA_DIR / 'ext2_input.txt')

for g in gramatica_ext2:
    print()
    print()
    print(f"Gramatica {g}:")
    print(f"Reglas: {gramatica_ext2[g]['reglas']}")

    for palabra in gramatica_ext2[g]['palabras']:
        print(f" Pertenece la palabra {palabra} a la gramatica {g}: {cky_probabilistico(gramatica_ext2[g]['reglas'], palabra)}")