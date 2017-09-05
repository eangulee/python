# reference:https://uqer.io/community/share/54ca15f9f9f06c276f651a56

import numpy as np
import numpy.linalg as nlg
'''
# 求逆
print('求逆------------------------------------------')
a = np.random.rand(2,2)
a = np.mat(a)
print("a:")
print(a)
ia = nlg.inv(a)
print("inverse of a:")
print(ia)
print("a * inv(a)")
print(a * ia)
'''
'''
# 求转置
print('求转置------------------------------------------')
a = np.random.rand(2,4)
print("a:")
print(a)
a = np.transpose(a)
print("a is an array, by using transpose(a):")
print(a)
b = np.random.rand(2,4)
b = np.mat(b)
print("b:")
print(b)
print("b is a matrix, by using b.T:")
print(b.T)
'''
'''
# 求特征值和特征向量
a = np.random.rand(3,3)
eig_value, eig_vector = nlg.eig(a)
print("eigen value:")
print(eig_value)
print("eigen vector:")
print(eig_vector)
'''

'''
# 按列拼接两个向量成一个矩阵
a = np.array((1,2,3))
b = np.array((2,3,4))
print(np.column_stack((a,b)))

# 在循环处理某些数据得到结果后，将结果拼接成一个矩阵是十分有用的，可以通过vstack和hstack完成：
a = np.random.rand(2,2)
b = np.random.rand(2,2)
print("a:")
print(a)
print("b:")
print(a)
c = np.hstack([a,b])
d = np.vstack([a,b])
print("horizontal stacking a and b:")
print(c)
print("vertical stacking a and b:")
print(d)
'''

