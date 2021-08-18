# Module that can be used for the book class. This has to be imported to be used in the main file


# Explanation of Functions that are part of the Book class
# 		Constructors:
# 			Book(int code, string name, string author, int qty, int price)-Constructor with all inputs
#
#		Member Functions:
#			getCode() - returns the book code
#			getName() - returns the name of the book
#			getAuthor() - returns the author of the book
#			getQTY() - returns the quantity of the book in inventory
#			getPrice() - returns the price of 1 book
#			inStock() - returns true if book is in stock or false and message if not in stock
#			addBook() - adds a book to inventory
#			addQuantity() - increases the quantity of the book in inventory
#			buyBook() - when user wants to buy book
#			printInventoryList() - makes a text file of all the books and their quantities in inventory
#           exportToExcel() - exports the inventory list into an excel doc


import pandas as pd  # import pandas module for export to Excel


class Book:
    _bookCode = 0;
    _bookName = "No Name"
    _bookAuthor = "No Author"
    _bookQTY = 0;
    _bookPrice = 0;
    
    # Constructor
    def __init__(self, code, name, author, qty, price):
        self._bookCode = code
        self._bookName = name
        self._bookAuthor = author
        self._bookQTY = qty
        self._bookPrice = price
    
    # Getter functions    
    # getCode()
    def getCode(self):
        return self._bookCode
    
    # getName()
    def getName(self):
        return self._bookName
    
    # getAuthor()
    def getAuthor(self):
        return self._bookAuthor
    
    # getQTY()
    def getQTY(self):
        return self._bookQTY
    
    # getPrice()
    def getPrice(self):
        return self._bookPrice
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
# inStock()
def inStock(database, bookID):
    # Input:
    #       database - Database array of objects
    #       bookID - book code used for identification
    # Output:
    #       A true or false and a print statement that prints if the book is in stock
    
    for item in database:
        if item.getCode() == bookID:
            print("Yes the book {} is in stock. There are {} copies available".format(item.getName(), item.getQTY()))
            return True
            
    return False
        
    
# addBook()
def addBook(database):
    # Input:
    #       database - Database array of objects
    # Output:
    #       None - a print statement indicates the new book that has now been added
    
    # Get user input
    title = input('Please enter the title of the book: ')
    author = input('Please enter the author of the book: ')
    qty = int(input('Please enter quanity of books being added: '))   # converting input into an int
    price = int(input('Please enter cost of one book: '))   # converting input into an int
    
    # Create new Book and add to database
    newBook = Book((len(database) + 1), title, author, qty, price)
    database.append(newBook)
    print("Success! {} of qty {} has now been added to stock".format(newBook.getName(), newBook.getQTY()))
    
    
# addQuantity()
def addQuantity(database, bookID, qtytoAdd):
    # Input:
    #       database - Database array of objects
    #       bookID - book code used for identification
    #       qtytoAdd - int value of how many books will be added 
    # Output:
    #       None - a print statement indicates the the new total quantity of the book in stock
    
    for item in database:
        if item.getCode() == bookID:
            item._bookQTY = item.getQTY() + qtytoAdd
            print("The book {} now has {} copies in inventory.".format(item.getName(), item.getQTY()))

    
# buyBook
def buyBook(database, bookID, qtytoBuy):
    # Input:
    #       database - Database array of objects
    #       bookID - book code used for identification
    #       qtytoBuy - int value of how many books user wishes to buy 
    # Output:
    #       None - a print statement that indicates that must be paid
    
    for item in database:
        if item.getCode() == bookID:
            if item.getQTY() < qtytoBuy:
                print("Not enough books in inventory can only buy {} books.".format(item.getQTY()))
                print("Your total comes out to be: ${}".format(item.getQTY() * item.getPrice()))
                item._bookQTY = 0
            else:
                item._bookQTY = item.getQTY() - qtytoBuy
                print("Your total comes out to be: ${}".format(qtytoBuy* item.getPrice()))

    
# printInventoryList()
def printInventoryList(database):
    # Input:
    #       database - Database array of objects
    # Output:
    #       None - a print statement for each book in stock 
    
    for item in database:
        print("Book Code: {}~~The Book: {} by Author {}, now has {} copies in inventory at cost ${}".format(item.getCode(), item.getName(), item.getAuthor(), item.getQTY(), item.getPrice()))
        

def exportToExcel(database):
    # Input:
    #       database - Database array of objects
    # Output:
    #       None - Excel document titled "Bookshop Inventory" is created with each item in inventory    
    
    # Separating out data from each book into different arrays
    
    # Creating and initializing empty arrays
    codeArray = []
    nameArray = []
    authorArray = []
    qtyArray = []
    costArray = []
    
    # looping through database array to split data and add to each array
    for item in database:
        codeArray.append(item.getCode())
        nameArray.append(item.getName())
        authorArray.append(item.getAuthor())
        qtyArray.append(item.getQTY())
        costArray.append(item.getPrice())
    
    
    # Writing to Excel file
    # Creating a Data Frame structure from the dictionary created. Dictionary contains the arrays that hold the data for each of the books that are in our inventory
    df = pd.DataFrame({'Code':codeArray,
                       'Title':nameArray,
                       'Author':authorArray,
                       'Quantity':qtyArray,
                       'Price':costArray})
    writer = pd.ExcelWriter('Bookshop Inventory.xlsx')  # Creating the new Excel file
    df.to_excel(writer,'Sheet 1', index = False)        # Save to Sheet 1 of the newly created Excel file
    writer.save()

    
 

