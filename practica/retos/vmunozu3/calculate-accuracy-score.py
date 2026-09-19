# Link del reto: https://www.deep-ml.com/problems/36

import numpy as np

def accuracy_score(y_true, y_pred):
    predicciones_correctas = np.sum(y_true == y_pred)
    total_predicciones = len(y_true)
    accuracy = predicciones_correctas / total_predicciones
    return float(accuracy)