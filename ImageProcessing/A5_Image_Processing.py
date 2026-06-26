#!/usr/bin/env python3
"""
File: A5_Image_Processing

Author: Christian Bailey
Co-Author: Thomas Frank
Date: 2026-02-17
Course: CS1400, University of Utah, Kahlert School of Computing
Copyright: CS1400, Christian Bailey and Thomas Frank - This work may not be copied for use in Academic Coursework.
We, Christian Bailey and Thomas Frank, certify that we wrote this code from scratch and did not copy it in part
or whole from another source.

File contents/Program Purpose
This program applies different filters to images.

"""
import math
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw


def main() -> None:
    """
    Build the image manipulation GUI.
    :return: None - Infinite Event Loop
    """
    try:
        build_an_run_image_manimpulation_GUI("images/university_of_utah.png")
    except:
        root = tk.Tk()
        root.withdraw()  # hide the main window

        messagebox.showinfo("Hello", "Error Trying To Load Image File. Is it in the right spot and named correctly?")


# ------------------------------------------------------------
# The following functions for you to implement
# ------------------------------------------------------------

def rotate_colors(image):
    """

    TODO: remove this comment --> This code is provided for you as an example

    Move each color "one to the right", in other words R -> G -> B -> R
    Red goes into Green's value, Green goes into Blues, and Blue goes into Reds
    :param image: the starting point
    :return: the new image
    """
    image = image.copy()
    width, height = image.size

    pixels = image.load()

    for row in range(height):
        for col in range(width):
            (red,green,blue) = pixels[col, row]
            pixels[col, row] = (blue, red, green)

    return image

def brighten_image(image, amount):
    """
        this function takes the image, and uses an accumulation loop to change the rgb values while using
        if statements to ensure we do not go above or below our desired 0-255 values.
    :param image: the starting point
    :param amount: the amount that the slider adjusts
    :return: the new image
    """
    image=image.copy()
    width,height=image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            red,green,blue = pixels[x,y]

            red = red + amount
            green = green + amount
            blue = blue + amount

            if red > 255: red = 255
            if green > 255: green = 255
            if blue > 255: blue = 255

            if red < 0: red = 0
            if green < 0: green = 0
            if blue < 0: blue = 0

            pixels[x,y]=(red,green,blue)


    return image

def convert_to_grayscale(image):
    """
    this function takes the image, divides the rgb value by 3 to make the whole image darker,
    and then converts the rgb into gray with the same brightness values.
    :param image: the starting point
    :return: the new image
    """
    image=image.copy()
    width,height=image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            red,green,blue = pixels[x,y]
            gray = int((red + green + blue) / 3)
            pixels[x,y]=(gray, gray, gray)
    return image

def threshold_image(image, threshold):
    """
        this function takes the image, and uses a for loop to change the rgb of each x,y to either a max
        of 255 or 0 depending on the average of its starting value.
    :param image: the starting image
    :param threshold: the amount that the slider adjusts
    :return: the new image
    """
    image=image.copy()
    width,height=image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            red, green, blue = pixels[x, y]
            average = (red + green + blue)//3
            if average > threshold:
                pixels[x,y] = (255, 255, 255)
            else:
                pixels[x,y] = (0,0,0)
    return image

def horizontal_flip(image):
    """
    our function defines the left side of the image, and places it on the right half of the screen while also
    replacing the left side with its opposite right side value.
    Param: image: the starting point
    return: returns the new image.
    """
    image = image.copy()
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width // 2):
            left = pixels[x, y]
            right = pixels[(width - 1 - x), y]

            pixels[x, y] = right
            pixels[(width - 1 - x), y] = left
    # Implement this function
    return image

def vertical_flip(image):
    """
    our function defines the top side of the image, and places it on the bottom half of the screen while also
    replacing the top side with its opposite bottom side value.
    Param: image: the starting point
    return: returns the new image.
    """
    image = image.copy()
    width, height = image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height // 2):
            bottom = pixels[x, y]
            top = pixels[x, (height - 1 - y)]

            pixels[x, y] = top
            pixels[x, (height - 1 - y)] = bottom
    return image

def photonegative(image):
    """
    this function takes the RGB values and subtracts them from 255, thus creating a negative image
    param: image: the starting point
    return: the new image
    """
    image = image.copy()
    width, height = image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            red, green, blue = pixels[x, y]

            new_red = 255 - red
            new_green = 255 - green
            new_blue = 255 - blue

            pixels[x, y] = (new_red, new_green, new_blue)
    return image

def merge_green_screen_with_image(green_image, background_image):
    """
    this function uses a forloop to go through the green_image and any pixel that is not
    green gets transfered to the background image.
    param: green_image: green screen image
    param: background_image: background image
    return: returns the background image with new pixels copied from green image
    """
    image = background_image.copy()

    green_pix = green_image.load()
    background = image.load()

    width, height = green_image.size


    for x in range(width):
        for y in range(height):
            red, green, blue = green_pix[x,y]
            if not (red < 100 and green >= 150 and blue < 100):
                background[x, y] = (red, green, blue)
    return image

def dotify_image(image, radius, count):
    """
    Place 'count' filled circles of radius 'radius' at random locations.
    Each circle's color is sampled from the original (unmodified) image.
    Returns a new dotified image.
    """
    source = image.copy()          # never draw on this
    result = image.copy()          # draw on this

    width, height = source.size
    source_pixels = source.load()

    draw = ImageDraw.Draw(result)

    for _ in range(count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        color = source_pixels[x, y]   # sample from original

        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),fill=color)

    return result
def decode_secret_message(image):
    """
    this function decodes a secret message in an image by going through each pixel location and determining if the
    values are even or odd. if even, it sets the value to 0. if the value is odd it returns 255.
    param: image: the base image
    return: returns the secret message
    """
    image = image.copy()
    width, height = image.size
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            red, green, blue = pixels[x, y]
            red = 255 if red % 2 == 1 else 0
            green = 255 if green % 2 == 1 else 0
            blue = 255 if blue % 2 == 1 else 0

            pixels[x,y] = (red, green, blue)
    return image

# ------------------------------------------------------------
# GUI FUNCTIONS
#
# Greetings students, If you are reading this, congratulations!
# You are showing curiosity and initiative.
#
# The functions below are all used to build the GUI that allows
# the program to be more user-friendly.
#
# You do NOT need to understand nor modify this code.  That being
# said, if you are interested, you should have _some_ of the tools
# necessary to understand what is going on, and a "guess" of
# what the code does.  While there won't be test questions on this
# part of the code, if you ever want to make your own interactive
# GUI program, you will likely use something along the following lines.
#
# Again, I congratulate you on showing initiative and I hope
# that solving problems with code gives you the same pleasure
# that it gives me.
# ------------------------------------------------------------

def put_image_on_screen(canvas, image):
    """Replace the image currently shown on the canvas."""
    canvas.img = image.convert("RGB")
    canvas.photo = ImageTk.PhotoImage(canvas.img)
    canvas.itemconfig("main_image", image=canvas.photo)
    canvas.image = canvas.photo  # keep reference

def on_mouse_move(event, canvas):
    """
    When the mouse moves across the image, this function is called.
    Here we "look up" the value of the pixel under the mouse and show
    it as text at the bottom of the screen.
    :param event:
    :param canvas:
    :return:
    """
    col, row = event.x, event.y
    img = canvas.img

    if 0 <= col < img.width and 0 <= row < img.height:
        pixel = img.getpixel((col, row))
        canvas.info_label.config(
            text=f"col={col:4d}, row={row:4d}  pixel={pixel}\nwidth = {img.width:4d}, height = {img.height:4d}"
        )
    else:
        canvas.info_label.config(text="")

def file_menu_load_image(canvas):
    """
    Bring up a file menu and allow the user to select an image to manipulate.
    Make sure we save this image as the new original.
    :param canvas: the GUI drawing pane
    :return: None
    """
    filename = filedialog.askopenfilename(
        title="Open Image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )

    if not filename:  # user cancelled out
        return

    try:
        img = Image.open(filename)
        img.verify()  # validate file without decoding fully
        img = Image.open(filename).convert("RGB")  # reopen after verify
    except OSError:
        messagebox.showerror(
            "Invalid Image",
            f"The selected file is not a valid image:\n\n"
        )
        return

    canvas.original_img = img.copy()
    canvas.config(width=img.width, height=img.height)
    put_image_on_screen(canvas, img)

def slider_changed(canvas, value, label):
    """
    Handle the event that takes place when the user moves the slider for the
    Threshold method.
    :param canvas: the GUI container and data repository
    :param value: an integer between 0 and 255
    :param label: should be Brightness or Threshold
    :return:
    """
    print("slider changed")
    canvas.slider.config(label=f"{label}: {value}")
    if label.startswith("Brightness"):
        put_image_on_screen( canvas, brighten_image(canvas.original_img, int(value) ) )
    else:
        put_image_on_screen( canvas, threshold_image(canvas.original_img, int(value) ) )

def toggle_slider(canvas, name):
    """
    Show or hide the slider for use with various functionality, like
    thresholding or brightening.
    :param canvas: holds the image and widgets
    :param name: should be either Threshold or Brightness
    :return: Nothing
    """
    if canvas.slider_visible:
        if canvas.slider.cget("label").startswith(name):
            canvas.slider.pack_forget()
            canvas.slider_visible = False
        else:
            canvas.slider.config(command=lambda value: slider_changed( canvas, int( value ), name ) )
    else:
        canvas.slider.pack(pady=10)
        canvas.slider_visible = True
        canvas.slider.config(command=lambda value: slider_changed( canvas, int( value ), name ) )

    if name.startswith("Brightness"):
        put_image_on_screen( canvas, brighten_image(canvas.original_img, 100 ) )
        canvas.slider.config(from_=-255,to_=255)
        canvas.slider.set(0)
    else:
        put_image_on_screen( canvas, threshold_image(canvas.original_img, 100 ) )
        canvas.slider.config(from_=0,to_=255)
        canvas.slider.set(100)

def get_dotify_info(canvas):

    root = canvas.winfo_toplevel()

    # Get root position and size
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    dialog = tk.Toplevel(root)
    dialog.title("Dotify Information")
    dialog.resizable(False, False)

    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    x = root_x + (root_width // 2) - (dialog_width // 2)
    y = root_y + (root_height // 2) - (dialog_height // 2)

    dialog.transient(root)
    dialog.grab_set()
    dialog.geometry(f"+{x}+{y}")

    result = {"values": None}

    tk.Label(dialog, text="Circle Size:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(dialog, text="Number of Circles:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    circle_entry = tk.Entry(dialog)
    count_entry = tk.Entry(dialog)

    circle_entry.grid(row=0, column=1, padx=10, pady=5)
    count_entry.grid(row=1, column=1, padx=10, pady=5)

    circle_entry.insert(0, canvas.dot_radius)
    count_entry.insert(0, canvas.dot_count)

    def on_ok():
        try:
            circle_Radius = int(circle_entry.get())
            num_circles = int(count_entry.get())

            canvas.dot_radius=circle_Radius
            canvas.dot_count=num_circles

            result["values"] = (circle_Radius, num_circles)
            put_image_on_screen( canvas, dotify_image(canvas.img, circle_Radius, num_circles) )
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")

    dialog.bind("<Return>", lambda event: on_ok())

    tk.Button(dialog, text="OK", width=10, command=on_ok).grid(row=2, column=0, pady=10)
    tk.Button(dialog, text="Cancel", width=10, command=dialog.destroy).grid(row=2, column=1, pady=10)

    circle_entry.focus()

    root.wait_window(dialog)

    return result["values"]

def generate_dotify_image(canvas):
    """
    Bring up a modal asking for information about the dotify, and then
    generate and display the new image.

    :param canvas: the GUI drawing pane
    :return: None
    """
    get_dotify_info( canvas )

    return canvas.img



def load_green_screen(canvas):
    """
    Bring up a file menu and allow the user to select a green screen
    image to apply to the current image.  Make sure the image is the proper size.

    :param canvas: the GUI drawing pane
    :return: None
    """
    filename = filedialog.askopenfilename(
        title="Select Green Screen Image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
            ("All files", "*.*")
        ]
    )

    if not filename:  # user cancelled out
        return

    try:
        green_image = Image.open(filename)
        green_image.verify()  # validate file without decoding fully
        green_image = Image.open(filename).convert("RGB")  # reopen after verify
        if green_image.size != canvas.img.size:
            messagebox.showerror(
                "Invalid Image",
                f"The image must be the same size as the current image\n\n"
            )
        put_image_on_screen( canvas, merge_green_screen_with_image(green_image,canvas.img) )
    except OSError:
        messagebox.showerror(
            "Invalid Image",
            f"The selected file is not a valid image:\n\n"
        )
        return


def build_an_run_image_manimpulation_GUI(image_filename):
    """
    This function builds the GUI that shows the image and allows the
    user to choose manipulation filters/options.
    :param image_filename: the default image to show
    :return: the TK root, so the program can go into an infinite event loop
    """
    root = tk.Tk()
    root.minsize(500, 500)
    root.title(image_filename)

    # Load a te given image and remove alpa channel (if there)
    img = Image.open(image_filename).convert("RGB")

    # Build the GUI
    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()

    # Add a text box at the bottom
    info = tk.Label(root, text="", font=("Consolas", 12),justify="left")
    info.pack(anchor="w")

    # For use with dotify function
    canvas.dot_radius = 10
    canvas.dot_count = 1000

    # Store shared state on canvas
    canvas.img = img
    canvas.original_img = img.copy()
    canvas.info_label = info

    canvas.photo = ImageTk.PhotoImage(img)
    canvas.create_image(
        0, 0,
        anchor="nw",
        image=canvas.photo,
        tags="main_image"
    )

    ####################################################################
    # Add mouse tracking
    canvas.bind("<Motion>", lambda event: on_mouse_move(event, canvas))

    ####################################################################
    # Add the threshold slider
    slider = tk.Scale(
        root,
        from_=0,
        to=255,
        orient=tk.HORIZONTAL,
        length=300,
        label="Threshold"
    )
    slider.set(100)

    canvas.slider_visible = False
    canvas.slider = slider

    ####################################################################
    # Build the Menu Bars
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(
        label="Load",
        accelerator="Ctrl+O",
        command=lambda: file_menu_load_image(canvas)
    )
    file_menu.add_command(
        label="Quit Program",
        accelerator="Ctrl+Q",
        command=lambda: root.destroy()
    )

    filters = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade( label="Filters", menu=filters)
    filters.add_command( label="Reset",            accelerator="Ctrl-Return", command=lambda: put_image_on_screen( canvas, canvas.original_img ) )
    filters.add_separator()
    filters.add_command( label="Horizontal Flip",  accelerator="Ctrl-H", command=lambda: put_image_on_screen( canvas, horizontal_flip(canvas.img) ) )
    filters.add_command( label="Vertical Flip",    accelerator="Ctrl-V", command=lambda: put_image_on_screen( canvas, vertical_flip(canvas.img) ) )
    filters.add_separator()
    filters.add_command( label="Brighten",         accelerator="Ctrl-B", command=lambda: toggle_slider( canvas, "Brightness" ) )
    filters.add_command( label="Negative",         accelerator="Ctrl-N", command=lambda: put_image_on_screen( canvas, photonegative(canvas.img) ) )
    filters.add_command( label="Grayscale",        accelerator="Ctrl-G", command=lambda: put_image_on_screen( canvas, convert_to_grayscale(canvas.img) ) )
    filters.add_command( label="Threshold",        accelerator="Ctrl-T", command=lambda: toggle_slider( canvas, "Threshold") )
    filters.add_command( label="Rotate Colors",    accelerator="Ctrl-R", command=lambda: put_image_on_screen( canvas, rotate_colors(canvas.img) ) )
    filters.add_separator()
    filters.add_command( label="Decode Secret",    accelerator="Ctrl-?", command=lambda: put_image_on_screen( canvas, decode_secret_message(canvas.img) ) )
    filters.add_command( label="Dotify Image",     accelerator="Ctrl-D", command=lambda: generate_dotify_image(canvas)  )
    filters.add_command( label="Green Screen",     accelerator="Ctrl-M", command=lambda: put_image_on_screen( canvas, load_green_screen(canvas) ) )

    # Make some keyboard shortcuts for faster demo
    root.bind( "<Control-o>", lambda event: file_menu_load_image(canvas) )
    root.bind( "<Control-Return>", lambda event: put_image_on_screen( canvas, canvas.original_img ) )
    root.bind( "<Control-h>", lambda event: put_image_on_screen( canvas, horizontal_flip(canvas.img) ) )
    root.bind( "<Control-v>", lambda event: put_image_on_screen( canvas, vertical_flip(canvas.img) ) )
    root.bind( "<Control-g>", lambda event: put_image_on_screen( canvas, convert_to_grayscale(canvas.img) ) )
    root.bind( "<Control-n>", lambda event: put_image_on_screen( canvas, photonegative(canvas.img) ) )
    root.bind( "<Control-b>", lambda event: toggle_slider(canvas, "Brightness"))
    root.bind( "<Control-t>", lambda event: toggle_slider(canvas, "Threshold"))
    root.bind( "<Control-d>", lambda event: put_image_on_screen(canvas, generate_dotify_image(canvas) ) )
    root.bind( "<Control-?>", lambda event: put_image_on_screen(canvas, decode_secret_message(canvas.img)))
    root.bind( "<Control-r>", lambda event: put_image_on_screen(canvas, rotate_colors(canvas.img)))
    root.bind( "<Control-m>", lambda event: load_green_screen( canvas ) )

    root.bind_all("<Control-q>", lambda event: root.destroy())

    root.mainloop()


if __name__ == "__main__":
    main()
