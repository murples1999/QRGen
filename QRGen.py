import qrcode
import os
import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def main():
    url, arg = get_arguments()
    if arg == "gui":
        open_gui()
    elif arg == "generate":
        qr = generate_qr_code(url)
        save_locally(qr)


def get_arguments() -> tuple:
    # -g to specify url in terminal command
    # no argument to use GUI

    if len(sys.argv) < 2:
        return "", "gui"

    elif len(sys.argv) == 3 and sys.argv[1] == "-g":
        return sys.argv[2], "generate"

    else:
        sys.exit("Incorrect Usage")


def open_gui():

    root = tk.Tk()
    root.geometry("300x200")
    root.title("QRGen")

    url_var = tk.StringVar()

    url_entry_label = tk.Label(
        root, 
        text="Type URL Here",
    )
    url_entry_label.pack(padx=10, pady=5)

    url_entry_box = tk.Entry(
        root,
        width=250,
        textvariable=url_var
    )
    url_entry_box.pack(padx=10, pady=5)

    generate_qr_button = tk.Button(
        root,
        text="Generate QR Code",
        command=lambda: update_qr_display(url_var, qr_display, save_qr_button, root)
    )
    generate_qr_button.pack(padx=10, pady=10)

    qr_display = tk.Label(root, image="", state=tk.DISABLED)
    qr_display.pack(padx=10, pady=5)

    save_qr_button = tk.Button(
        root,
        text="Save",
        command=lambda: save_to_location(url_var),
        state=tk.DISABLED
    )
    save_qr_button.pack(padx=10, pady=5)

    root.mainloop()


def save_to_location(url_var):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )

    if file_path:
        qr = generate_qr_code(url_var.get())
        qr.save(file_path)


def update_qr_display(url_var, qr_display, save_qr_button, root):
    if url_var.get() != "":
        pil_image = generate_qr_code(url_var.get())
        tk_image = ImageTk.PhotoImage(pil_image)
        qr_display.config(image=tk_image)
        qr_display.image = tk_image
        qr_display.config(state=tk.NORMAL)
        save_qr_button.config(state=tk.NORMAL)

        image_width, image_height = pil_image.size
        padding = 10
        new_width = image_width + padding
        new_height = image_height + padding + 170
        root.geometry(f"{new_width}x{new_height}")


def generate_qr_code(url) -> qrcode:
    img = qrcode.make(url)
    return img


def save_locally(qr: qrcode):
    qr.save("test.png")


if __name__ == "__main__":
    main()