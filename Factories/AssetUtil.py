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

def load_icon(icon_fn: str) -> PhotoImage:
    # png_path = "login_icon.png"
    # gif_path = "login_icon.gif"

    # try:
    #     png_image = Image.open(png_path)
    #     # resize the image to 32x32 (standard icon size)
    #     png_image = png_image.resize((32, 32))
    #     png_image.save(gif_path, format="GIF")
    # except Exception as e:
    #     print("Error converting icon:", str(e))

    # icon = PhotoImage(file=gif_path)
    # self.win.call('wm', 'iconphoto', self.win._w, icon)
    
    print(f'loading asset: {icon_fn}')
    return PhotoImage(file=icon_fn)
