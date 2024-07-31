import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser

class Notepad:
    def __init__(self, **kwargs):
        self.root = tk.Tk()
        self.file = None
        self.initUI()

    def initUI(self):
        # Set icon and title
        self.root.title("Untitled - Notepad")
        self.root.geometry('800x600')

        # Create Menu Bar
        self.menu_bar = tk.Menu(self.root)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_format_menu()
        self.create_help_menu()
        self.root.config(menu=self.menu_bar)

        # Create Toolbar
        self.toolbar = tk.Frame(self.root, bg='lightgrey')
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add buttons to toolbar
        self.create_toolbar_buttons()

        # Create Text Area
        self.text_area = tk.Text(self.root, wrap=tk.WORD, font=('Arial', 12), undo=True)
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Setup automatic save
        self.auto_save_interval = 60000  # 60 seconds
        self.auto_save_job = None
        self.setup_auto_save()

    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_application)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def create_format_menu(self):
        format_menu = tk.Menu(self.menu_bar, tearoff=0)
        format_menu.add_command(label="Font...", command=self.change_font)
        format_menu.add_command(label="Background Color...", command=self.change_bg_color)
        format_menu.add_command(label="Text Color...", command=self.change_text_color)
        self.menu_bar.add_cascade(label="Format", menu=format_menu)

    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_toolbar_buttons(self):
        # Toolbar buttons with improved appearance
        button_style = {
            'bg': '#4CAF50',  # Background color
            'fg': 'white',    # Text color
            'font': ('Arial', 10, 'bold'),
            'padx': 5,
            'pady': 2,
            'bd': 2,
            'relief': tk.RAISED
        }

        # Button callback functions
        def on_enter(e):
            e.widget['bg'] = '#45a049'  # Darker green on hover

        def on_leave(e):
            e.widget['bg'] = '#4CAF50'  # Original green color

        # Create buttons
        buttons = {
            'New': self.new_file,
            'Open': self.open_file,
            'Save': self.save_file,
            'Save As': self.save_file_as,
            'Cut': self.cut,
            'Copy': self.copy,
            'Paste': self.paste,
            'Undo': self.undo,
            'Redo': self.redo
        }

        # Add buttons to toolbar
        for text, command in buttons.items():
            btn = tk.Button(self.toolbar, text=text, command=command, **button_style)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

    def quit_application(self):
        if self.auto_save_job:
            self.root.after_cancel(self.auto_save_job)
        self.root.destroy()

    def show_about(self):
        messagebox.showinfo("Notepad", "Simple Notepad Application")

    def open_file(self):
        self.file = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("All Files", "*.*"),
                                                         ("Text Documents", "*.txt")])
        if self.file:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            with open(self.file, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, file.read())

    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, tk.END)

    def save_file(self):
        if not self.file:
            self.save_file_as()
        else:
            with open(self.file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
            self.root.title(os.path.basename(self.file) + " - Notepad")

    def save_file_as(self):
        self.file = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                                defaultextension=".txt",
                                                filetypes=[("All Files", "*.*"),
                                                           ("Text Documents", "*.txt")])
        if self.file:
            self.save_file()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            messagebox.showwarning("Undo", "Nothing to undo")

    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            messagebox.showwarning("Redo", "Nothing to redo")

    def find_text(self):
        search_term = simpledialog.askstring("Find", "Enter text to find:")
        if search_term:
            self.text_area.tag_remove("found", "1.0", tk.END)
            start = "1.0"
            while True:
                start = self.text_area.search(search_term, start, stopindex=tk.END)
                if not start:
                    break
                end = f"{start}+{len(search_term)}c"
                self.text_area.tag_add("found", start, end)
                start = end
            self.text_area.tag_config("found", background="yellow")

    def replace_text(self):
        find_text = simpledialog.askstring("Find", "Enter text to find:")
        replace_text = simpledialog.askstring("Replace", "Enter replacement text:")
        if find_text and replace_text:
            content = self.text_area.get(1.0, tk.END)
            updated_content = content.replace(find_text, replace_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, updated_content)

    def change_font(self):
        font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
        font_size = simpledialog.askinteger("Font Size", "Enter font size:")
        if font_family and font_size:
            self.text_area.config(font=(font_family, font_size))

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(bg=color)

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(fg=color)

    def setup_auto_save(self):
        self.auto_save_job = self.root.after(self.auto_save_interval, self.auto_save)

    def auto_save(self):
        if self.file:
            with open(self.file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
        self.auto_save_job = self.root.after(self.auto_save_interval, self.auto_save)

    def run(self):
        self.root.mainloop()

# Run main application
if __name__ == "__main__":
    notepad = Notepad()
    notepad.run()
