import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Style Configuration
style = ttk.Style()
style.configure('Treeview', rowheight=30, font=('Arial', 10), padding=(10, 5))
style.configure('Treeview.Row', borderwidth=1, relief='solid')  # Custom style for rows

# Custom styles for odd and even rows
style.configure('Treeview.OddRow', background='lightgray')
style.configure('Treeview.EvenRow', background='white')

# Treeview Widget
columns = ('Column 1', 'Column 2', 'Column 3')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)  # Adjust the column width as needed

# Sample Data
data = [('Row 1', 'Data A', 'Value 1'),
        ('Row 2', 'Data B', 'Value 2'),
        ('Row 3', 'Data C', 'Value 3')]

# Insert Data into Treeview with alternating row styles
for idx, row in enumerate(data):
    tags = ('Treeview.OddRow',) if idx % 2 == 1 else ('Treeview.EvenRow',)
    tree.insert('', 'end', values=row, tags=tags + ('Treeview.Row',))

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.config(yscrollcommand=scrollbar.set)

# Pack Treeview
tree.pack(side='left', fill='both', expand=True)

root.mainloop()
