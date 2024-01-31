import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import random
import tksvg

current_svg_path = None  # Variable to store the current SVG file path

def change_color(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Change the fill or stroke attribute to a new random color
    for element in root.iter():
        if 'fill' in element.attrib:
            element.attrib['fill'] = get_random_color()
        elif 'stroke' in element.attrib:
            element.attrib['stroke'] = get_random_color()

    output_file = svg_file.replace('.svg', '_modified.svg')
    tree.write(output_file)
    print(f"Color changed successfully. Modified SVG saved to {output_file}")

    return output_file

def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def clean_svg_namespace(svg_file):
    with open(svg_file, 'r') as f:
        content = f.read()

    # Remove or replace namespaces (ns0:) from the SVG content
    content = content.replace('ns0:', '')
    content = content.replace(':ns0', '')
    
    with open(svg_file, 'w') as f:
        f.write(content)

def browse_file():
    global current_svg_path
    current_svg_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if current_svg_path:
        modified_file_path = change_color(current_svg_path)
        clean_svg_namespace(modified_file_path)
        display_modified_svg(modified_file_path)

def display_modified_svg(modified_file_path):
    svg_image = tksvg.SvgImage(file=modified_file_path, scale=0.4)
    label.config(image=svg_image)  # Update the image property of the label
    label.image = svg_image  # Store a reference to prevent the image from being garbage collected

def change_color_and_display():
    global current_svg_path
    if current_svg_path:
        modified_file_path = change_color(current_svg_path)
        clean_svg_namespace(modified_file_path)
        display_modified_svg(modified_file_path)

# Create the main Tkinter window
root = tk.Tk()

# Set the Tkinter window size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

root.title("SVG Color Changer")

# Create a frame to contain the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create a button to browse and change the color of the selected SVG file
browse_button = tk.Button(button_frame, text="Browse SVG", command=browse_file)
browse_button.pack(side='left', padx=5)

# Create a button to change color and display the modified SVG file
change_color_button = tk.Button(button_frame, text="Change Color", command=change_color_and_display)
change_color_button.pack(side='left', padx=5)

# Create a label to display the modified SVG image
label = tk.Label(root)
label.pack()

# Start the Tkinter event loop
root.mainloop()
