import json
import tkinter as tk
import Book_adder

# Палитра фонов
main_background = '#fff0c8'
labels_background = '#c89650'
text_background = '#fff0dc'

books, genres, choiced_genres = [], [], []
genre_listbox = None
pages_entry = None
res_text = None
main_label = None
filter_mode = 'ge'
filter_label = None
authors_selection_label = None

lab_text = 'Выберите фильтры для отображения определенных книг (жанры и длина в страницах)'


def update():
    global books, genres, choiced_genres, genre_listbox, main_label, authors_selection_label
    try:
        with open('Book list.json', encoding='utf-8') as file: books = json.load(file)

        genres = sorted(set(book.get('genre', '') for book in books if book.get('genre')))

        genre_listbox.delete(0, tk.END)
        for genre in genres:
            genre_listbox.insert(tk.END, genre)

        genre_listbox.selection_clear(0, tk.END)
        choiced_genres = []

        if authors_selection_label:
            authors_selection_label['text'] = ''
        main_label['text'] = lab_text

    except FileNotFoundError:
        main_label['text'] = 'Файла с книгами нет (Добавьте первую прочитанную книгу)'
        genre_listbox.delete(0, tk.END)
        choiced_genres = []
        if authors_selection_label: authors_selection_label['text'] = ''

    except json.decoder.JSONDecodeError:
        main_label['text'] = 'Файл с книгами поврежден'
        genre_listbox.delete(0, tk.END)
        choiced_genres = []
        if authors_selection_label: authors_selection_label['text'] = ''


def select_genre():
    global choiced_genres
    choiced_genres = [genre_listbox.get(i) for i in genre_listbox.curselection()]

    if choiced_genres: authors_selection_label['text'] = 'Выбраны жанры: ' + str(len(choiced_genres))

    else: authors_selection_label['text'] = 'Жанры не выбраны'


def set_filter_ge():
    global filter_mode
    filter_mode = 'ge'
    filter_label['text'] = 'Страниц ≥'


def set_filter_le():
    global filter_mode
    filter_mode = 'le'
    filter_label['text'] = 'Страниц ≤'


def show():
    global books, choiced_genres, pages_entry, res_text, filter_mode
    selected_genres = choiced_genres if choiced_genres else genres
    pages_str = pages_entry.get().strip()
    try:
        pages = int(pages_str) if pages_str else None
    except ValueError:
        res_text.delete(1.0, tk.END)
        res_text.insert(tk.END, 'Ошибка: введите корректное число страниц')
        return

    filtered = []
    for book in books:
        if book.get('genre') not in selected_genres:
            continue
        if pages is not None:
            book_pages = book.get('pages')
            if book_pages is None:
                continue
            try:
                book_pages = int(book_pages)
            except ValueError:
                continue
            if filter_mode == 'ge' and book_pages < pages:
                continue
            elif filter_mode == 'le' and book_pages > pages:
                continue
        filtered.append(book)

    if not filtered: result_text = 'Нет книг, соответствующих фильтрам.'
    else:
        lines = []
        for book in filtered:
            name = book.get('name', 'Без названия')
            author = book.get('author', 'Неизвестный автор')
            pages_count = book.get('pages', '?')
            genre = book.get('genre', 'Неизвестный жанр')
            lines.append(f'{name} - {author} ({pages_count} стр.) из жанра "{genre}"')
        result_text = '\n'.join(lines)

    res_text.delete(1.0, tk.END)
    res_text.insert(tk.END, result_text)


def adding_window():
    Book_adder.adding_window()


# Создаем главное окно
showing_window = tk.Tk()
showing_window.title('Список прочитанного')
showing_window.geometry('600x500')
showing_window.minsize(600, 500)
showing_window.configure(bg=main_background)

main_label = tk.Label(showing_window, bg=labels_background, fg='white', font='Arial 11', text=lab_text)
main_label.pack(pady=10, fill=tk.X)

# Лейблы для выбранных жанров и режима фильтрации
authors_selection_label = tk.Label(showing_window, fg='black', text='', bg=main_background)
filter_label = tk.Label(showing_window, fg='black', text='Страниц ≥', bg=main_background)
authors_selection_label.place(relx=0.25, y=50, anchor='center')
filter_label.place(relx=0.75, y=50, anchor='center')

# Список жанров
genre_listbox = tk.Listbox(showing_window, width=40, height=10, selectmode='multiple', bg=text_background)
genre_listbox.place(relx=0.25, y=150, anchor='center')

# Кнопка выбора жанров
tk.Button(showing_window, command=select_genre, text='Выбрать жанры', relief='flat', bg=labels_background, fg='white').place(relx=0.25, y=250, anchor='center')

# Поле ввода страниц и кнопки +/-
pages_entry = tk.Entry(showing_window, font='Arial 11', bg=text_background, fg='black')
pages_entry.place(relx=0.75, y=120, anchor='center')

tk.Button(showing_window, command=set_filter_ge, text='+', relief='flat', bg=labels_background, fg='white').place(x=435, y=80, anchor='center')
tk.Button(showing_window, command=set_filter_le, text='-', relief='flat', bg=labels_background, fg='white').place(x=455, y=80, anchor='center')

tk.Button(showing_window, command=update, text='Обновить', relief='flat', bg=labels_background, fg='white').place(relx=0.75, y=160, anchor='center')


tk.Button(showing_window, command=show, text='Вывести список прочитанного',
          relief='flat', bg=labels_background, width=2360, font='Arial 13', fg='white'
          ).place(relx=0.5, y=300, anchor='center')


res_text = tk.Text(showing_window, bg=text_background, height=6, font='Arial 11', width=70, wrap='word')
res_text.place(relx=0.5, y=330, anchor='n')

tk.Button(showing_window, text='Добавить книгу', relief='flat', bg=labels_background, fg='white', command=adding_window).place(relx=0.5, y=465, anchor='center')

update()

showing_window.mainloop()