import scipy.sparse as sparse
import numpy as np

matrix = sparse.dok_matrix((400, 400), dtype=object)
is_init = sparse.dok_matrix((400, 400), dtype=bool)

for i in range(1000):
    x = np.random.randint(0, 400)
    y = np.random.randint(0, 400)
    w = np.random.randint(0, 400)
    z = np.random.randint(0, 400)
    if not is_init[x,y]:
        is_init[x,y] = True
        matrix[x,y] = sparse.dok_matrix((400, 400), dtype=bool)
    matrix[x,y][w,z] = True