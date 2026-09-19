# https://www.deep-ml.com/problems/17

# https://claude.ai/share/06dabf00-ee09-4743-8a25-e4631bbf2903

import math

def euclidean_distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    """
    Calcula la distancia euclidiana entre dos puntos de cualquier dimensión.

    Args:
        a: Coordenadas del primer punto.
        b: Coordenadas del segundo punto (misma dimensión que a).

    Returns:
        Distancia euclidiana como float.
    """
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def assign_points(
    points: list[tuple[float, ...]],
    centroids: list[tuple[float, ...]],
) -> tuple[list[int], list[int], list[list[float]]]:
    """
    Asigna cada punto al centroide más cercano y acumula estadísticas por clúster.

    Args:
        points: Lista de puntos (tuplas de igual dimensión).
        centroids: Lista de centroides actuales.

    Returns:
        Tupla (asignaciones, conteos, sumas):
          - asignaciones: asignaciones[i] = índice del centroide del punto i.
          - conteos: conteos[j] = cantidad de puntos del clúster j.
          - sumas: sumas[j] = suma por coordenada de los puntos del clúster j.

    Notas:
        En empates de distancia gana el centroide de menor índice
        (por la comparación estricta `<`).
    """
    k = len(centroids)
    dim = len(points[0])

    assignments: list[int] = []
    counts = [0] * k
    sums = [[0.0] * dim for _ in range(k)]

    for point in points:
        best_dist = math.inf
        best_idx = -1

        for idx, centroid in enumerate(centroids):
            dist = euclidean_distance(point, centroid)
            if dist < best_dist:
                best_dist = dist
                best_idx = idx

        assignments.append(best_idx)
        counts[best_idx] += 1
        for d, coord in enumerate(point):
            sums[best_idx][d] += coord

    return assignments, counts, sums


def update_centroids(
    sums: list[list[float]],
    counts: list[int],
    previous_centroids: list[tuple[float, ...]],
) -> list[tuple[float, ...]]:
    """
    Calcula los nuevos centroides como la media de los puntos asignados.

    Args:
        sums: Suma por coordenada de los puntos de cada clúster.
        counts: Cantidad de puntos de cada clúster.
        previous_centroids: Centroides de la iteración anterior.

    Returns:
        Lista de nuevos centroides (tuplas). Un clúster vacío conserva su
        centroide anterior para evitar división por cero.
    """
    new_centroids: list[tuple[float, ...]] = []

    for cluster_sum, count, previous in zip(sums, counts, previous_centroids):
        if count == 0:
            new_centroids.append(previous)
        else:
            new_centroids.append(tuple(coord / count for coord in cluster_sum))

    return new_centroids


def k_means_clustering(
    points: list[tuple[float, ...]],
    k: int,
    initial_centroids: list[tuple[float, ...]],
    max_iterations: int,
) -> list[tuple[float, ...]]:
    """
    Implementa el algoritmo k-Means.

    Args:
        points: Puntos a agrupar (tuplas de igual dimensión).
        k: Número de clústeres.
        initial_centroids: k centroides iniciales.
        max_iterations: Máximo de iteraciones.

    Returns:
        Lista de k centroides finales, cada coordenada redondeada a 4 decimales.

    Raises:
        ValueError: si points está vacío, si len(initial_centroids) != k
            o si las dimensiones no coinciden.
    """
    if not points:
        raise ValueError("points no puede estar vacío")
    if len(initial_centroids) != k:
        raise ValueError("len(initial_centroids) debe ser igual a k")

    dim = len(points[0])
    if any(len(p) != dim for p in points) or any(len(c) != dim for c in initial_centroids):
        raise ValueError("Todos los puntos y centroides deben tener la misma dimensión")

    # Lista nueva: la entrada nunca se muta (las tuplas son inmutables).
    centroids = list(initial_centroids)
    previous_assignments = None

    for _ in range(max_iterations):
        assignments, counts, sums = assign_points(points, centroids)

        # Ningún punto cambió de clúster -> los centroides ya son la media de sus grupos.
        if assignments == previous_assignments:
            break

        centroids = update_centroids(sums, counts, centroids)
        previous_assignments = assignments

    # Redondeo solo al final.
    return [tuple(round(coord, 4) for coord in c) for c in centroids]
