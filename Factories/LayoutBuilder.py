from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from Factories.AssetUtil import load_asset
import Styles


# helpers

def on_entry_focus(event):
    event.widget.config(highlightcolor='#168FC1')

def on_entry_blur(event):
    event.widget.config(highlightcolor='gray')

class LayoutBuilder:
    def __init__(self, window: Tk, dimms: tuple):
        self._dimms = dimms
        self._window = window
        self._row_ctr = 0
        self.primary_btn = None
        self._table = None
        self.selected_row = None
        self.form_entries = []

        Styles.setup_styling()

        # equally space the grid
        for i in range(dimms[0]): window.columnconfigure(i, weight=1)

        # add some default weighting to the expected rows
        self._window.rowconfigure(0, weight=1)
        self._window.rowconfigure(1, weight=1)
        self._window.rowconfigure(2, weight=2)
        self._window.rowconfigure(3, weight=1)

    def configure_rows_big(self):
        for i in range(self._row_ctr):
            self._window.rowconfigure(i, weight=1)

        # filter configured? Then different layout
        if self._table is not None:
            self._window.rowconfigure(6, weight=8) # the data-table row
        else:
            self._window.rowconfigure(4, weight=8) # the data-table row

        return self

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
            field_entry = tk.Entry(inputs_frame, highlightthickness=2)
            field_entry.grid(row=self._row_ctr, column=1, sticky='e', pady=5)
            field_entry.bind('<KeyRelease>', self._validate_all_exist)
            field_entry.bind("<FocusIn>", on_entry_focus)
            field_entry.bind("<FocusOut>", on_entry_blur)
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

    def add_filter(self, filters: dict):
        # add an input frame for the filter
        filter_frame = Frame(self._window)
        filter_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0])

        # ensure the entire column width is consumed
        for i in range(self._dimms[0]): filter_frame.columnconfigure(i, weight=1)
        # filter label and inputs are stacked vertically unlike normal forms
        for filter in filters:
            filter_label = Label(filter_frame, text=filter)
            filter_label.grid(row=self._row_ctr, column=1, pady=2)

            self._row_ctr += 1

            field_entry = tk.Entry(filter_frame, highlightthickness=2)
            field_entry.grid(row=self._row_ctr, column=1, sticky='e', pady=5)
            field_entry.bind('<KeyRelease>', self._validate_all_exist)
            field_entry.bind("<FocusIn>", on_entry_focus)
            field_entry.bind("<FocusOut>", on_entry_blur)

            # entry should be full-width
            field_entry.grid(row=self._row_ctr, column=1, columnspan=self._dimms[0])
            field_entry.bind('<KeyRelease>', lambda x: filters[filter](field_entry.get(), self._table))

            self._row_ctr += 1

    def add_table_data(self, window_width: int, table_data=None, filters=None, navigate_kwargs={}):
        if table_data is None: return self

        table_frame = Frame(self._window)
        # utilise the Treeview to enable scrolling
        table = Treeview(
            table_frame,
            columns=table_data['columns'],
            show='headings',
            selectmode='browse',
            height=10
        )
        self._table = table

        if filters is not None:
            self.add_filter(filters)
            # store a ref to table for filtering

        table_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0], sticky='ns')

        self._row_ctr += 1

        # add headings and data
        for column in table_data['columns']:
            table.heading(column, text=column)
            table.column(column, width=(window_width // len(table_data['columns'])), anchor='w')

        self.add_table_rows(table, table_data['rows'], navigate_kwargs)
        self._add_scrollbar_to_table(table_frame, table)
        table.pack(side='left', fill='both', expand=True)
        
        return self
    
    def add_list_view(self, list_data: dict, navigate_kwargs={}):
        view_frame = Frame(self._window)
        view_frame.grid(row=self._row_ctr, column=0, columnspan=self._dimms[0], sticky='nsew')

        self._row_ctr += 1

        if list_data['data'] is None or len(list_data['data']) == 0:
            no_data_label = Label(view_frame, text=list_data['default'])
            no_data_label.grid(row=self._row_ctr, pady=(40, 20))
        else:
            table = Treeview(
                view_frame,
                columns=['list_view'],
                show='headings',
                selectmode='browse',
                height=10
            )
            self._table = table

            self.add_table_rows(table, list_data['data'], navigate_kwargs)
            self._add_scrollbar_to_table(view_frame, table)
            table.pack(side='left', fill='both', expand=True)

        return self
    
    def _add_scrollbar_to_table(self, frame, table):
        # include a scrollbar as spec'd
        scrollbar = Scrollbar(frame, orient='vertical', command=table.yview)
        scrollbar.pack(side='right', fill='y')
        table.config(yscrollcommand=scrollbar.set)

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

    def add_table_rows(self, table: Treeview, data: list, navigate_kwargs: dict):
        # rows should alternate, using tags alternate (I think lightgray and white are the example?)
        table.tag_configure('oddrow', background='#f2f1f1')
        table.tag_configure('evenrow', background='white')

        # save the selected row index
        table.tag_bind('oddrow', '<ButtonRelease-1>', lambda event: self.on_row_select(event, navigate_kwargs))
        table.tag_bind('evenrow', '<ButtonRelease-1>', lambda event: self.on_row_select(event, navigate_kwargs))

        for idx, row in enumerate(data):
            tags = ('evenrow',) if idx % 2 == 0 else ('oddrow',)
            if type(row) is not list:
                table.insert('', 'end', values=[row], tags=tags, iid=idx)
            else:
                table.insert('', 'end', values=row, tags=tags, iid=idx)

    def on_row_select(self, event, navigate_kwargs):
        navigate_kwargs["selected_row"] = self._table.focus()