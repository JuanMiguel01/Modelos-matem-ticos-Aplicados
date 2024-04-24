from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

# Definir el problema
prob = LpProblem("Programacion_Examenes", LpMinimize)

#Variables de decisión
M = 2 #Número de cursos
N = [3, 3] #Número de asignaturas por curso
F = [[[1, 2, 3,4,6,7,8,9], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]]] #Días no válidos para asignar pruebas por curso, asignatura y evaluación
V = [[[(1, 5), (6, 10), (11, 15)], [(16, 20), (21, 25), (26, 30)], [(1, 5), (6, 10), (11, 15)]], [[(1, 5), (6, 10), (11, 15)], [(16, 20), (21, 25), (26, 30)], [(1, 5), (6, 10), (11, 15)]]] # Ajustado para que no excedan los 30 días
K = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]]] # Carga de trabajo de las asignaturas por curso, asignatura y evaluación
Di = [30] # Días del curso
'''
M=1
N=[3]
F=[[[1, 2, 3,4], [4, 5, 6], [7, 8, 9]]]
V=[[[(1, 5), (6, 10), (11, 15)], [(1, 5), (6, 10), (11, 15)], [(1, 5), (6, 10), (11, 15)]]]
K=[[[1, 2, 3], [7], [11, 13]]]
Di=[15]'''

# Crear variables de decisión
x = LpVariable.dicts("x", ((i, j, e, k) for i in range(M) for j in range(N[i]) for e in range(len(F[i][j])) for k in range(Di[0])), cat='Binary')

# Función objetivo
prob += lpSum([K[i][j][e] * x[(i, j, e, k)] for i in range(M) for j in range(N[i]) for e in range(len(K[i][j])) for k in range(Di[0])])

# Restricciones
for i in range(M):
    for j in range(N[i]):
        for e in range(len(K[i][j])): # Asegúrate de que 'e' itere sobre el rango correcto
            prob += lpSum([x[(i, j, e, k)] for k in range(Di[0])]) == 1

# Restricción para evitar que dos exámenes de la misma asignatura se asignen al mismo día
for i in range(M):
    for j in range(N[i]):
        for k in range(Di[0]):
            prob += lpSum([x[(i, j, e, k)] for e in range(len(F[i][j]))]) <= 1

# Restricción de que no se pueden programar exámenes en días no válidos o fuera de los plazos
for i in range(M):
    for j in range(N[i]):
        for e in range(len(V[i][j])):
            for k in range(Di[0]):
                print(i,j,e)
                
                print(V[i][j][e])
                if k in F[i][j] or (k < V[i][j][e][0] or k > V[i][j][e][1]):
                    print(f"Examen {e} de la asignatura {j} del curso {i} no se puede asignar al día {k}")
                    prob += x[(i, j, e, k)] == 0

# Resolver el problema
prob.solve()

# Imprimir el estado del problema
print("Estado:", LpStatus[prob.status])

# Imprimir el valor de la función objetivo
print("Valor objetivo =", value(prob.objective))

# Imprimir la asignación de exámenes
for i in range(M):
    for j in range(N[i]):
        for e in range(len(F[i][j])):
            for k in range(Di[0]):
                if value(x[(i, j, e, k)]) == 1:
                    print(f"Examen {e} de la asignatura {j} del curso {i} se asigna al día {k}")
