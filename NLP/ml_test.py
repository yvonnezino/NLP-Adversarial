import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1,1],[1,2],[2,2],[2,3]])

y = np.dot(X,np.array([1,2]))+3

reg = LinearRegression().fit(X,y)

predict = reg.predict(np.array([[3,5]]))

print(predict)