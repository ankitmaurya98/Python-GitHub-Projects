# Created 6/14/2021

# This program is a book inventory system. With this program the user can:
# 		Search through a database to see if a book is in inventory
# 		Checkout a book and a QTY of the book from inventory.
# 		Add a book and QTY of that book to the inventory.
# 		Export entire inventory as a text file.
#
#



# Project idea and some example code from:https: //omkarnathsingh.wordpress.com/2016/02/09/c-program-for-book-shop/

# Explanation of Functions that are part of the Book class
# 		Constructors:
# 			Book(int code, string name, string author, int qty, int price)-Constructor with all inputs
#			Book(int code, string name, string author)-Constructor with limited inputs
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






import Book


def menuFunction(inventory):
    runloop = 0
    
    while(runloop != 1):
        print('''------Menu------
            1. Entry of New Book
            2. Buy Book
            3. Search for Book
            4. Edit Quantity of Book in Inventory
            5. Print Inventory List
            6. Export Inventory List to Excel
            7. Exit
            ''')
        choice = int(input("Enter your choice: "))
        
        # If statements that will run based on the choice that is made
        if choice == 1:
            Book.addBook(inventory)
        elif choice == 2:
            inputCode = int(input("Enter Book Code: "))
            inputQTYToBuy = int(input("Enter Quantity to Buy: "))
            Book.buyBook(inventory, inputCode, inputQTYToBuy)
        elif choice == 3:
            inputCode = int(input("Enter Book Code: "))
            Book.inStock(inventory, inputCode)
        elif choice == 4:
            inputCode = int(input("Enter Book Code: "))
            inputQTYToAdd = int(input("Enter Quantity to Add: "))
            Book.addQuantity(inventory, inputCode, inputQTYToAdd)
        elif choice == 5:
            Book.printInventoryList(inventory)
        elif choice == 6:
            Book.exportToExcel(inventory)
        elif choice == 7:
            runloop = 1
        else:
            print("Invalid Entry")
            





def main():

    # Creating some Book objects that will be placed in an inventory array
    book1 = Book.Book(1, "Harry Potter", "JK Rowling", 7, 20)
    book2 = Book.Book(2, "Game Of Thrones", "George RR Martin", 5, 15)
    book3 = Book.Book(3, "Percy Jackson", "Rick Riordan", 5, 10)
    
    # Creating the inventory array and appending the book objects
    inventory = []
    inventory.append(book1)
    inventory.append(book2)
    inventory.append(book3)
    
    
    # Testing functions~~~~~~~~~~~~~~~~~~~~~~~~
    # inStock() function
    # Book.inStock(inventory, 2)
    
    # addQuantity() function
    # Book.addQuantity(inventory, 2, 10)
    
    # addBook() function
    # Book.addBook(inventory)
    # Book.addBook(inventory)
    # Book.addQuantity(inventory, 4, 21)
    
    # buyBook() function
    # Book.buyBook(inventory, 4, 20)
    
    # printInventoryList() function
    # Book.printInventoryList(inventory)
    
    # exportToExcel() function
    # Book.exportToExcel(inventory)
    
    # Menu Function loop
    menuFunction(inventory)


if __name__ == '__main__': main()



