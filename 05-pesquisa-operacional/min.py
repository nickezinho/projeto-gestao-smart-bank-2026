import pulp as pl

modelo = pl.LpProblem("Minimizacao_Cloud", pl.LpMinimize)


sp_aws = modelo.add_variable("SP_AWS", lowBound=0)
sp_azure = modelo.add_variable("SP_Azure", lowBound=0)

rj_aws = modelo.add_variable("RJ_AWS", lowBound=0)
rj_azure = modelo.add_variable("RJ_Azure", lowBound=0)

cwb_aws = modelo.add_variable("CWB_AWS", lowBound=0)
cwb_azure = modelo.add_variable("CWB_Azure", lowBound=0)


modelo += (
    15 * sp_aws + 12 * sp_azure +
    10 * rj_aws + 14 * rj_azure +
    18 * cwb_aws + 11 * cwb_azure
)


modelo += sp_aws + sp_azure == 80
modelo += rj_aws + rj_azure == 50
modelo += cwb_aws + cwb_azure == 30


modelo += sp_aws + rj_aws + cwb_aws <= 100
modelo += sp_azure + rj_azure + cwb_azure <= 90


resultado = modelo.solve(pl.COIN_CMD(msg=False))


print("Status:", resultado.status_str)

if resultado.status_str == "Optimal":

    print("\nDistribuição das transferências:")

    print("SP -> AWS:", pl.value(sp_aws), "TB")
    print("SP -> Azure:", pl.value(sp_azure), "TB")

    print("RJ -> AWS:", pl.value(rj_aws), "TB")
    print("RJ -> Azure:", pl.value(rj_azure), "TB")

    print("CWB -> AWS:", pl.value(cwb_aws), "TB")
    print("CWB -> Azure:", pl.value(cwb_azure), "TB")

    print(
        "\nCusto mínimo: R$",
        pl.value(modelo.objective)
    )