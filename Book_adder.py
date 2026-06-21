import tkinter as tk
import json

main_background = '#fff0c8'
labels_background = '#c89650'
text_background = '#fff0dc'

book_name, book_author, book_pages, add_pages, add_name, add_author, add_genre,res_label = '', '', '', '', '', '', '', ''


def add_book():
    global book_pages, add_pages, add_name, add_author, res_label, add_genre
    try:
        book_name = add_name.get()
        book_author = add_author.get()
        book_pages = int(add_pages.get())
        book_genre = add_genre.get()
        add_genre.delete(0, tk.END)
        add_name.delete(0, tk.END)
        add_author.delete(0, tk.END)
        add_pages.delete(0, tk.END)
        if book_pages and book_name and book_author:

            book = {'author': book_author, 'genre': book_genre, 'name': book_name, 'pages': book_pages}
            try:
                with open('Book list.json', 'r', encoding='utf-8') as file:
                    books = json.load(file)

            except FileNotFoundError: res_label['text'] = 'Файла с книгами нет. Создаем новый'; books = []
            except json.decoder.JSONDecodeError: res_label['text'] = 'Файл поврежден, создаем новый.'; books = []

            books.append(book)

            with open('Book list.json', 'w', encoding='utf-8') as file:
                json.dump(books, file, indent=4, sort_keys=True, ensure_ascii=False)

            res_label['text'] = 'Книга добавлена'

        else: res_label['text'] = 'Заполните все поля'
    except ValueError: res_label['text'] = 'В графе со страницами должно быть целое число'

def adding_window():
    global add_name, add_author, add_pages, res_label, add_genre
    adding_window = tk.Tk()
    adding_window.title('Добавить книгу')
    adding_window.geometry('600x250')
    adding_window.minsize(600, 250)
    adding_window.resizable(False, False)
    adding_window.configure(bg=main_background)

    tk.Label(adding_window, bg=labels_background, fg='white', font='Arial 13', text='Заполните все поля для добавления книги').pack(pady=10, fill=tk.X)

    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Название:').place(y=50, anchor='w', x=10)
    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Автор:').place(y=80, anchor='w', x=10)
    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Жанр:').place(y=140, anchor='w', x=10)
    tk.Label(adding_window, bg=main_background, fg='black', font='Arial 11', text='Кол-во стр.:').place(y=110, anchor='w', x=10)

    add_name = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)
    add_author = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)
    add_pages = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)
    add_genre = tk.Entry(adding_window, bg=text_background, fg='black', font='Arial 11', width=50)

    res_label = tk.Label(adding_window, bg=labels_background, fg='white', font='Arial 13', text='', width=90)
    tk.Button(adding_window, command=add_book, text='Добавить', relief='flat', bg=labels_background, width=2360, font='Arial 13', fg='white').place(relx=0.5, y=220, anchor='center')

    add_name.place(x=100, y=50, anchor='w')
    add_author.place(x=100, y=80, anchor='w')
    add_pages.place(x=100, y=110, anchor='w')
    add_genre.place(x=100, y=140, anchor='w')
    res_label.place(relx=0.5, y=170, anchor='n')

    adding_window.mainloop()