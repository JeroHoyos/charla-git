# Link del reto: https://www.deep-ml.com/problems/1137

def top_three_largest(values):
    # values: list of numbers
    # return the three largest values in descending order
    aux = []
    
    for i in range(0, 3, 1):
        aux.append(max(values))
        values.remove(max(values))
  
    return aux