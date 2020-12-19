import fitz
from PIL import Image, ImageEnhance
import os
import webbrowser
from tkinter import filedialog
import tkinter as tk
if __name__ == '__main__':
    # pick pdf files
    root = tk.Tk()
    root.title("SeePDF")
    root.filenames = filedialog.askopenfilenames(filetypes = [("PDF Files", "*.pdf")])
    # get files directory
    first_file = root.filenames[0]
    parts = first_file.split("/")
    name = parts[-1]
    path = first_file.replace("/"+name, "")
    os.chdir(path)
    # extract images from pdf files
    for i in range(len(root.filenames)):
        doc = fitz.open(root.filenames[i])
        xref = doc.getPageImageList(0)[0][0]
        pix = fitz.Pixmap(doc, xref)
        pix.writePNG("seepdf{}.png".format(i))
    # enhance each image's contrast
    for i in range(len(root.filenames)):
        im = Image.open("seepdf{}.png".format(i))
        bwEnhancer = ImageEnhance.Color(im)
        color_output = bwEnhancer.enhance(0.0)
        contrastEnhancer = ImageEnhance.Contrast(color_output)
        contrastFactor = 2.6
        contrast_output = contrastEnhancer.enhance(contrastFactor)
        brightnessEnhancer = ImageEnhance.Brightness(contrast_output)
        brightnessFactor = 0.9;
        brightness_output = brightnessEnhancer.enhance(brightnessFactor)
        brightness_output.save("seepdf{}.png".format(i))
    # create new pdf from images
    images = list()
    for i in range(len(root.filenames)):
        im = Image.open("seepdf{}.png".format(i))
        images.append(im)
    pdf_filename = "output.pdf"
    first_img = images.pop(0)
    first_img.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=images)
    # clean up
    for i in range(len(root.filenames)):
        os.remove("seepdf{}.png".format(i))
    webbrowser.open("file://" + path + "/output.pdf")
