#Dependencias: numpy as np, pandas as pd.
def cld_piepho(tukey):
    total_grupos = len(tukey.groupsunique)

    # Crear un DataFrame vacío con una matriz cuadrada del tamaño de los grupos
    # La primera columna se inicializa en 1
    matriz_letras = pd.DataFrame(np.nan, index=np.arange(total_grupos), columns=np.arange(total_grupos), dtype=object)
    matriz_letras.iloc[:, 0] = 1

    contador = 0
    # Crear un DataFrame para almacenar los nombres de los grupos
    nombres_grupos = pd.DataFrame(tukey.groupsunique, index=np.arange(total_grupos), columns=['grupo'])

    # Comparación por pares entre los grupos
    for i in np.arange(total_grupos):
        for j in np.arange(i + 1, total_grupos):
            if tukey.reject[contador]:  # Si hay diferencia significativa entre los grupos
                for columna in np.arange(total_grupos):
                    if matriz_letras.iloc[i, columna] == 1 and matriz_letras.iloc[j, columna] == 1:
                        matriz_letras = pd.concat([matriz_letras.iloc[:, :columna + 1], matriz_letras.iloc[:, columna + 1:].T.shift().T], axis=1)
                        matriz_letras.iloc[:, columna + 1] = matriz_letras.iloc[:, columna]
                        matriz_letras.iloc[i, columna] = 0
                        matriz_letras.iloc[j, columna + 1] = 0
                    
                    # Verificar columnas para absorción
                    for izquierda in np.arange(len(matriz_letras.columns) - 1):
                        for derecha in np.arange(izquierda + 1, len(matriz_letras.columns)):
                            if matriz_letras.iloc[:, izquierda].notna().any() and matriz_letras.iloc[:, derecha].notna().any():
                                if (matriz_letras.iloc[:, izquierda] >= matriz_letras.iloc[:, derecha]).all():
                                    matriz_letras.iloc[:, derecha] = 0
                                    matriz_letras = pd.concat([matriz_letras.iloc[:, :derecha], matriz_letras.iloc[:, derecha:].T.shift(-1).T], axis=1)
                                if (matriz_letras.iloc[:, izquierda] <= matriz_letras.iloc[:, derecha]).all():
                                    matriz_letras.iloc[:, izquierda] = 0
                                    matriz_letras = pd.concat([matriz_letras.iloc[:, :izquierda], matriz_letras.iloc[:, izquierda:].T.shift(-1).T], axis=1)
            contador += 1

    # Ordenar las columnas para que la primera columna tenga la letra 'a'
    matriz_letras = matriz_letras.sort_values(by=list(matriz_letras.columns), axis=1, ascending=False)

    # Asignar letras a cada columna
    for columna in np.arange(len(matriz_letras.columns)):
        matriz_letras.iloc[:, columna] = matriz_letras.iloc[:, columna].replace(1, chr(97 + columna)) 
        matriz_letras.iloc[:, columna] = matriz_letras.iloc[:, columna].replace(0, '')
        matriz_letras.iloc[:, columna] = matriz_letras.iloc[:, columna].replace(np.nan, '')

    # Convertir la matriz a tipo string y concatenar las letras en una sola cadena
    matriz_letras = matriz_letras.astype(str)
    resultado_final = matriz_letras.sum(axis=1)

    # Crear un DataFrame con los grupos y sus respectivas letras
    resultado_df = pd.DataFrame({'Grupo': nombres_grupos['grupo'], 'Letras': resultado_final})
    
    return resultado_df