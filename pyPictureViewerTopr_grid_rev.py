import os

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

global img_x, img_y, kx, ky
global images, image, image_gui
global filelist, path


path        =   os.getcwd()
filelist    =   os.listdir(os.getcwd())
images      =   []

file_formats = [".png", ".jpg", ".tiff", ".gif"]

# get screen width and height for the tkinter root - commented out automatic screen detection, looks bad
#import ctypes
#user32 = ctypes.windll.user32
max_size_root_x = 1920 #user32.GetSystemMetrics(0)
max_size_root_y = 1080 #user32.GetSystemMetrics(1)

# base fixed resolution for the canvas
ores_x, ores_y = int(0.8*max_size_root_x), int(0.8*max_size_root_y)
scale_fac = ores_y / ores_x

# base scaled resolution for the tkinter canvas
size_canvas_x, size_canvas_y = int(round(0.5 * ores_x, 0)), int(round(0.5 * ores_y, 0))

# initial screen size x, y for the tkinter root
init_size_root_x, init_size_root_y = int(round(max_size_root_x * 0.5, 0)), int(round(max_size_root_y * 0.5, 0))

# base minimum size for the root
min_size_root_x = 1024
min_size_root_y = int(round(scale_fac * min_size_root_x * 1.33, 0))


def image_reader() -> ImageTk.PhotoImage:
    """Function returning the image to be stored and displayed via tKinter"""
    global image_gui, img_x, img_y, kx, ky, image, images, image_gui
    value = slider_selector.get()
    image_path = os.path.join(path, images[value])
    label_imageName.config(text = images[value])
    image = Image.open(image_path)

    img_x, img_y    = image.size[0], image.size[1]
    kx, ky          = panel.winfo_width(), panel.winfo_height()

    image.thumbnail((kx,ky),Image.ANTIALIAS)
    image_gui = ImageTk.PhotoImage(image)
    return image_gui

def image_shower(image_gui: ImageTk.PhotoImage) -> None:
    """Functions accepting the PhotoImage object to display it onto tKinter Root Canvas
    args
        - image_gui (ImageTk.PhotoImage): read image (from image_reader) 
    """
    panel.delete("all")
    panel.create_image(int(round(0.5*kx,0)),int(round(0.5*ky,0)),anchor=CENTER, image = image_gui)
    root.update()

def browser(button: Button, scaler: Scale, canvas: Canvas) -> None:
    """Invokes the system browsing window to select the desired directory and loads the pictures in it by updating global variables
    Accepts the tKinter objects as arguments
    args:
        - button (Button): tKinter button used to run this command (calls it back to switch its color)
        - scaler (Scale): tKinter scale which will get updated so the user can select the photos
        - canvas (Canvas): the displaying canvas of tKinter in Root"""
    global path, filelist, images
    path = filedialog.askdirectory()
    tmppath = []
    for file in os.listdir(path):
        for ob in file_formats:
            if ob in file:
                tmppath.append("png")

    if "png" in tmppath:
        canvas.config(bg="white")
        label_imageName.config(text = "Image name", bg= "lightblue")
    else:
        canvas.config(bg= "red")
        label_imageName.config(bg= "red", text= "No pictures in the folder") 

    filelist.clear()
    images.clear()

    filelist = os.listdir(path)
    for file in filelist:
        for ob in file_formats:
            if ob in file:
                images.append(file)
    images.sort(reverse=True)
    button.config(text= path)
    scaler.configure(to = len(images) - 1)
    scaler.set(0)

def filtering(entry: Entry, scaler: Scale, panel: Canvas) -> None:
    """Filters the selected pictures with a keyword, accepts tKinter objects
    args:
        - entry (Entry): the keyword inputted by the user 
        - scaler (Scale) the slider controlling displayed image
        - panel (Canvas): where the pictures are displayed"""

    global images, filelist, path
    images.clear()
    text        = entry.get()
    filelist    = os.listdir(path)
    entry.get()
    count = 0

    for file in filelist:
        if text in file: count += 1
        if text == "":
            for ob in file_formats:
                if ob in file:
                    images.append(file)  
            panel.config(bg = "white")        
            label_imageName.config(text = "Image name", bg= "lightblue")  

        else:
            if text in file:
                for ob in file_formats:
                    if ob in file:
                        entry.delete(0, "end")
                        entry.insert(0, text)
                        images.append(file)
                        panel.config(bg = "white")
                        label_imageName.config(text = "Image name", bg= "lightblue")
                        
            elif text not in file and count == 0:
                entry.delete(0, "end")
                entry.insert(0,"INVALID")
                panel.config(bg = "red")
                label_imageName.config(bg= "red", text= "No pictures in the folder") 
    
    if len(images) == 0: scaler.configure(to = 0)
    else: scaler.configure(to = len(images) - 1)
    scaler.set(0)

def gif_export(entry_fps: int = 20) -> None:
    """Converts the pictures in the folder (or filtered pictures) to a gif in an alphabetical order
    args:
        entry_fps (int): framerate of the gif
    """
    global images, path
    timer = 1/(entry_fps/1_000)
    imglist_tmp = []

    gif_path = filedialog.asksaveasfilename(
        filetypes= [("gif animation", "*.gif")], initialdir = path) \
                 + [("gif animation", "*.gif")][0][1][1:]

    for img in images:
        img_path = os.path.join(path, img)
        print("\t", img_path)
        imglist_tmp.append(Image.open(img_path))

    imglist_tmp[0].save(
        gif_path,
        save_all=True,
        quality=100,
        optimize=True,
        progressive=True,
        append_images=imglist_tmp[:],
        duration=timer,
        loop=0)
    print("gif_export: done")

# main panel and boundary definition
root = Tk()
root.title("PyImageViewer ToPr")
root.geometry(f"{init_size_root_x}x{init_size_root_y}")

root.minsize(min_size_root_x,
             min_size_root_y
             )

root.maxsize(max_size_root_x, max_size_root_y)


# label
textpanel = Label(text= "Picture Viewer - Tomáš Prejda")

panel = Canvas(root,
               width = size_canvas_x,
               height= size_canvas_y,
               bg = "white"
               )

# label - name of the loaded picture
label_imageName = Label(text = "Image name", bg= "lightblue")

# position selector of the images
slider_selector = Scale(root,
                   from_= 0,
                   to = len(images) - 1,
                   orient = HORIZONTAL,
                   length = size_canvas_x
                   )

# assigning image selector command to the slider
# the lambda value thing is a trick (so I can pass multiple commands - without it the list won't get accepted)
slider_selector.config(command = lambda value: [image_shower(image_reader())])

# assigning key-press events 
root.bind("<Right>",            lambda value: [slider_selector.set(slider_selector.get() + 1), image_shower(image_reader())])
root.bind("<Left>",             lambda value: [slider_selector.set(slider_selector.get() - 1), image_shower(image_reader())])
root.bind("<Control-Right>",    lambda value: [slider_selector.set(slider_selector.get() + 10), image_shower(image_reader())])
root.bind("<Control-Left>",     lambda value: [slider_selector.set(slider_selector.get() - 10), image_shower(image_reader())])


# button for folder selection
button_folder_selection = Button(root,
                                 text = "Browse Folder",
                                 command = lambda: browser(button_folder_selection, slider_selector,panel)
                                 )

# row with filtering gui objects
label_filter = Label(root,
                     text="Filtering Word"
                     )

entry_filter = Entry(root)
entry_filter.insert(0, "Filter")
button_filter_apply = Button(root,
                             text = "Apply Filter",
                             command = lambda: filtering(entry_filter, slider_selector, panel)
                             )

# row with gif creation gui objects
label_gif   = Label(root, text = "Frame speed [fps]")

entry_Gif = Entry(root)
entry_Gif.insert(0, "40")
button_gif_apply = Button(root,
                          text = "Export Gif",
                          command = lambda: gif_export(int(entry_Gif.get()))
                          )


# gui layout configuration
Grid.rowconfigure(root, index = 0, weight = 1)
Grid.rowconfigure(root, index = 1, weight = 10)
Grid.rowconfigure(root, index = 2, weight = 1)
Grid.rowconfigure(root, index = 3, weight = 1)
Grid.rowconfigure(root, index = 4, weight = 1)
Grid.rowconfigure(root, index = 5, weight = 1)
Grid.rowconfigure(root, index = 6, weight = 1)
Grid.columnconfigure(root, index = 0, weight = 1)
Grid.columnconfigure(root, index = 1, weight = 2)
Grid.columnconfigure(root, index = 2, weight = 1)
Grid.columnconfigure(root, index = 3, weight = 2)
Grid.columnconfigure(root, index = 4, weight = 1)


# gui layout assignment
textpanel.grid                  (row = 0, column = 0, columnspan = 5, sticky = NSEW)
panel.grid                      (row = 1, column = 0, columnspan = 5, sticky = NSEW)
slider_selector.grid                 (row = 2, column = 0, columnspan = 5, sticky = NSEW)
label_imageName.grid            (row = 3, column = 0, columnspan = 5, sticky = NSEW)
button_folder_selection.grid    (row = 4, column = 0, columnspan = 5, sticky = NSEW)
label_filter.grid               (row = 5, column = 0, columnspan = 1, sticky = NSEW)
entry_filter.grid               (row = 5, column = 1, columnspan = 2, sticky = NSEW)
button_filter_apply.grid        (row = 5, column = 3, columnspan = 2, sticky = NSEW)
label_gif.grid                  (row = 6, column = 0, columnspan = 1, sticky = NSEW)
entry_Gif.grid                  (row = 6, column = 1, columnspan = 3, sticky = NSEW)
button_gif_apply.grid           (row = 6, column = 3, columnspan = 2, sticky = NSEW)

# execute gui
root.mainloop()