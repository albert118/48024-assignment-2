from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


def load_asset(image_fn: str, new_width: int) -> PhotoImage:
    print(f'{__name__}: loading asset: {image_fn}')
    original_image = None
    try:
        original_image = Image.open(image_fn)
    except:
        print(f'{__name__}: failed to load asset "{image_fn}"')
        raise

    resized_image = None
    try:
        print(f'{__name__}: resizing asset to fit window...')
        # resize with a fixed aspect ratio
        original_width, original_height = original_image.size
        new_height = int((original_height / original_width) * new_width)
        resized_image = original_image.resize((new_width, new_height))
    except:
        print(f'{__name__}: failed to resize asset "{image_fn}"')
        raise

    return ImageTk.PhotoImage(resized_image)
