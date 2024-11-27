from tkinter import *

import pandas as pd

from Names import Names
from tkinter import filedialog
# checked on python 3.12

THEME_COLOR = "#E8E8E4"
DARK_GREY = "#a0a0a0"
PINK = '#ff468c'
FILTER_LABEL_ROW = 1
BUTTON_WIDTH = 35
BUTTON_ROW = 8
ICON_ROW = 4
LABEL_ROW = 5
CANVAS_ROW = 6
INFO_ROW = 7
FILTER_ROW = 2


class UI:

    def __init__(self, names_bank: Names):
        self.names_bank = names_bank
        self.game_over = True
        self.current_position = 0
        self.info = f'{self.current_position + 1} / {len(self.names_bank.data)}'
        self.info_counts = f'Liczba imion w PL: {str(self.names_bank.data.loc[self.names_bank.data.index[self.current_position]]["Counts"])}'
        self.info_counts_2022 = f'Liczba imion w PL 2022: {str(int(self.names_bank.data.loc[self.names_bank.data.index[self.current_position]]["Counts_2022"]))}'

        self.window = Tk()
        self.set_layout()
        self.window.mainloop()

    def void(self):
        pass

    def boy_clicked(self):
        self.canvas.itemconfig(self.name_text, text='BOY NAME', fill='blue')
        self.names_bank.filter_gender = 'male'
        # set filter gender boy

    def mom_clicked(self):
        self.names_bank.filter_parent = 'Kinga'

    def dad_clicked(self):
        self.names_bank.filter_parent = 'Arek'

    def girl_clicked(self):
        #self.canvas.config(background='#ff468c')
        self.canvas.itemconfig(self.name_text, text='GIRL NAME', fill='#ff468c')
        self.names_bank.filter_gender = 'female'

    def hide_buttons(self):
        print('hiding buttons')
        self.check_button.grid_forget()
        self.delete_button.grid_forget()
        self.question_button.grid_forget()

    def show_buttons(self):
        self.check_button.grid(row=BUTTON_ROW, column=1, padx=10, pady=30)
        self.delete_button.grid(row=BUTTON_ROW, column=2, padx=10, pady=30)
        self.question_button.grid(row=BUTTON_ROW, column=3, padx=10, pady=30)

    def like_clicked(self):
        #print(f'INFO: like_clicked: current_position: {self.current_position}')
        if self.names_bank.data.index[self.current_position] is not None:
            self.vote(self.names_bank.data.index[self.current_position], 'like')
        #self.current_position = self.current_position + 1
        #self.get_next_name()
        self.rev()

    def dislike_clicked(self):
        #print(f'INFO: dislike_clicked: current_position: {self.current_position}')
        if self.names_bank.data.index[self.current_position] is not None:
            self.vote(self.names_bank.data.index[self.current_position], 'dislike')
        self.rev()
        #self.current_position = self.current_position + 1
        #self.get_next_name()
    def vote(self, ix, vote_rate):
        print(f'vote: ix: {ix}')
        self.names_bank.data.loc[ix, (self.names_bank.filter_parent)] = vote_rate
        print(f'vote: {self.names_bank.data.loc[ix, ("Name")]} = {vote_rate}')
        self.save_data(name=self.names_bank.data.loc[ix, ("Name")], gender=self.names_bank.data.loc[ix, ("Gender")], vote_rate=vote_rate)
        #self.names_bank.data.to_csv('names_99.csv', sep=',', index=False)

    def get_next_name(self):

        if self.current_position < len(self.names_bank.data.index):
            #self.current_position = self.current_position + 1
            self.update_labels()
            next_index = self.names_bank.data.index[self.current_position]
            print(f'get_next_name: current pos: {self.current_position}')
            print(f'get_next_name: {self.names_bank.data.loc[next_index]["Name"]}')

            if self.names_bank.data.loc[next_index]['Gender'] == 'male':
                self.canvas.itemconfig(self.name_text, text=self.names_bank.data.loc[next_index]['Name'], fill='blue')
            else:
                self.canvas.itemconfig(self.name_text, text=self.names_bank.data.loc[next_index]['Name'], fill='#ff468c')
            #self.current_position = self.current_position + 1
        else:
            print(f'self.current_position: {self.current_position}')

    def update_labels(self):
        self.info = f'{self.current_position + 1} / {len(self.names_bank.data)}'
        self.info_counts = f'Liczba imion: {str(self.names_bank.data.loc[self.names_bank.data.index[self.current_position]]["Counts"])}'
        try:
            self.info_counts_2022 = f'Liczba imion w 2022: {str(int(self.names_bank.data.loc[self.names_bank.data.index[self.current_position]]["Counts_2022"]))}'
        except ValueError:
            self.info_counts_2022 = f'Liczba imion w 2022: brak danych'
        self.info_label.configure(text=self.info)
        self.info_counts_label.configure(text=self.info_counts)
        self.info_counts_2022_label.configure(text=self.info_counts_2022)

    def start(self):
        self.game_over = False

        print(f'current_position: {self.current_position}')

        self.get_next_name()
        self.check_button['state'] = 'active'
        self.delete_button['state'] = 'active'
        self.question_button['state'] = 'active'
        self.set_button['state'] = 'disabled'
        self.scale_counts_min['state'] = 'disabled'
        self.scale_counts_max['state'] = 'disabled'

        print(f'gender: {self.names_bank.filter_gender}')
        print(f'parent: {self.names_bank.filter_parent}')

    def save_data(self, name, gender, vote_rate):

        print(f'name: {name} gender: {gender}')
        org = pd.read_csv('names_98.csv')
        print(org.info())
        name_filter = org['Name'] == name
        gender_filter = org['Gender'] == gender
        index_to_update = org[name_filter & gender_filter].index
        org.loc[index_to_update, 'Arek'] = vote_rate
        org.to_csv('names_98.csv', sep=',', index=False)

    def set_filter(self):
        print('set filter')
        pass

    def apply_filters(self):

        if self.check_filter():
            self.names_bank.data = self.names_bank.data_backup
            self.filter_gender = self.names_bank.data['Gender'] == self.names_bank.filter_gender
            self.filter_parent = self.names_bank.data[self.names_bank.filter_parent] == 'Unknown'
            total_min = self.names_counts_PL_min.get() / 1000 * 800000
            total_max = self.names_counts_PL_max.get() / 1000 * 800000
            c2022_min = self.names_counts_PL2022_min.get() / 100 * 4000
            c2022_max = self.names_counts_PL2022_max.get() / 100 * 4000
            print(f'{total_min} {total_max} {c2022_min} {c2022_max}')
            self.filter_counts = self.names_bank.data['Counts'].between(total_min, total_max)
            self.filter_counts2022 = self.names_bank.data['Counts_2022'].between(c2022_min, c2022_max)
            #print(f'sum filter gender: {self.filter_gender.sum()}')
            self.names_bank.data = self.names_bank.data_backup[(self.filter_gender) & (self.filter_parent) & (self.filter_counts) & (self.filter_counts2022)]

            self.names_bank.reset_indexes_INT()
            self.current_position = 0
            #self.question_button['state'] = 'active'
            self.show_buttons()
            self.start()
            print(f'apply filters: current pos: {self.current_position}')
        else:
            pass

        self.debugger()

    def test_button(self):
        print('test button')
        print(f'{self.names_counts_PL_min.get()}')

    def back_to_filters(self):
        self.game_over = True
        self.check_button['state'] = 'disabled'
        self.delete_button['state'] = 'disabled'
        self.question_button['state'] = 'disabled'
        self.set_button['state'] = 'active'
        self.scale_counts_min['state'] = 'active'
        self.scale_counts_max['state'] = 'active'

    def debugger(self):
        print(f'debugger: self.names_bank.filter_gender: {self.names_bank.filter_gender}')
        print(f'debugger: len(self.names_bank.data): {len(self.names_bank.data)}')
        print(f'debugger: index[current_pos]: {self.names_bank.data.index[self.current_position]}')
        print(f'debugger: name at index[current_pos]: {self.names_bank.data.index[self.current_position]}')

    def check_filter(self):

        if self.names_bank.filter_gender is None:
            print("Ustaw płeć dziecka")
            self.canvas.itemconfig(self.name_text, text="Wybierz płeć dziecka", fill='red')
            return False
        if self.names_bank.filter_parent is None:
            print("Ustaw kto wybiera: mama czy tata?")
            self.canvas.itemconfig(self.name_text, text="Kto wybiera? mama czy tata?", fill='red')
            return False
        if self.names_counts_PL_min.get() > self.names_counts_PL_max.get():
            print(f'names_counts_PL_min > names_counts_PL_max: {self.names_counts_PL_min.get()} > {self.names_counts_PL_max.get()}')
            self.canvas.itemconfig(self.name_text, text="Zmień zakres w pierwszym filtrze", fill='red')
            return False
        if self.names_counts_PL2022_min.get() > self.names_counts_PL2022_max.get():
            print(f'names_counts_PL2022_min > names_counts_PL2022_max: {self.names_counts_PL2022_min.get()} > {self.names_counts_PL2022_max.get()}')
            self.canvas.itemconfig(self.name_text, text="Zmień zakres w drugim filtrze", fill='red')
            return False

        return True

    def set_layout(self):
        self.window.title("[K] i n d e r")
        self.window.config(background=THEME_COLOR, padx=20, pady=20)
        self.window.minsize(width=860, height=800)
        self.window.maxsize(width=860, height=800)
        # Images
        self.img_baby_boy = PhotoImage(file='images/baby-boy.png')
        # img_baby_boy = img_baby_boy.zoom(10)
        # img_baby_boy = img_baby_boy.subsample(51)

        self.img_baby_girl = PhotoImage(file='images/baby-girl.png')
        # img_baby_girl = img_baby_girl.zoom(10)
        # img_baby_girl = img_baby_girl.subsample(51)

        self.img_check = PhotoImage(file='images/check_new.png')
        self.img_delete = PhotoImage(file='images/remove.png')
        self.img_question = PhotoImage(file='images/question.png')
        self.img_woman = PhotoImage(file='images/woman.png')
        self.img_man = PhotoImage(file='images/profile.png')
        self.img_common = PhotoImage(file='images/results.png')
        self.icon_baby = PhotoImage(file='images/icon-baby.png')
        self.before_btn = PhotoImage(file='images/before.png')
        self.next_btn = PhotoImage(file='images/next.png')
        self.save_btn = PhotoImage(file='images/diskette.png')
        self.apply_btn = PhotoImage(file='images/apply.png')
        self.exit_btn = PhotoImage(file='images/log-out.png')

        self.window.iconphoto(False, self.icon_baby)

        self.names_counts_PL_min = IntVar()
        self.names_counts_PL_max = IntVar()
        self.scale_counts_min = Scale(variable=self.names_counts_PL_min, orient=HORIZONTAL, cursor="dot", from_=0,
                                      to=1000, background=THEME_COLOR, highlightthickness=0)
        self.scale_counts_min.set(0)
        self.scale_counts_min.grid(row=FILTER_ROW, column=0)
        self.scale_counts_max = Scale(variable=self.names_counts_PL_max, orient=HORIZONTAL, cursor="dot", from_=0,
                                      to=1000, background=THEME_COLOR, highlightthickness=0)
        self.scale_counts_max.set(1000)
        self.scale_counts_max.grid(row=FILTER_ROW, column=1)

        self.names_counts_PL2022_min = IntVar()
        self.names_counts_PL2022_max = IntVar()
        self.scale_counts_min2022 = Scale(variable=self.names_counts_PL2022_min, orient=HORIZONTAL, cursor="dot",
                                          from_=-1,
                                          to=100, background=THEME_COLOR, highlightthickness=0)
        self.scale_counts_min2022.set(0)
        self.scale_counts_min2022.grid(row=FILTER_ROW, column=2)
        self.scale_counts_max2022 = Scale(variable=self.names_counts_PL2022_max, orient=HORIZONTAL, cursor="dot",
                                          from_=0,
                                          to=100, background=THEME_COLOR, highlightthickness=0)
        self.scale_counts_max2022.set(100)
        self.scale_counts_max2022.grid(row=FILTER_ROW, column=3)

        # Create a label widget
        # label = Label(win, font='Helvetica 15 bold')
        # label.pack()

        # Create a button to get the value at the scale
        # button = Button(win, text="Get Value", command=sel)
        # button.pack()

        # Buttons

        self.set_button = Button(image=self.apply_btn, command=self.apply_filters, highlightthickness=0, borderwidth=0, background=THEME_COLOR)
        self.set_button.grid(row=FILTER_ROW, column=4, padx=10, pady=20)

        self.boy_button = Button(image=self.img_baby_boy, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                 command=self.boy_clicked)
        self.boy_button.grid(row=ICON_ROW, column=0, padx=10, pady=20)
        self.girl_button = Button(image=self.img_baby_girl, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                  command=self.girl_clicked)
        self.girl_button.grid(row=ICON_ROW, column=1, padx=10, pady=20)
        self.check_button = Button(image=self.img_check, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                   command=self.like_clicked, state='disabled')
        self.check_button.grid(row=BUTTON_ROW, column=2, padx=10, pady=30)
        self.delete_button = Button(image=self.img_delete, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                    command=self.dislike_clicked, state='disabled')
        self.delete_button.grid(row=BUTTON_ROW, column=3, padx=10, pady=30)
        self.question_button = Button(image=self.exit_btn, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                      command=self.back_to_filters, state='disabled')
        self.question_button.grid(row=BUTTON_ROW, column=5, padx=10, pady=30)

        self.woman_button = Button(image=self.img_woman, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                   command=self.mom_clicked)
        self.woman_button.grid(row=ICON_ROW, column=2)
        self.man_button = Button(image=self.img_man, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                 command=self.dad_clicked)
        self.man_button.grid(row=ICON_ROW, column=3)
        self.comparison_button = Button(image=self.img_common, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                        command=self.show_common_choice)
        self.comparison_button.grid(row=ICON_ROW, column=4, padx=20, pady=20)

        self.save_button = Button(image=self.save_btn, command=self.save_to_file, highlightthickness=0, borderwidth=0, background=THEME_COLOR)
        self.save_button.grid(row=10, column=3)

        self.before_button = Button(image=self.before_btn, highlightthickness=0, borderwidth=0, background=THEME_COLOR, command=self.rev_before)
        self.before_button.grid(row=10, column=1)

        self.next_button = Button(image=self.next_btn, highlightthickness=0, borderwidth=0, background=THEME_COLOR,
                                    command=self.rev)
        self.next_button.grid(row=10, column=2)




        # Labels
        self.par_label_min_counts = Label(text="min liczba osób w PL", font=('Arial', 10), foreground='grey',
                                          background=THEME_COLOR)
        self.par_label_min_counts.grid(row=FILTER_LABEL_ROW, column=0)
        self.par_label_max_counts = Label(text="max liczba osób w PL", font=('Arial', 10), foreground='grey',
                                          background=THEME_COLOR)
        self.par_label_max_counts.grid(row=FILTER_LABEL_ROW, column=1)
        self.par_label_min_counts = Label(text="min w 2022 PL", font=('Arial', 10), foreground='grey',
                                          background=THEME_COLOR)
        self.par_label_min_counts.grid(row=FILTER_LABEL_ROW, column=2)
        self.par_label_max_counts = Label(text="max w 2022 w PL", font=('Arial', 10), foreground='grey',
                                          background=THEME_COLOR)
        self.par_label_max_counts.grid(row=FILTER_LABEL_ROW, column=3)

        self.boy_label = Label(text="chłopiec", font=('Ariel', 10, 'bold'), foreground='blue', background=THEME_COLOR)
        self.boy_label.grid(row=LABEL_ROW, column=0)

        self.girl_label = Label(text="dziewczynka", font=('Ariel', 10, 'bold'), foreground='#ff468c',
                                background=THEME_COLOR)
        self.girl_label.grid(row=LABEL_ROW, column=1)

        self.mom_label = Label(text="Mama", font=('Ariel', 10, 'bold'), foreground='grey',
                               background=THEME_COLOR)
        self.mom_label.grid(row=LABEL_ROW, column=2)

        self.daddy_label = Label(text="Tata", font=('Ariel', 10, 'bold'), foreground='grey',
                                 background=THEME_COLOR)
        self.daddy_label.grid(row=LABEL_ROW, column=3)

        self.daddy_label = Label(text="Wspólny Wybór", font=('Ariel', 10, 'bold'), foreground='black',
                                 background=THEME_COLOR)
        self.daddy_label.grid(row=LABEL_ROW, column=4)

        self.info_label = Label(text=self.info, font=('Ariel', 10, 'bold'), foreground=DARK_GREY,
                                background=THEME_COLOR)
        self.info_label.grid(row=INFO_ROW, column=4)

        self.info_counts_label = Label(text=self.info_counts, font=('Ariel', 10, 'bold'), foreground=DARK_GREY,
                                       background=THEME_COLOR)
        self.info_counts_label.grid(row=INFO_ROW, column=0)

        self.info_counts_2022_label = Label(text=self.info_counts_2022, font=('Ariel', 10, 'bold'),
                                            foreground=DARK_GREY,
                                            background=THEME_COLOR)
        self.info_counts_2022_label.grid(row=INFO_ROW, column=2)

        # Canvas
        self.canvas = Canvas(width=450, height=100, background=THEME_COLOR, borderwidth=0, highlightthickness=0)
        if self.names_bank.data.loc[self.names_bank.data.index[self.current_position]]['Gender'] == 'male':
            fill_color = 'blue'
        else:
            fill_color = '#ff468c'

        if not self.game_over:
            self.name_text = self.canvas.create_text(300, 50,
                                                     text=self.names_bank.data.loc[
                                                         self.names_bank.data.index[self.current_position]]['Name'],
                                                     fill=fill_color,
                                                     font=('Arial', 35, 'italic'),
                                                     width=500,
                                                     justify='right')
        else:
            self.name_text = self.canvas.create_text(300, 50,
                                                     text="USTAW FILTRY",
                                                     fill='black',
                                                     font=('Arial', 30, 'italic'),
                                                     width=500,
                                                     justify='center')
        self.canvas.grid(row=CANVAS_ROW, column=0, columnspan=5, pady=10, padx=0)

        self.hide_buttons()

    def save_to_file(self):

        self.names_bank.save_choices()

    def show_common_choice(self):

        self.names_bank.common_choice()
        self.current_position = 0
        print(self.names_bank.data)
        self.get_next_name()

    def rev(self):
        if self.current_position < len(self.names_bank.data)-1:
            self.current_position = self.current_position + 1
        self.get_next_name()

    def rev_before(self):
        if self.current_position > 0:
            self.current_position = self.current_position - 1
        self.get_next_name()




