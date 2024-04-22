import pulp

Big = 1e8

M = 1 # Número de cursos
N = 2 # Número de asignaturas
F = [1, 2, 3] # Días no válidos para asignar pruebas (feriados, fin de semana)
V = [[(1, 5), (2, 19)]] # Plazos para realizar las pruebas
K = [[1, 2]] # Carga de trabajo de las asignaturas
Di = [20] # Días del curso

# Crear el problema
prob = pulp.LpProblem ("Programacion_Examenes", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts ("x", ((i, j) for i in range (M) for j in range (N)), lowBound = 0, cat = pulp.LpInteger)
E = pulp.LpVariable.dicts ("E", ((i, j, k) for i in range (M) for j in range (N) for k in range (Di [i])), cat = pulp.LpBinary)

prob += pulp.lpSum (E [(i, j, k)] * (K [i][j] / (V [i][j][1] - V [i][j][0])) for i in range (M) for j in range (N) for k in range (Di[i]))

# Restricciones
for i in range (M):

    for j in range (N):

        prob += x [(i, j)] >= V [i][j][0]
        prob += x [(i, j)] <= V [i][j][1]

        for f in F:

            prob += x [(i, j)] != f

for i in range (M):

    for j in range (N):

        for k in range (Di [i]):

            prob += x [(i, j)] <= k + Big * (1 - E [(i, j, k)])
            prob += x [(i, j)] >= k - Big * E [(i, j, k)]

print (prob)

import os
os._exit(0)
# Resolver el problema
prob.solve()

# Imprimir el resultado
print("Estado:", pulp.LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Costo total =", pulp.value(prob.objective))
