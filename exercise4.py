import sqlite3
import sys

# Create database and tables
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Books (
                BookID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT,
                Author TEXT,
                ISBN TEXT,
                Status TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Email TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                BookID INTEGER,
                UserID INTEGER,
                ReservationDate TEXT,
                FOREIGN KEY (BookID) REFERENCES Books (BookID),
                FOREIGN KEY (UserID) REFERENCES Users (UserID)
            )''')

conn.commit()

# Function to add a new book to the database
def add_book(title, author, isbn):
    c.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
              (title, author, isbn, "Available"))
    conn.commit()
    print("Book added successfully!")

# Function to find a book's details based on BookID
def find_book_details(book_id):
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID
                 WHERE Books.BookID = ?''', (book_id,))
    result = c.fetchone()
    if result:
        book_id, title, author, isbn, status, user_name, user_email = result
        print("Book ID:", book_id)
        print("Title:", title)
        print("Author:", author)
        print("ISBN:", isbn)
        print("Status:", status)
        if user_name and user_email:
            print("Reserved by:", user_name)
            print("User email:", user_email)
    else:
        print("Book not found!")

# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status(search_text):
    if search_text.startswith("LB"):
        # Search by BookID
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.BookID = ?''', (search_text,))
    elif search_text.startswith("LU"):
        # Search by UserID
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Users.UserID = ?''', (search_text,))
    elif search_text.startswith("LR"):
        # Search by ReservationID
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Reservations.ReservationID = ?''', (search_text,))
    else:
        # Search by Title
        c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                     FROM Books
                     LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                     LEFT JOIN Users ON Reservations.UserID = Users.UserID
                     WHERE Books.Title = ?''', (search_text,))

    result = c.fetchall()
    if result:
        for row in result:
            book_id, title, status, user_name, user_email = row
            print("Book ID:", book_id)
            print("Title:", title)
            print("Status:", status)
            if user_name and user_email:
                print("Reserved by:", user_name)
                print("User email:", user_email)
            print()
    else:
        print("No matching records found!")

# Function to find all the books in the database
def find_all_books():
    c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
                 FROM Books
                 LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                 LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    result = c.fetchall()
    if result:
        for row in result:
            book_id, title, author, isbn, status, user_name, user_email = row
            print("Book ID:", book_id)
            print("Title:", title)
            print("Author:", author)
            print("ISBN:", isbn)
            print("Status:", status)
            if user_name and user_email:
                print("Reserved by:", user_name)
                print("User email:", user_email)
            print()
    else:
        print("No books found!")

# Function to modify/update book details based on its BookID
def update_book_details(book_id, new_title=None, new_author=None, new_isbn=None, new_status=None):
    if new_status:
        c.execute("UPDATE Books SET Title = ?, Author = ?, ISBN = ?, Status = ? WHERE BookID = ?",
                  (new_title, new_author, new_isbn, new_status, book_id))
        c.execute("UPDATE Reservations SET BookID = ? WHERE BookID = ?", (book_id, book_id))
        conn.commit()
        print("Book details updated successfully!")
    else:
        c.execute("UPDATE Books SET Title = ?, Author = ?, ISBN = ? WHERE BookID = ?",
                  (new_title, new_author, new_isbn, book_id))
        conn.commit()
        print("Book details updated successfully!")

# Function to delete a book based on its BookID
def delete_book(book_id):
    c.execute("SELECT * FROM Reservations WHERE BookID = ?", (book_id,))
    result = c.fetchone()
    if result:
        c.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book and reservation deleted successfully!")
    else:
        c.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully!")

# Main program loop
while True:
    print("Library Management System")
    print("1. Add a new book")
    print("2.Find a book's reservation status")
    print("3. Find all books") 
    print("4. Update book details") 
    print("5. Delete a book") 
    print("6. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        title = input("Enter the book title: ")
        author = input("Enter the book author: ")
        isbn = input("Enter the book ISBN: ")
        add_book(title, author, isbn)
        
    elif choice == "2":
        search_text = input("Enter the book ID, title, user ID, or reservation ID: ")
        find_reservation_status(search_text)
    
    elif choice == "3":
        find_all_books()
    
    elif choice == "4":
        book_id = input("Enter the book ID: ")
        new_title = input("Enter the new title (leave blank to keep current): ")
        new_author = input("Enter the new author (leave blank to keep current): ")
        new_isbn = input("Enter the new ISBN (leave blank to keep current): ")
        new_status = input("Enter the new status (leave blank to keep current): ")
        update_book_details(book_id, new_title, new_author, new_isbn, new_status)
    
    elif choice == "5":
        book_id = input("Enter the book ID: ")
        delete_book(book_id)
    
    elif choice == "6":
        sys.exit()
    else:
        print("Invalid choice. Please try again.\n")