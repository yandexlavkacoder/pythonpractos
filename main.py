import os

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
    
    def __str__(self):
        status = "доступна" if self.available else "выдана"
        return f"'{self.title}' - {self.author} ({status})"

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []
    
    def __str__(self):
        return f"{self.name} (книг: {len(self.borrowed_books)})"

class Library:
    def __init__(self):
        print("Добро пожаловать в библиотечную систему!")
        self.books = []
        self.users = []
        self.load_data()
    
        self.create_sample_data()
    
    def create_sample_data(self):
        """Создание тестовых данных при первом запуске"""
        if not self.books:
            print("Книга 'Война и мир' добавлена.")
            print("Книга 'Преступление и наказание' добавлена.")
            self.books.append(Book("Война и мир", "Л. Толстой"))
            self.books.append(Book("Преступление и наказание", "Ф. Достоевский"))
        
        if not self.users:
            print("Пользователь 'Иван Иванов' зарегистрирован.")
            self.users.append(User("Иван Иванов"))
    
    def load_data(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split("|")
                        if len(parts) >= 3:
                            book = Book(parts[0], parts[1])
                            book.available = parts[2] == "доступна"
                            self.books.append(book)
        
        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split("|")
                        if parts:
                            user = User(parts[0])
                            if len(parts) > 1 and parts[1]:
                                user.borrowed_books = parts[1].split(",")
                            self.users.append(user)
    
    def save_data(self):
        with open("books.txt", "w", encoding="utf-8") as f:
            for book in self.books:
                status = "доступна" if book.available else "выдана"
                f.write(f"{book.title}|{book.author}|{status}\n")
        
        with open("users.txt", "w", encoding="utf-8") as f:
            for user in self.users:
                books = ",".join(user.borrowed_books)
                f.write(f"{user.name}|{books}\n")
    
    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None
    
    def find_user(self, name):
        for user in self.users:
            if user.name.lower() == name.lower():
                return user
        return None
    
    def librarian_menu(self):
        while True:
            print("\n--- Библиотекарь ---")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Добавить пользователя")
            print("4. Список пользователей")
            print("5. Список книг")
            print("6. Выйти")
            
            choice = input("Выбор: ")
            
            if choice == "1":
                title = input("Название: ")
                author = input("Автор: ")
                self.books.append(Book(title, author))
                print(f"Книга '{title}' добавлена!")
            
            elif choice == "2":
                title = input("Название книги для удаления: ")
                book = self.find_book(title)
                if book:
                    if not book.available:
                        print("Книга выдана, нельзя удалить!")
                    else:
                        self.books.remove(book)
                        print(f"Книга '{title}' удалена!")
                else:
                    print("Книга не найдена!")
            
            elif choice == "3":
                name = input("Имя пользователя: ")
                if not self.find_user(name):
                    self.users.append(User(name))
                    print(f"Пользователь '{name}' добавлен!")
                else:
                    print("Пользователь уже существует!")
            
            elif choice == "4":
                if not self.users:
                    print("Нет пользователей!")
                for user in self.users:
                    print(f"- {user}")
            
            elif choice == "5":
                if not self.books:
                    print("Нет книг!")
                for book in self.books:
                    print(f"- {book}")
            
            elif choice == "6":
                break
    
    def user_menu(self, user):
        while True:
            print(f"\n--- Пользователь: {user.name} ---")
            print("1. Доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("5. Выйти")
            
            choice = input("Выбор: ")
            
            if choice == "1":
                available = [b for b in self.books if b.available]
                if not available:
                    print("Нет доступных книг!")
                for book in available:
                    print(f"- {book.title} ({book.author})")
            
            elif choice == "2":
                title = input("Название книги: ")
                book = self.find_book(title)
                if book:
                    if book.available:
                        book.available = False
                        user.borrowed_books.append(title)
                        print(f"Вы взяли '{book.title}'!")
                    else:
                        print("Книга уже выдана!")
                else:
                    print("Книга не найдена!")
            
            elif choice == "3":
                if not user.borrowed_books:
                    print("У вас нет книг!")
                else:
                    print("Ваши книги:")
                    for title in user.borrowed_books:
                        print(f"- {title}")
                    
                    title = input("Название для возврата: ")
                    if title in user.borrowed_books:
                        user.borrowed_books.remove(title)
                        book = self.find_book(title)
                        if book:
                            book.available = True
                        print("Книга возвращена!")
                    else:
                        print("У вас нет такой книги!")
            
            elif choice == "4":
                if not user.borrowed_books:
                    print("У вас нет книг!")
                for title in user.borrowed_books:
                    print(f"- {title}")
            
            elif choice == "5":
                break

library = Library()

print("=== Библиотечная система ===")

while True:
    print("\nВыберите роль:")
    print("1. Библиотекарь")
    print("2. Пользователь")
    print("3. Выход")
    
    role = input("Роль: ")
    
    if role == "1":
        print("Добро пожаловать, библиотекарь!")
        library.librarian_menu()
    
    elif role == "2":
        name = input("Ваше имя: ")
        user = library.find_user(name)
        if user:
            library.user_menu(user)
        else:
            print("Пользователь не найден! Обратитесь к библиотекарю.")
    
    elif role == "3":
        library.save_data()
        print("Данные сохранены. До свидания!")
        break