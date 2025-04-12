from datetime import datetime, timedelta, date


class Book:
    def __init__(self, title, author, isbn, category):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = 'Available'
        self.category = category.upper()

    def __str__(self):
        return f"📘 {self.title} by {self.author}"  # Nice for user display

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}, {self.isbn}, {self.category}')"  # Better for debugging

    def borrow_book(self):
        if self.status == 'Borrowed':
            return False
        self.status = 'Borrowed'
        return True

    def return_book(self):
        if self.status == 'Available':
            return False
        self.status = 'Available'
        return True


class Member:
    def __init__(self, name, unique_id):
        self.name = name
        self.id = unique_id
        self.books_borrowed = {}  # Stores borrowed books mapped to their due dates

    def __repr__(self):
        return f"Member: {self.name} ID: {self.id}"


class Library:
    def __init__(self):
        self.books = {}  # Dictionary to store books by ISBN
        self.members = {}  # key: member.id, value: Member object

    def add_book(self, book):
        """Adds a book if not found in the Library"""
        if book.isbn in self.books:
            print(f"A book with ISBN: {book.isbn} is already in the Library.")
            return
        if not book.title or not book.author or not book.isbn:
            print("Invalid book details. Title, author, and ISBN cannot be empty.")
            return
        if book.category not in ['FICTION', 'NON-FICTION']:
            print('Invalid book category. It has to be eiter "FICTION" or "NON-FICTION".')
            return
        self.books[book.isbn] = book
        print(f'Book "{book.title}" added successfully to the Library.')

    def register_member(self, member):
        """Registers a new member if the ID is unique."""
        if member.id in self.members:
            print(f'A member with the ID: {member.id} is already registered in the Library.')
            return
        if not member.name or not member.id:
            print("Invalid member details. Name and ID cannot be empty.")
            return
        self.members[member.id] = member
        print(f'Member "{member.name}" registered successfully.')

    def borrowing_book(self, book, member):
        """Allows a member to borrow a book if available and sets a due date"""
        if book.isbn not in self.books:
            print('The book is not currently present in the Library')
            return

        if member.id not in self.members:
            print(f'{member.name} is not a member in the Library')
            return

        if not book.borrow_book():
            print('The book is already borrowed')
            return

        member.books_borrowed[book.isbn] = self._get_due_date()
        book.borrow_book()
        print(f'"{book.title}" has been borrowed by {member.name}.')
        print(f'Due Date: {member.books_borrowed[book.isbn]}')

    def returning_book(self, book, member):
        """Allows a member to return a borrowed book"""
        if book.isbn not in self.books:
            print(f'Book Not Found! This book ({book.title}) does not belong in this Library.')
            return

        if member.id not in self.members:
            print(f'Member not found! {member.name} is not a member in the Library')
            return

        if book.isbn not in member.books_borrowed:
            print(f"The book was not found in the {member.name}'s borrowed list!!!")
            return

        due_date_str = member.books_borrowed[book.isbn]
        return_date_str = datetime.today().strftime('%Y-%m-%d')

        if return_date_str <= due_date_str:
            del member.books_borrowed[book.isbn]
            book.return_book()
            print(f'"{book.title}" has been returned by {member.name}.')
        else:
            delayed_num_of_days = (datetime.strptime(return_date_str, "%Y-%m-%d") - datetime.strptime(due_date_str, "%Y-%m-%d")).days
            late_fee = delayed_num_of_days * 1
            print(f'You were late by {delayed_num_of_days} day(s).')
            print(f'Late Fee: ${late_fee} (Library charges $1 per day for each overdue book.)')
            del member.books_borrowed[book.isbn]
            book.status = 'Available'
            print(f'"{book.title}" has been returned by {member.name}.')

    def display_available_books(self):
        """Displays books that are available for borrowing."""
        available_books = [book for book in self.books.values() if book.status == 'Available']
        if not available_books:
            print("No books are currently available in the Library")
            return
        print('\n-----Available Books------')
        for index, book in enumerate(available_books, start=1):
            print(f'{index}. {book.title}')

    def borrowed_books_by_member(self, member):
        """Displays books borrowed by a specific member."""
        if member.id not in self.members:
            print("Member not found in the Library.")
            return
        if not member.books_borrowed:
            print(f'{member.name} does not currently borrow any books from the Library')
            return

        print(f"\nBooks borrowed by {member.name}:")
        for index, isbn in enumerate(member.books_borrowed, start=1):
            book = self.books[isbn]
            print(f"{index}. {book.title} - Due Date: {member.books_borrowed[isbn]}")

    def search(self):
        """Searches by a specific option selected"""
        print('🔍 Search By: ')
        print('1.Title')
        print('2.Author')
        print('3.ISBN')
        print('4.Category (Fiction/Non-Fiction)')
        print('5.Exit')
        while True:
            choice = input('Choose an option (1-5): ').strip()
            if choice == '1':
                title = input('Please enter the name of the book you are looking for: ').strip().lower()
                search_book = [book for book in self.books.values() if title in book.title.lower()]
                if search_book:
                    print(f'----Similar matches found with the Title: {title}')
                    for index, books in enumerate(search_book, start=1):
                        print(f'\n{index}. {books.title}')
                        print(f'Author: {books.author}')
                        print(f'ISBN: {books.isbn}')
                        print(f'Category: {books.category}')
                        print(f'Status: {books.status}')
                    return
                else:
                    print(f'No similar matches found with the title name {title}')
                    return
            elif choice == '2':
                author = input('Please enter the name of the author: ').strip().lower()
                search_author = [book for book in self.books.values() if author in book.author.lower()]
                if search_author:
                    print(f'Books written by {author}')
                    for index, books in enumerate(search_author, start=1):
                        print(f'\n{index}. {books.title}')
                        print(f'ISBN: {books.isbn}')
                        print(f'Category: {books.category}')
                        print(f'Status: {books.status}')
                    return
                else:
                    print(f'No books were found in the library written by {author.upper()}')
                    return
            elif choice == '3':
                isbn = input('Please enter the ISBN of the book you are looking for: ').strip()
                if isbn in self.books:
                    print('------MATCH FOUND-------')
                    print(self.books[isbn])
                    return
                print(F'No book was found in the library with the ISBN: {isbn}')
            elif choice == '4':
                print('1.Fiction books')
                print('2.Non-Fiction books')
                while True:
                    category = input('Please choose an option (1 or 2): ').strip()
                    if category == '1':
                        books_by_category = [b for b in self.books.values() if b.category == 'FICTION']
                        break
                    elif category == '2':
                        books_by_category = [b for b in self.books.values() if b.category == 'NON-FICTION']
                        break
                    else:
                        print('Please enter a valid option. Either "1" or "2"')
                if books_by_category:
                    if category == '1':
                        print('-------FICTIONAL BOOKS--------')
                    elif category == '2':
                        print('-------NON-FICTIONAL BOOKS--------')
                    for index, book in enumerate(books_by_category, start=1):
                        print(f'\n {index}. {book.title}')
                        print(f'Author: {book.author}')
                        print(f'ISBN: {book.isbn}')
                        print(f'Status: {book.status}')
                    return
                else:
                    print(f'No books found under the category {category}')
                    return
            elif choice == '5':
                print('Hope to see you soon again! Bye! T-T')
                return
            else:
                print('Please choose a valid option. (e.g., "Enter "1" to search by title, etc.)')

    @staticmethod
    def _get_due_date():
        """Returns the due date (21 days from the current date)"""
        borrow_date_str = datetime.today().strftime('%Y-%m-%d')
        borrow_date = datetime.strptime(borrow_date_str, "%Y-%m-%d")
        due_date = str((borrow_date + timedelta(days=21)).date())
        return due_date


# ----- Create Library Instance -----
my_library = Library()

# ----- Test Books -----
book1 = Book("The Alchemist", "Paulo Coelho", "1234567890", "Fiction")
book2 = Book("Sapiens", "Yuval Noah Hero", "0987654321", "Non-Fiction")
# book3 = Book("", "Unknown", "1111111111", "Fiction")  # Invalid: Empty title
# book4 = Book("Invisible Book", "Ghost Writer", "1234567890", "Fiction")  # Duplicate ISBN
# book5 = Book("Random Book", "Random Author", "5555555555", "Fantasy")  # Invalid category

# ----- Add Books -----
my_library.add_book(book1)  # ✅ Should succeed
my_library.add_book(book2)  # ✅ Should succeed
# my_library.add_book(book3)  # ❌ Invalid title
# my_library.add_book(book4)  # ❌ Duplicate ISBN
# my_library.add_book(book5)  # ❌ Invalid category

# ----- Test Members -----
member1 = Member("Alice", "001")
member2 = Member("Bob", "002")
member3 = Member("", "003")  # ❌ Invalid name
# member4 = Member("Alice", "001")  # ❌ Duplicate ID

# ----- Register Members -----
my_library.register_member(member1)  # ✅ Should succeed
my_library.register_member(member2)  # ✅ Should succeed
# my_library.register_member(member3)  # ❌ Invalid name
# my_library.register_member(member4)  # ❌ Duplicate ID

# ✅ Valid Borrowing
# my_library.borrowing_book(book1, member1)  # Should succeed

# ❌ Already borrowed
# my_library.borrowing_book(book1, member2)  # Should fail (book is not available)

# ❌ Non-member
# non_member = Member("Charlie", "999")
# my_library.borrowing_book(book2, non_member)  # Should fail (not registered)

# ❌ Non-existent Book
# fake_book = Book("Fake Book", "Nobody", "0000000000", "Fiction")
# my_library.borrowing_book(fake_book, member1)  # Should fail (not in library)

# ✅ Valid Return before due
# my_library.returning_book(book1, member1)  # Should succeed (no late fee)

# ❌ Book was never borrowed by member
# my_library.returning_book(book2, member1)  # Should fail

# ❌ Book not in library
# my_library.returning_book(fake_book, member2)  # Should fail

# 🔁 Borrow again, simulate late return
# Manually set a past due date to simulate late return
# my_library.borrowing_book(book1, member1)
# member1.books_borrowed[book1.isbn] = "2024-12-01"  # Simulate overdue

# my_library.returning_book(book1, member1)  # Should show late fee

my_library.display_available_books()  # Should list only non-borrowed books
my_library.borrowed_books_by_member(member1)  # Should list borrowed books with due dates
my_library.borrowed_books_by_member(member3)  # Should fail (not registered)


# my_library.search()


