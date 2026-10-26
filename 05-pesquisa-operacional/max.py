import pulp

# Parâmetros do problema
investimento_total_x = 60000 
investimento_total_y = 70000 
taxa_retorno_x = 0.08
taxa_retorno_y = 0.12
orcamento_disponivel = 100000

model = pulp.LpProblem(
    "SmartBank_Maximization_Problem", 
    pulp.LpMaximize
)

x = pulp.LpVariable("Investment_X", lowBound=0, upBound=investimento_total_x)
y = pulp.LpVariable("Investment_Y", lowBound=0, upBound=investimento_total_y)

# Função objetivo
model += taxa_retorno_x * x + taxa_retorno_y * y, "Total_Profit"

# Restrições
model += x >= 0, "Investment_X_Lower_Bound"
model += y >= 0, "Investment_Y_Lower_Bound"
model += x + y <= orcamento_disponivel, "Total_Investment_Limit"

model.solve()

print("Status:", pulp.LpStatus[model.status])
print("Melhor investimento em X:", x.varValue)
print("Melhor investimento em Y:", y.varValue)
print("Lucro total:", pulp.value(model.objective))

