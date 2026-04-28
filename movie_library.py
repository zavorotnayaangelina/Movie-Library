import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("900x600")
        
        # Файл для хранения данных
        self.data_file = "movies.json"
        
        # Список фильмов
        self.movies = []
        
        # Загрузка данных из JSON
        self.load_data()
        
        # Создание интерфейса
        self.create_input_form()
        self.create_filter_section()
        self.create_movie_table()
        
    def create_input_form(self):
        """Создание формы для ввода данных"""
        input_frame = tk.LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Название
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Жанр
        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", pady=5, padx=(20,0))
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # Год
        tk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="w", pady=5)
        self.year_entry = tk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Рейтинг
        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w", pady=5, padx=(20,0))
        self.rating_entry = tk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, pady=5, padx=5)
        
        # Кнопки
        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        add_btn = tk.Button(button_frame, text="Добавить фильм", command=self.add_movie, 
                           bg="#4CAF50", fg="white", padx=20, pady=5)
        add_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(button_frame, text="Очистить форму", command=self.clear_form,
                            bg="#f44336", fg="white", padx=20, pady=5)
        clear_btn.pack(side="left", padx=5)
        
    def create_filter_section(self):
        """Создание секции фильтрации"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(pady=5, padx=10, fill="x")
        
        # Фильтр по жанру
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=20)
        self.filter_genre_entry.pack(side="left", padx=5)
        
        # Фильтр по году
        tk.Label(filter_frame, text="Фильтр по году:").pack(side="left", padx=(20,5))
        self.filter_year_entry = tk.Entry(filter_frame, width=10)
        self.filter_year_entry.pack(side="left", padx=5)
        
        # Кнопки фильтрации
        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter,
                              bg="#2196F3", fg="white")
        filter_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter,
                              bg="#FF9800", fg="white")
        reset_btn.pack(side="left", padx=5)
        
    def create_movie_table(self):
        """Создание таблицы для отображения фильмов"""
        table_frame = tk.LabelFrame(self.root, text="Список фильмов", padx=10, pady=10)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Создание Treeview
        columns = ("ID", "Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        
        self.tree.column("ID", width=50)
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления
        control_frame = tk.Frame(table_frame)
        control_frame.pack(fill="x", pady=(10,0))
        
        delete_btn = tk.Button(control_frame, text="Удалить выбранный фильм", command=self.delete_movie,
                              bg="#f44336", fg="white")
        delete_btn.pack(side="left", padx=5)
        
        edit_btn = tk.Button(control_frame, text="Редактировать выбранный", command=self.edit_movie,
                            bg="#FF9800", fg="white")
        edit_btn.pack(side="left", padx=5)
        
        # Обновление таблицы
        self.refresh_table()
        
    def add_movie(self):
        """Добавление нового фильма"""
        # Получение данных из формы
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        # Валидация
        if not title:
            messagebox.showerror("Ошибка", "Введите название фильма")
            return
        
        if not genre:
            messagebox.showerror("Ошибка", "Введите жанр фильма")
            return
        
        if not year:
            messagebox.showerror("Ошибка", "Введите год выпуска")
            return
        
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:
                messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2026")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        
        if not rating:
            messagebox.showerror("Ошибка", "Введите рейтинг")
            return
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return
        
        # Создание ID
        movie_id = len(self.movies) + 1
        
        # Добавление фильма
        movie = {
            "id": movie_id,
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        }
        
        self.movies.append(movie)
        self.save_data()
        self.clear_form()
        self.refresh_table()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
        
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления")
            return
        
        # Получение ID выбранного фильма
        item = self.tree.item(selected[0])
        movie_id = int(item['values'][0])
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Удалить выбранный фильм?"):
            self.movies = [m for m in self.movies if m['id'] != movie_id]
            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Успех", "Фильм удален")
    
    def edit_movie(self):
        """Редактирование выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для редактирования")
            return
        
        # Получение ID выбранного фильма
        item = self.tree.item(selected[0])
        movie_id = int(item['values'][0])
        
        # Поиск фильма
        movie = next((m for m in self.movies if m['id'] == movie_id), None)
        
        if movie:
            # Заполнение формы данными фильма
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, movie['title'])
            
            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(0, movie['genre'])
            
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, str(movie['year']))
            
            self.rating_entry.delete(0, tk.END)
            self.rating_entry.insert(0, str(movie['rating']))
            
            # Удаление старой записи
            self.movies = [m for m in self.movies if m['id'] != movie_id]
            
            messagebox.showinfo("Информация", "Теперь вы можете отредактировать данные и добавить фильм заново")
    
    def apply_filter(self):
        """Применение фильтрации"""
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()
        
        filtered_movies = self.movies.copy()
        
        if genre_filter:
            filtered_movies = [m for m in filtered_movies if genre_filter in m['genre'].lower()]
        
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered_movies = [m for m in filtered_movies if m['year'] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом")
                return
        
        self.refresh_table(filtered_movies)
        
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()
    
    def refresh_table(self, movies_list=None):
        """Обновление таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение списка для отображения
        display_movies = movies_list if movies_list is not None else self.movies
        
        # Добавление данных в таблицу
        for movie in display_movies:
            self.tree.insert("", "end", values=(
                movie['id'],
                movie['title'],
                movie['genre'],
                movie['year'],
                f"{movie['rating']:.1f}"
            ))
    
    def clear_form(self):
        """Очистка формы ввода"""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    self.movies = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.movies = []
        else:
            # Пример данных для демонстрации
            self.movies = [
                {"id": 1, "title": "Побег из Шоушенка", "genre": "Драма", "year": 1994, "rating": 9.3},
                {"id": 2, "title": "Криминальное чтиво", "genre": "Криминал", "year": 1994, "rating": 8.9},
                {"id": 3, "title": "Темный рыцарь", "genre": "Экшн", "year": 2008, "rating": 9.0}
            ]
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
