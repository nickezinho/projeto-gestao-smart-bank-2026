
from scipy.optimize import linprog

def minimizar(custos, nome):
    # Custos de transporte
    objetivo = [
        custos[0][0], custos[0][1], custos[0][2],
        custos[1][0], custos[1][1], custos[1][2],
        custos[2][0], custos[2][1], custos[2][2]
    ]

    # Limites de oferta
    oferta = [120, 80, 100]

    # Demandas
    demanda = [100, 70, 130]

    # Restrições de oferta
    A = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1]
    ]

    # Restrições de demanda
    A_eq = [
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1]
    ]

    resultado = linprog(
        objetivo,
        A_ub=A,
        b_ub=oferta,
        A_eq=A_eq,
        b_eq=demanda,
        bounds=(0, None),
        method="highs"
    )

    print("\nCENÁRIO:", nome)

    if resultado.success:
        print("Distribuição das unidades:")

        nomes = [
            "SP -> Osasco", "SP -> Barueri", "SP -> Santos",
            "Campinas -> Osasco", "Campinas -> Barueri",
            "Campinas -> Santos",
            "Jundiaí -> Osasco", "Jundiaí -> Barueri",
            "Jundiaí -> Santos"
        ]

        for i in range(9):
            if resultado.x[i] > 0.001:
                print(f"{nomes[i]}: {resultado.x[i]:.0f} unidades")

        print(f"Custo mínimo: R$ {resultado.fun:.2f}")
        return resultado.fun

    else:
        print("Não foi possível encontrar uma solução.")
        return None


# CENÁRIO NORMAL
custos_normais = [
    [8, 6, 10],
    [9, 7, 11],
    [7, 9, 8]
]

custo_normal = minimizar(custos_normais, "Normal")


# CENÁRIO WHAT-IF
# A rota SP -> Barueri passa de R$ 6 para R$ 12
custos_alternativos = [
    [8, 12, 10],
    [9, 7, 11],
    [7, 9, 8]
]

custo_alternativo = minimizar(custos_alternativos, "What-If")


# COMPARAÇÃO
if custo_normal is not None and custo_alternativo is not None:
    print("\nCOMPARAÇÃO DOS CENÁRIOS")
    print(f"Custo normal: R$ {custo_normal:.2f}")
    print(f"Custo What-If: R$ {custo_alternativo:.2f}")
    print(f"Diferença: R$ {custo_alternativo - custo_normal:.2f}")
