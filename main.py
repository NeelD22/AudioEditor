"""
Code illustration: 2.12.py
Features Added:
    Add context/ Pop-up Menu
    Set focus on launch

@Tkinter GUI Application Development Blueprints
"""
"""
Code illustration: 2.12.py
Features Added:
    Add context/ Pop-up Menu
    Set focus on launch

@Tkinter GUI Application Development Blueprints
"""
import os
from tkinter import Tk, PhotoImage, Menu, Frame, Text, Scrollbar, IntVar, \
    StringVar, BooleanVar, Button, END, Label, INSERT
import tkinter.filedialog
import tkinter.messagebox

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
from tkinter import StringVar, IntVar
import json
import requests
import time
import json
import numpy as np
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
from tkinter import StringVar, IntVar




#CURRENTLY THE NEWEST ASSEMBLY PART OF CODE


AssemblyKey = "a5299ec7135747478e2eb8aa2fe00ac6"

upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers_authorisation = {'authorization': AssemblyKey}
headers = {"authorization": AssemblyKey,
           "content-type": "application/json"}
chunk_size = 5242880

filename = r"C:\Users\NeelD\Documents\Simple_Transcription\Listen To Your Inner Child _ Hayley Ep 6.mp4"


# Upload
def upload(filename):
    # reads audio file
    def read_file(filename):
        with open(filename, 'rb') as file:
            while True:  # infinte while loop
                data = file.read(chunk_size)  # returns chunksize
                if not data:  # when all the data is read
                    break
                # returns generator obj
                yield data  # converts expression into generator func (spec function to be iterated to give the values)

    # send post request to end point
    # When you want to send data to a server
    # Post method specifies that a client that a client is posting data on a given endpoint
    # Upload is a json response (key) from assemblyai which points to a backend server
    # Post request gives an id key and a status key
    # The status key shows the status of your transcription, starts with queued then goes to processing and finally completed
    # print(response.json())#to see what response assemblyai gives
    # need to extract response
    upload_response = requests.post(upload_endpoint, headers=headers_authorisation, data=read_file(filename))
    audio_url = upload_response.json()['upload_url']
    # print("This is audiourl", audio_url)
    return audio_url


# After submitting an audio file for processing the "status" key goes from "queued" to "processing" to completedcchcjcjc
# get request to get status of transcript: completed or error
# One has to make repeated get requests until status is completed or error
# Once status is shown as completed, you'll see the text

# Transcribe
def transcribe(audio_url):
    # transcript request has just audiourl details
    transcript_request = {"audio_url": audio_url, "speaker_labels": True}
    headers = {"authorization": AssemblyKey,
               "content-type": "application/json"}
    # transcript response is where to
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    transcript_id = transcript_response.json()['id']
    # print('Text:', transcript_response.json()['text'])
    # print("This is transcript response: ", transcript_response.json())
    # print("This is transcriptid", transcript_id)
    return transcript_id


# poll
# writing code which will keep polling assemblyai
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    # gives status of transcript:
    # polling response has everything from details of the audio file, status of transcription, to the actual text transcription
    polling_response = requests.get(polling_endpoint, headers=headers)
    # print("this is polling response",polling_response.json())
    return polling_response


# in the example the status was pending, so we need to repeatedly ask assemblyai if it is done

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    linearray = []
    confidence_list = []
    confidence_error_values = []
    counter = 1
    error_val = 0.2
    highlighted_words = []
    while True:
        data = poll(transcript_id)  # gives the entirety of the polling response - including status
        text = data.json()['text']
        status = data.json()['status']
        print("This is the status of the transcription: ", status)
        data2 = json.loads(data.text)

        if data.json()['status'] == "completed":
            words = data.json()['words']

            print("text: ", text)
            print('words: ', words)

            with open('AssemblyDataFile.txt', "w") as f:
                json.dump(data2, f, indent=4)

            return data


        elif status == "error":
            print('error')

        print("waiting for 30 seconds")
        time.sleep(30)

# Word by word Indexer
def create_indexer(data):
    words = data.json()['words']
    indexer = [[]]
    temparray = []
    for w in words:
        temparray = list(w.values())

        indexer.append(temparray)

    indexer.pop(0)
    # adding other attributes to indexer!
    highlighted_or_not = False
    edited_or_not = False
    character_index1 = 0
    character_index2 = 0

    for block in indexer:
        block.append(highlighted_or_not)
        block.append(edited_or_not)
        # Character Tag line
        block.append(character_index1)
        block.append(character_index2)

    return indexer

def place_indexer_in_file(indexer):
    with open('Indexer_file.txt', "w") as f:
        for block in indexer:
            for element in block:
                f.write(str(element) + " ")
            f.write("\n")


audio_url = upload(filename)
data = get_transcription_result_url(audio_url)
indexer = create_indexer(data)

# MOVED TO SCRATCHES\SCRATCH_8


#TK Window displayer using file


PROGRAM_NAME = "Transcript!"
file_name = None

root = Tk()
root.geometry('1500x1500')
root.title(PROGRAM_NAME)

# show pop-up menu


def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)


def show_cursor_info_bar():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor_info_bar(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)


def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(
        background=background_color, fg=foreground_color)


def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')


def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


def on_content_changed(event=None):
    update_line_numbers()
    update_cursor_info_bar()


def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output


def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "About", "{}{}".format(PROGRAM_NAME, "\nTkinter GUI Application\n Development Blueprints"))


def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo(
        "Help", "Help Book: \nTkinter GUI Application\n Development Blueprints",
        icon='question')


def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()


def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()


def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
        on_content_changed()


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        tkinter.messagebox.showwarning("Save", "Could not save the file.")


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"


def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"


def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"


def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)

    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')

    search_entry_widget = Entry(
        search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(
        row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               content_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"


def search_output(needle, if_ignore_case, content_text,
                  search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos,
                                            nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config(
            'match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"


def copy():
    content_text.event_generate("<<Copy>>")
    return "break"


def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"


def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return 'break'


new_file_icon = PhotoImage(file='icons/new_file.gif')
open_file_icon = PhotoImage(file='icons/open_file.gif')
save_file_icon = PhotoImage(file='icons/save.gif')
cut_icon = PhotoImage(file='icons/cut.gif')
copy_icon = PhotoImage(file='icons/copy.gif')
paste_icon = PhotoImage(file='icons/paste.gif')
undo_icon = PhotoImage(file='icons/undo.gif')
redo_icon = PhotoImage(file='icons/redo.gif')

menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left',
                      image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left',
                      image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label='Save', accelerator='Ctrl+S',
                      compound='left', image=save_file_icon, underline=0, command=save)
file_menu.add_command(
    label='Save as', accelerator='Shift+Ctrl+S', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl+Z',
                      compound='left', image=undo_icon, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y',
                      compound='left', image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X',
                      compound='left', image=cut_icon, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl+C',
                      compound='left', image=copy_icon, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V',
                      compound='left', image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', underline=0,
                      accelerator='Ctrl+F', command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', underline=7,
                      accelerator='Ctrl+A', command=select_all)
menu_bar.add_cascade(label='Edit', menu=edit_menu)


view_menu = Menu(menu_bar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label='Show Line Number', variable=show_line_number,
                          command=update_line_numbers)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(
    label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor_info_bar)
to_highlight_line = BooleanVar()
view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1,
                          offvalue=0, variable=to_highlight_line, command=toggle_highlight)
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)

color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(
        label=k, variable=theme_choice, command=change_theme)
menu_bar.add_cascade(label='View', menu=view_menu)

about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label='About', command=display_about_messagebox)
about_menu.add_command(label='Help', command=display_help_messagebox)
menu_bar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menu_bar)

shortcut_bar = Frame(root,  height=25)
shortcut_bar.pack(expand='no', fill='x')

icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
         'undo', 'redo', 'find_text')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(icon))
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')

line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0,
                       background='khaki', state='disabled',  wrap='none')
line_number_bar.pack(side='left',  fill='y')

content_text = Text(root, width=80, font = ('Courier, 12'), wrap='word', undo=1)
#Text(parent, width = chars, font = ('Helvetica, 24'))
content_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')


content_text.bind('<KeyPress-F1>', display_help_messagebox)
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-f>', find_text)
content_text.bind('<Control-F>', find_text)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='ivory2')

# set up the pop-up menu
popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=select_all)
content_text.bind('<Button-3>', show_popup_menu)


# bind right mouse click to show pop up and set focus to text widget on launch
content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()

with open("TranscriptVol4.txt", 'r') as file:
    for line in file:
        content_text.insert(tk.INSERT, line)

#Open indexer file and get all the words
def word_extractor():
    first_word_array = []
    with open('Indexer_file.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            first_word = line.split()[0]
            first_word_array.append(first_word)
    return first_word_array

first_word_array = word_extractor()

def give_indexer(word, widget):
    start_index_array = []
    end_index_array = []
    start_index = '1.0'
    while True:
        start_index = widget.search(word, start_index, stopindex=tk.END)
        if not start_index:
            break
        end_index = f"{start_index}+{len(word)}c"
        #widget.tag_add('highlight', start_index, end_index)
        start_index = end_index
        start_index_array.append(start_index)
        end_index_array.append(end_index)
        with open('Indexer_file.txt', 'r') as f:
            with open('output214.txt', 'w') as output:
                for i in start_index:
                    # Loop through each line in the input file
                    for line in f:
                        # Remove the newline character from the end of the line
                        line = line.rstrip('\n')

                        # Append the elements to the end of the line using string concatenation
                        line = line + " ".join(i)
                        #line = line + " " + " ".join(end_index)

                        # Write the modified line to the output file
                        output.write(line + '\n')

    return start_index_array, end_index_array




        #content_text.tag_configure('highlight', background='yellow')
        #content_text.tag_add('highlight', start_index, end_index)

#Incomplete highlighter function currently working on
def highlight():
    mydict = {}
    linearray = []
    confidence_list = []
    confidence_error_values = []
    counter = 1
    error_val = 0.2
    with open(r"TranscriptWindow.txt", 'r') as window:
        data = window.read()
        words = data.split()
        for word in words:
            start_index_array, end_index_array = give_indexer(word, content_text)

    with open('Indexer_file.txt', 'r') as f:
        contents = f.read()

    lines = contents.splitlines()

    for line in lines:
        elements = line.split(' ')
        confidence = elements[3]




    #print('confidence:', confidence)

highlight()

#Old Highlighter Function
def highlighter_calc(indexer):
    print('highlighter_calc index:', indexer)
    mydict = {}
    linearray = []
    confidence_list = []
    confidence_error_values = []
    counter = 1
    error_val = 0.2
    #
    highlighted_words = []
    for i in indexer:  # create a dict which associates word w confid
        word = i[0]
        start = i[1]
        confidence = i[2]
        confidence_list.append(confidence)
        mydict.update({confidence: start})


    sorted_list = sorted(confidence_list)
    # print("sorted list: ", sorted_list)

    number_of_possible_errors = error_val * len(confidence_list)
    roundedno = round(number_of_possible_errors)
    # print("no of poss errors: ", roundedno)

    confidence_error_values = sorted_list[:roundedno]
    # print(confidence_error_values)
    for n in confidence_error_values:
        tempsolution = mydict.get(n)
        highlighted_words.append(tempsolution)

    return highlighted_words





#1.) Calculate index of each word
#2.) Calculate words to be highlighted and then return with those words its specific index and change if needs to b highlighted in indexer,
#3.) Iterate through indexer: if needs to be highlighted, then do tag_add(index1,index2) to highlight

root.protocol('WM_DELETE_WINDOW', exit_editor)




root.mainloop()