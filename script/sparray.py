import numpy


class sparray(object):
    def __init__(self, shape, default=0, dtype=bool):
        
        self.__default = default
        self.shape = tuple(shape)
        self.ndim = len(shape)
        self.dtype = bool
        self.__data = {}

    def __setitem__(self, index, value):
        self.__data[index] = value

    def __getitem__(self, index):
        return self.__data.get(index,self.__default)

B = sparray((150000000,150000000,150000000,150000000))
for i in range (0,100):
    for j in range (0,150000):
        B[i,j,i,i] = True