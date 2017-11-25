import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox as tmb
import os # for handling file operations
file_name = None
PROGRAM_NAME = 'Python Text Editor'

root = tk.Tk()
root.title(PROGRAM_NAME)
root.geometry("500x500") # default size of the root window

###################### MENU BAR STARTS HERE ###########################################################
menu_bar = tk.Menu(root)


# When TEAROFF is set to 1 (enabled),the menu appears with a dotted line above
# the menu options. Clicking on the dotted line enables the user to literally
# tear off or separate the menu from the top. However, as this is not a
# cross-platform feature, we have decided to disable tear-off, marking it as
# tearoff = 0.
########################### FILE_MENU ################################################################
file_menu = tk.Menu(menu_bar, tearoff = 0) # tearoff is kindda ugly so 0 it is
# all file menu-items will be added here next
##### CALLBACKS for FILE_MENU
def new_file(event=None): # callback function
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0,tk.END)
    on_content_changed()
def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                filetypes=[("All Files", "*.*"), ("Text Documents","*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name),
        PROGRAM_NAME)) # in case filedialog returns a valid filename, we
        # isolate the filename using the os module and
        # add it as the title of the root window
        content_text.delete(1.0, tk.END)
        content_text.bind('<Any-KeyPress>', on_content_changed)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
    on_content_changed()
def save_file(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
            write_to_file(file_name)
    return "break"
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                        filetypes=[("All Files", "*.*"),
                        ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"
def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file: the_file.write(content)
    except IOError:
        pass
    # pass for now but we show some warning - we do this in next iteration
def exit_file(event = None):
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()
# Must declare image here and must be .gif/PGM/PPM for the PhotoImage class
# There are other alternatives to PhotoImage
##################### NEW FILE
new_file_icon = tk.PhotoImage(file = 'static/menu_bar/new_file.gif')
# The UNDERLINE option lets you specify the index of a character in the menu
# text that needs to be underlined.
file_menu.add_command(label = 'New', accelerator = 'Ctrl + N', compound = 'left',
                        image = new_file_icon, underline = 0,
                        command = new_file)
##################### OPEN_FILE
open_file_icon = tk.PhotoImage(file = 'static/menu_bar/open_file.gif')
file_menu.add_command(label = 'Open', underline = 0, accelerator = 'Ctrl + O',
                        compound = 'left',image = open_file_icon,
                        command = open_file)
##################### SAVE_FILE
save_file_icon = tk.PhotoImage(file = 'static/menu_bar/save_file.gif')
file_menu.add_command(label = 'Save as', underline = 0, accelerator = 'Ctrl + S',
                        compound = 'left', image = save_file_icon,
                        command = save_file)
##################### SAVE_AS
save_as_file_icon = tk.PhotoImage(file = 'static/menu_bar/save_as_file_icon.gif')
file_menu.add_command(label = 'Save', underline = 0,compound = 'left',
                        image = save_as_file_icon, command = save_file)
file_menu.add_separator() # separation line
##################### EXIT
exit_icon = tk.PhotoImage(file = 'static/menu_bar/exit.gif')
file_menu.add_command(label = 'Exit', underline = 1, accelerator = 'Alt + F4',
                        compound = 'left', image = exit_icon, command = exit_file)
menu_bar.add_cascade(label='File', menu=file_menu)

############################### EDIT MENU #################################################################
edit_menu = tk.Menu(menu_bar, tearoff = 0)
### EDIT MENU CALLBACKS
def undo():
    content_text.event_generate("<<Undo>>") # context_text - where we write
    on_content_changed()
def redo_action(event = None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return "break" # The return 'break' expression in the preceding function
# tells the system that it has performed the event and that it should not be
# propagated further.
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
def copy():
    content_text.event_generate("<<Copy>>")
    return "break"
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
def find_text():
    search_toplevel = tk.Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    tk.Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = tk.Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set() # text cursor brought to this Entry
    ignore_case_value = tk.IntVar()
    tk.Checkbutton(search_toplevel, text='IgnoreCase',
                variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                padx=2, pady=2)
    tk.Button(search_toplevel, text="Find All", underline=0,
            command=lambda: search_output(search_entry_widget.get(),
            ignore_case_value.get(), content_text, search_toplevel,
            search_entry_widget)).grid(row=0, column=2, sticky='e' +'w',padx=2,
            pady=2)
    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"
def search_output(needle, if_ignore_case, content_text,search_toplevel,search_box):
    content_text.tag_remove('match', '1.0', tk.END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
    while True:
        start_pos = content_text.search(needle, start_pos,nocase=if_ignore_case,
                                        stopindex= tk.END)
        if not start_pos:
            break
        end_pos = '{}+{}c'.format(start_pos, len(needle))
        content_text.tag_add('match', start_pos, end_pos)
        matches_found += 1
        start_pos = end_pos
    content_text.tag_config('match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matchesfound'.format(matches_found))
def select_all(event = None):
    content_text.tag_add("sel", "1.0", "end")
    return "break"
# all edit menu-items will be added here next
#################### UNDO
undo_icon = tk.PhotoImage(file = 'static/menu_bar/undo.gif')
edit_menu.add_command(label = 'Undo', accelerator = 'Ctrl + Z', compound = 'left',
                        image = undo_icon, command = undo)
#################### REDO
redo_action = tk.PhotoImage(file = 'static/menu_bar/redo_action.gif')
edit_menu.add_command(label = 'Redo', accelerator = 'Shift + Ctrl + Z',
                        compound = 'left', image = redo_action,
                        command = redo_action)
edit_menu.add_separator()

#################### CUT
cut_icon = tk.PhotoImage(file = 'static/menu_bar/cut.gif')
edit_menu.add_command(label = 'Cut', accelerator = 'Ctrl + X',
                        compound = 'left', image = cut_icon, command = cut)

#################### COPY
copy_icon = tk.PhotoImage(file = 'static/menu_bar/copy.gif')
edit_menu.add_command(label = 'Copy', accelerator = 'Ctrl + C',
                        compound = 'left', image = copy_icon, command = copy)

#################### PASTE
paste_icon = tk.PhotoImage(file = 'static/menu_bar/paste.gif')
edit_menu.add_command(label = 'Paste', accelerator = 'Ctrl + V',
                        compound = 'left', image = paste_icon, command = paste)
edit_menu.add_separator()
#################### FIND
find_icon = tk.PhotoImage(file = 'static/menu_bar/find_text.gif')
edit_menu.add_command(label = 'Find', accelerator = 'Ctrl + F',
                        compound = 'left', image = find_icon, command = find_text)
edit_menu.add_separator()
##################### SELECT ALL
select_all_icon = tk.PhotoImage(file = 'static/menu_bar/select_all.gif')
edit_menu.add_command(label = 'Select all', accelerator = 'Ctrl + A',
                        compound = 'left', image = select_all_icon,
                        command = select_all)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

############################ VIEW MENU #########################################################
view_menu = tk.Menu(menu_bar, tearoff = 0)
def show_line_no():
    dir(print("OK"))
def highlight():
    dir(print("OK"))
# all view menu-items will be added here next
show_line_no = tk.IntVar()
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_no)
view_menu.add_checkbutton(label = "Show Cursor Location at Bottom",
                        variable = show_line_no)
show_line_no.set(1)
view_menu.add_checkbutton(label = "Highlight Current Line", variable = highlight)
themes_menu = tk.Menu(view_menu, tearoff = 0)
view_menu.add_cascade(label="Themes", menu=themes_menu)
themes_menu.add_radiobutton(label = "Defalut")
themes_menu.add_radiobutton(label = "Blue")
themes_menu.add_radiobutton(label = "Yellow")
themes_menu.add_radiobutton(label = "Red")
menu_bar.add_cascade(label = 'View', menu = view_menu)
############################### ABOUT MENU ##########################################################
about_menu = tk.Menu(menu_bar, tearoff = 0)
# all about menu-items will be added here next
def about(event=None):
    tkinter.messagebox.showinfo("About", "{}{}".format(PROGRAM_NAME,
                            "\nTkinter GUIApplication\n Development Blueprints"))
def help_action(event=None):
    tkinter.messagebox.showinfo("Help",
    "Help Book: \nTkinter GUI Application\n DevelopmentBlueprints",
    icon='question')
about_menu.add_command(label = 'About', compound = 'left', command = about)
about_menu.add_command(label = 'Help', compound = 'left', command = help_action)
menu_bar.add_cascade(label = 'About', menu = about_menu)
###################### MENU BAR ENDS HERE ###########################################################
root.config(menu=menu_bar)
###################### SHORTCUTS BAR MENU ##########################################################
shortcut_bar = tk.Frame(root, height=25, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')
icons = ('new_file', 'open_file', 'save_file', 'cut', 'copy', 'paste','undo',
        'redo_action','find_text')
for i, icon in enumerate(icons):
    tool_bar_icon = tk.PhotoImage(file='static/menu_bar/{}.gif'.format(icon))
    cmd = eval(icon)
    tool_bar = tk.Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')
###################### LINE NUMBER BAR ##############################################################
line_number_bar = tk.Text(root, width = 4, padx = 3, border = 0, takefocus = 0,
                    state = 'disabled',background='khaki', wrap='none')
def on_content_changed(event=None):
    update_line_numbers()
def update_line_numbers():
    content_text.bind('<Any-KeyPress>', on_content_changed)
def get_line_numbers():
    output = ''
    if show_line_no.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i)+ '\n'
    return output
def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')
line_number_bar.pack(side='left', fill='y')

################## CONTEXT TEXT #######################################################################
content_text = tk.Text(root, wrap = 'word', undo = 1) # undo = 1 should allow...
#... the Text widget to have anunlimited undo and redo mechanism
content_text.pack(expand = 'yes', fill = 'both')
content_text.focus() # text-cursor set in content_text
content_text.bind('<Control-Z>', redo_action) # this changes the default of
# <<Redo>> to Shift-Ctrl-Z; if it where <Control-z> NB the lowercase, then it
# would had been Ctrl-Z
content_text.bind('<Control-a>', select_all)
scroll_bar = tk.Scrollbar(content_text)
content_text.config(yscrollcommand = scroll_bar.set)
scroll_bar.config(command = content_text.yview)
root.protocol('WM_DELETE_WINDOW', exit_file)
root.mainloop()