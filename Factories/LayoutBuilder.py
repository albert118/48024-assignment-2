from tkinter import *
from tkinter.ttk import *
from Factories.AssetUtil import load_asset
import Styles


class LayoutBuilder:
    def __init__(self, window: Tk, dimms: tuple):
        self._dimms = dimms
        self._window = window
        self._row_ctr = 0
        self.primary_btn = None
        self.form_entries = []

        Styles.setup_styling()

        # equally space the grid
        for i in range(dimms[0]): window.columnconfigure(i, weight=1)

        # add some default weighting to the expected rows
        self._window.rowconfigure(0, weight=1)
        self._window.rowconfigure(1, weight=1)
        self._window.rowconfigure(2, weight=2)
        self._window.rowconfigure(3, weight=1)

    def add_heading(self, menu_message: str):
        welcome_frame = Frame(self._window)
        welcome_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0])
        Label(welcome_frame, text=menu_message).grid(row=self._row_ctr, column=0, pady=(0, 15))

        # Set the minimum height for the heading row
        self._window.grid_rowconfigure(self._row_ctr, minsize=1)

        self._heading_row_num = self._row_ctr
        self._row_ctr += 1

        return self
    
    def add_error_message(self, error_message: Exception):
        exception_frame = Frame(self._window)
        exception_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0])

        Label(exception_frame, text=error_message.__class__.__name__, style='ExceptionType.TLabel').grid(
            row=self._row_ctr, 
            column=0, 
            pady=(0, 15)
        )

        self._row_ctr += 1

        Label(exception_frame, text=str(error_message).capitalize(), style='ErrorMessage.TLabel').grid(
            row=self._row_ctr, 
            column=0, 
            pady=(0, 15)
        )

        self._row_ctr += 1
    
    def add_image(self, window_width, image_fn):
        try:
            # load the splash image and attach it to a new label
            photo_image = load_asset(image_fn, new_width=window_width)
            image_label = Label(self._window, image=photo_image)
            image_label.image = photo_image
            image_label.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0])
            
            self._row_ctr += 1
        except Exception as ex:
            print(f'{__name__}: could not add image "{image_fn}" for window_width "{window_width}", {ex}')

        return self
    
    def add_separator(self):
        Separator(
            master=self._window,
            orient=HORIZONTAL,
            style='TSeparator',
            class_=Separator
        ).grid(
            row=self._row_ctr,
            column=0,
            columnspan=self._dimms[0],
            sticky='we',
            pady=(0, 15)
        )

        self._row_ctr += 1

        return self
    
    def add_form(self, form_fields: dict):
        # add an input frame
        inputs_frame = Frame(self._window)
        inputs_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0])
        self._row_ctr += 1

        is_first = True
        for field in form_fields:
            field_label = Label(inputs_frame, text=f'{field}:')
            field_label.grid(row=self._row_ctr, column=0, sticky='w', padx=5, pady=5)
            
            # track the entry using the given dict
            # this lets me use it later in a callback to submit
            field_entry = Entry(inputs_frame)
            field_entry.grid(row=self._row_ctr, column=1, sticky='e', pady=5)
            field_entry.bind('<KeyRelease>', self._validate_all_exist)
            # these could be combined for efficiency
            # but I don't care to make this too re-usable
            form_fields[field] = field_entry
            self.form_entries.append(field_entry)

            if is_first:
                field_entry.focus_force()
                is_first = False

            self._row_ctr += 1

        return self

    def _validate_all_exist(self, value):
        '''track form entries and validate entries have all been made to unlock submission'''
        if all(val.get() for val in self.form_entries) and self.primary_btn is not None:
            self.primary_btn.config(state='normal')
        else:
            self.primary_btn.config(state='disabled')

        return True

    def add_table_data(self, window_width: int, table_data=None):
        if (table_data is None):
            return self

        table_frame = Frame(self._window)
        # sticky is required for a frame to stretch to rowspan
        table_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0], sticky='ns')

        self._row_ctr += 1

        # utilise the Treeview to enable scrolling
        table = Treeview(
            table_frame,
            columns=table_data['columns'],
            show='headings'
        )

        # add headings and data
        for column in table_data['columns']:
            table.heading(column, text=column)
            table.column(column, width=(window_width // len(table_data['columns'])), anchor='center')

        # rows should alternate, using tags alternate (I think lightgray and white are the example?)
        table.tag_configure('oddrow', background='#f2f1f1')
        table.tag_configure('evenrow', background='white')

        for idx, row in enumerate(table_data['rows']):
            tags = ('evenrow',) if idx % 2 == 0 else ('oddrow',)
            table.insert('', 'end', values=row, tags=tags, iid=idx)

        # include a scrollbar as spec'd
        scrollbar = Scrollbar(table_frame, orient='vertical', command=table.yview)
        scrollbar.pack(side='right', fill='y')

        # finalise the table
        table.config(yscrollcommand=scrollbar.set)
        table.pack(side='left', fill='both', expand=True)
        
        return self

    def add_menu(self, menu_items: dict, disable_primary_action=False):
        '''the first action (ie. leftmost) is considered the primary action'''

        column_ctr = 0
        is_first = True
        for item in menu_items:
            # flex these buttons and fill the x-axis as per the design spec
            btn = Button(self._window, text=item, command=menu_items[item])
            btn.grid(
                row=self._row_ctr,
                column=column_ctr,
                sticky='we',
                pady=(20, 0)
            )

            if is_first:
                if disable_primary_action:
                    self.primary_btn = btn
                    self.primary_btn.config(state='disabled')

                is_first = False

            column_ctr += 1
        
        self._row_ctr += 1
        
        return self
