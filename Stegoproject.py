import cv2
import os
import tkinter as tk
from tkinter import filedialog

encrypted_image_path = None  # Variable to store the path of the encrypted image
password = None  # Variable to store the password
msg = None  # Variable to store the secret message


def encrypt_image():
    global encrypted_image_path, password, msg  # Use global variables

    # User enters secret message
    msg = entry_message.get()
    # User enters password
    password = entry_password.get()

    # Popup for user to select the image that needs to be encrypted
    img_path = filedialog.askopenfilename(title="Select Image to Encrypt", filetypes=[
                                          ("Image files", "*.jpg;*.png;*.jpeg")])  # Allow any image format
    img = cv2.imread(img_path)

    # Check if the image is not in PNG format
    if not img_path.lower().endswith(".png"):
        convert_to_png = tk.messagebox.askyesno(
            "Image Format", "The selected image is not in PNG format. It will be converted to PNG. Do you want to proceed?")

        if convert_to_png:
            # Convert the image to PNG format
            png_image_path = img_path.rsplit(".", 1)[0] + ".png"
            cv2.imwrite(png_image_path, img)

            # Inform the user that the conversion was successful
            tk.messagebox.showinfo("Conversion Complete",
                                   "Conversion successful to PNG.")

            # Ask the user for a location to save the PNG image
            save_directory = filedialog.askdirectory(
                title="Select Path to Save Converted Image")

            # Ask the user for a name for the converted PNG image
            image_name = tk.simpledialog.askstring(
                "Input", "Set name for image convetred to PNG:")

            # Add ".png" extension if not provided by the user
            if not image_name.lower().endswith(".png"):
                image_name += ".png"

            # Save the converted image
            new_png_image_path = os.path.join(save_directory, image_name)
            os.rename(png_image_path, new_png_image_path)

            # Inform the user that the save was successful
            tk.messagebox.showinfo(
                "Save as PNG Complete", "Image saved and will be used for encryption.")

            # Use the PNG image for encryption
            img_path = new_png_image_path

    m = 0
    n = 0
    z = 0

    for i in range(len(msg)):
        # Subtract 32 to bring the ASCII value within the range of pixel values
        img[n, m, z] = ord(msg[i]) - 32
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    # Ask the user for a location to save the encrypted image
    save_directory = filedialog.askdirectory(
        title="Select Location to Save Encrypted Image")

    # Ask the user for a name for the encrypted image
    image_name = tk.simpledialog.askstring(
        "Input", "Save encrypted image as :")

    # Add ".png" extension if not provided by the user
    if not image_name.lower().endswith(".png"):
        image_name += ".png"

    encrypted_image_path = os.path.join(
        save_directory, image_name)  # Store the path

    cv2.imwrite(encrypted_image_path, img)

    # Inform the user that the encryption was successful
    tk.messagebox.showinfo("Encryption Complete", "Encryption successful.")

    # Ask the user if they want to open the encrypted image
    open_image = tk.messagebox.askyesno(
        "Open Image", "Do you want to open the encrypted image?")
    if open_image:
        os.system('start "" "' + encrypted_image_path + '"')

    # Clear the entry fields
    entry_message.delete(0, tk.END)
    entry_password.delete(0, tk.END)

    # Inform the user to proceed
    tk.messagebox.showinfo(
        "Proceed", "Enter passcode to decrypt image that was encoded earlier.")


def decrypt_image():
    global encrypted_image_path, password, msg  # Use global variables

    if encrypted_image_path is None:
        tk.messagebox.showerror("No Encrypted Image",
                                "No image has been encrypted yet.")
        return

    message = ""

    n = 0
    m = 0
    z = 0

    pas = entry_decryption_password.get()

    if password == pas:
        img = cv2.imread(encrypted_image_path)

        # Make a copy of the encrypted image to avoid modifying the original
        decrypted_img = img.copy()

        for i in range(len(msg)):
            # Add 32 to convert the pixel value back to the correct ASCII value
            message = message + chr(decrypted_img[n, m, z] + 32)
            n = n + 1
            m = m + 1
            z = (z + 1) % 3

        tk.messagebox.showinfo("Decryption Successful",
                               f"Decryption message: {message}")

        # Clear the decryption entry field
        entry_decryption_password.delete(0, tk.END)

    else:
        tk.messagebox.showerror("Invalid Key", "Not a valid key.")


# GUI setup
root = tk.Tk()
root.title("Image Encryption and Decryption")

# Encryption Frame
frame_encrypt = tk.Frame(root)
frame_encrypt.pack(padx=10, pady=10)

label_message = tk.Label(frame_encrypt, text="Enter secret message:")
label_message.grid(row=0, column=0, padx=5, pady=5)

entry_message = tk.Entry(frame_encrypt)
entry_message.grid(row=0, column=1, padx=5, pady=5)

label_password = tk.Label(frame_encrypt, text="Enter password:")
label_password.grid(row=1, column=0, padx=5, pady=5)

entry_password = tk.Entry(frame_encrypt, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

button_encrypt = tk.Button(
    frame_encrypt, text="Encrypt Image", command=encrypt_image)
button_encrypt.grid(row=3, columnspan=2, pady=10)

# Decryption Frame
frame_decrypt = tk.Frame(root)
frame_decrypt.pack(padx=10, pady=10)

label_decryption_password = tk.Label(
    frame_decrypt, text="Enter passcode for Decryption:")
label_decryption_password.grid(row=0, column=0, padx=5, pady=5)

entry_decryption_password = tk.Entry(frame_decrypt, show="*")
entry_decryption_password.grid(row=0, column=1, padx=5, pady=5)

button_decrypt = tk.Button(
    frame_decrypt, text="Decrypt Image", command=decrypt_image)
button_decrypt.grid(row=1, columnspan=2, pady=10)

root.mainloop()
