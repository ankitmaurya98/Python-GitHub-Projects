# Created 5/2/2021

# This is the Matrix module that needs to be imported into the main file in order to create matrix object

 # This is a module that can be used to work with matrices:
 # 		The user has to input:
 # 			The number of rows in the matrix
 # 			The number of columns in the matrix
 # 			The elements of the matrix
 #
 # 		The functions that can then be called upon are:
 # 			getRows() - which returns the number of rows in the matrix
 # 			getColumns() - which returns the number of columns in the matrix
 # 			getMatrix() - this returns the matrix data member from the Matrix class (returns the vector of vectors)
 # 			printMatrix() - prints the matrix to the console
 # 			setElement() - which sets the elements of the matrix at a particular position
 # 			addMatrix() - which adds 2 matrices together
 # 			multiplyMatrix() - which multiplies 2 matrices together
 # 			subtractMatrix() - which subtracts 2 matrices together
 # 			transposeMatrix() - which returns the transpose of a matrix

# Defining the Matrix class
class Matrix:
    _rows = 0
    _columns = 0
    _matrix = []
    
    # Constructor method
    def __init__(self, rows, columns, matrix):
        # Inputs: 
        #       rows = number of rows in the matrix
        #       columns = number of columns in the matrix
        #       matrix = a nested list that represents the matrix
        
        self._rows = rows
        self._columns = columns
        self._matrix = matrix
        
    # getRows() function
    def getRows(self):
        # Inputs:
        #       None
        # Outputs:
        #       Returns the number of rows in the matrix
        return self._rows
    
    # getColumns() function
    def getColumns(self):
        # Inputs:
        #       None
        # Outputs:
        #       Returns the number of columns in the matrix
        return self._columns
    
    # getMatrix() function
    def getMatrix(self):
        # Inputs:
        #       None
        # Outputs:
        #       Returns the nested list form of the matrix
        return self._matrix
    
    # printMatrix() function
    def printMatrix(self):
        # Inputs:
        #       None
        # Outputs:
        #       No return statement so will return a None value
        #       However, it will print out the matrix in row, column format
        
        for i in range(self.getRows()):
            for j in range(self.getColumns()):
                print('{}  '.format(self._matrix[i][j]), end="")
            print(' ')  
        print(' ')
    
    # setElement() function
    def setElement(self, i, j, val):
        # Inputs:
        #       i = row index for element
        #       j = column index for element
        #       val = new value that will be placed at the specified index
        # Outputs:
        #       No return statement so will return a None value
        #       However, it will set the new value at the specified index in the _matrix data member
        
        self._matrix[i][j] = val
    
    # addMatrix() function
    def addMatrix(self, matB):
        # Inputs:
        #       Matrix object that will be added to the Matrix object that this method is being called upon
        # Outputs:
        #       Returns a new Matrix object of the resultant matrix
        
        addedMat = [[None] * self.getColumns() for i in range(self.getRows())]   # Creating a buffer list that will store the new values
        
        for i in range(self.getRows()):
            for j in range(self.getColumns()):
                addedMat[i][j] = self._matrix[i][j] + matB._matrix[i][j]
               
        return Matrix(self.getRows(), self.getColumns(), addedMat)
    
     
    # subtractMatrix() function
    def subtractMatrix(self, matB):
        # Inputs:
        #       Matrix object that will be subtracted to the Matrix object that this method is being called upon
        # Outputs:
        #       Returns a new Matrix object of the resultant matrix
        
        subtractedMat = [[None] * self.getColumns() for i in range(self.getRows())]   # Creating a buffer list that will store the new values
        
        for i in range(self.getRows()):
            for j in range(self.getColumns()):
                subtractedMat[i][j] = self._matrix[i][j] - matB._matrix[i][j]
               
        return Matrix(self.getRows(), self.getColumns(), subtractedMat)
    
    
    # multiplyMatrix() function
    def multiplyMatrix(self, matB):
        # Inputs:
        #       Matrix object that will be multiplied with the Matrix object that this method is being called upon
        # Outputs:
        #       Returns a new Matrix object of the resultant matrix
        
        multipliedMat = [[0] * matB.getColumns() for i in range(self.getRows())]   # Creating a buffer list that will store the new values
        
        #Performing check to see if the matrix dimensions are correct in order to perform multiplication
        if self.getColumns() == matB.getRows():
            for i in range(self.getRows()):
                for j in range(matB.getColumns()):
                    for k in range(self.getColumns()):
                        multipliedMat[i][j] = multipliedMat[i][j] + (self._matrix[i][k]*matB._matrix[k][j])  
        else:
            print('Matrix dimensions are not correct. Please check the rows and columns')
        
        return Matrix(self.getRows(), matB.getColumns(), multipliedMat)
    
    
    # transposeMatrix() function
    def transposeMatrix(self):
        # Inputs:
        #       None
        # Outputs:
        #       Returns a new Matrix object of the transposed matrix
        
        transposedMat = [[None] * self.getRows() for i in range(self.getColumns())]   # Creating a buffer list that will store the new values
        
        for i in range(self.getRows()):
            for j in range(self.getColumns()):
                transposedMat[j][i] = self._matrix[i][j]
               
        return Matrix(self.getColumns(), self.getRows(), transposedMat)
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
# Identity matrix function that can be called to create an identity matrix
def identityMatrix(val):
    # Inputs:
    #       Size of the matrix you want. Example, passing in 3 returns a 2 x 2 identity matrix
    # Outputs:
    #       Returns a new Matrix object of an identity matrix of the specified size
    
    identityMat = [[0] * val for i in range(val)]   # Creating a buffer list that will store the new values
    for i in range(val):
        for j in range(val):
            if i == j:
                identityMat[i][j] = 1
        
    return Matrix(val, val, identityMat)
