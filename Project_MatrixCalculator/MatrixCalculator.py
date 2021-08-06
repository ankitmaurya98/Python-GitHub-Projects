# Created 5/2/2021


# This is the main file that contains the test cases for the matrix module


 # This is a program that can be used to work with matrices:
 # 		The user has to input:
 # 			The number of rows in the matrix
 # 			The number of columns in the matrix
 # 			The elements of the matrix. The format is a nested list where each list inside the overall list is a new row
 #              Example: x = [[1,2,3], [4,5,6]] This is a 2 x 3 matrix where the [1,2,3] are the first row and [4,5,6] are the second
 #
 # 		The functions that can then be called upon are:
 # 			getRows() - which returns the number of rows in the matrix
 # 			getColumns() - which returns the number of columns in the matrix
 # 			getMatrix() - this returns the matrix data member from the Matrix class (returns the vector of vectors)
 # 			printMatrix() - prints the matrix to the console
 # 			setElement() - which sets the elements of the matrix at a particular position
 # 			addMatrix() - which adds 2 matrices together
 # 			subtractMatrix() - which subtracts 2 matrices together
 # 			multiplyMatrix() - which multiplies 2 matrices together
 # 			transposeMatrix() - which returns the transpose of a matrix
 #          identityMatrix() - returns an identity matrix of specified size (This is outside the Matrix Class, but still in the Matrix module)


import Matrix       # importing the Matrix module that we have created


# How a nested list works
#x = [[1,2,3],[4,5,6]]
#y = x[1]
#z = x[1][1]
#print(y)
#print(len(x))
#print(len(y))

# Testing to see how to create a Matrix object using the Matrix module that we created
print('Test 1: Creating Simple Matrix Object')
a = [[1,2,3],[4,5,6]]
matrixA = Matrix.Matrix(2, 3, a)      # Creating matrix object
print(matrixA.getRows())
print(matrixA.getColumns())
matrixA.printMatrix()


#Testing the setElement function
print('Test 2: Testing setElement()')
matrixAa = Matrix.Matrix(2, 3, [[1,2,3],[4,5,6]])
matrixAa.setElement(1,0,21)
matrixAa.printMatrix()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


b = [[1,2,3],[4,5,6]]
matrixB = Matrix.Matrix(2, 3, b)

#Testing the addMatrix Function
print('Test 3: Testing addMatrix()')
addedMatrix = matrixA.addMatrix(matrixB)
addedMatrix.printMatrix()

#Testing the subtractMatrix Function
print('Test 4: Testing subtractMatrix()')
subtractedMatrix = matrixA.subtractMatrix(matrixB)
subtractedMatrix.printMatrix()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Testing the multiplyMatrix Function
print('Test 5: Testing multiplyMatrix()')
matrix1 = Matrix.Matrix(2, 2, [[1,2], [3,4]])
matrix2 = Matrix.Matrix(2, 1, [[5], [6]])
multipliedMatrix = matrix1.multiplyMatrix(matrix2)
multipliedMatrix.printMatrix()
matrix3 = Matrix.Matrix(2, 2, [[1,2], [3,4]])
multipliedMatrix2 = matrix1.multiplyMatrix(matrix3)
multipliedMatrix2.printMatrix()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Testing the transposeMatrix Function
print('Test 6: Testing transposeMatrix()')
transposedMatrix = matrixA.transposeMatrix()
matrixA.printMatrix()
transposedMatrix.printMatrix()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('Test 7: Identity Matrix Test')
identityMatrix = Matrix.identityMatrix(3)
identityMatrix.printMatrix()

