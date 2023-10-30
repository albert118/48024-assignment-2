# Hello world!

Welcome to my solution to assignment #2.

## Notes

- not very pythonic or friendly to throw exceptions, but the
  skeleton recommended they be throw (aka. raised in Python)
- data classes / records define a to_string method, Python has `__str__` for this purpose
- several instance methods missing `self`
- list init often done iteratively with for-loop (could use list init's)
- some specs only available in the fxml source (this is annoying and easy to miss, as it's not a clear Python requirement)
  - window sizes
  - expected styling
- tkinter not handling the provided assets adds further unspecced work to hack a workaround
- ~no default/expected login creds for this assignment??~ these are buried in the admins file

## TODO

- [ ] submit this repo as a `zip` to Canvas
- [ ] submit source code to Ed
- [ ] submit the assignment cover sheet

[info on themes](https://github.com/coapp-packages/tk/blob/master/library/ttk/clamTheme.tcl#L93), might help figuring out why focus styling isn't working

[on using PIL with TK](https://www.activestate.com/resources/quick-reads/how-to-add-images-in-tkinter/)
