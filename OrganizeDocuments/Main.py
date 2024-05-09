import os
import shutil
import tkinter as tk
from tkinter import filedialog
import sys
import subprocess

source_directory = 'C:/Documentos Para Organizar Miptec'
destination_directory = 'C:/Documentos Organizados Miptec/'

def select_folder():
    global source_directory

    folder_path = filedialog.askdirectory()
    if folder_path:
        source_directory = folder_path
        root.destroy()
    else:
        label.config(text="Nenhuma pasta selecionada.")


root = tk.Tk()
root.title("Selecione a pasta que contem os documentos")
label = tk.Label(root, text="Nenhuma pasta selecionada.")
label.pack(pady=10)
select_button = tk.Button(root, text="Seleciona a pasta", command=select_folder)
select_button.pack(pady=130)

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window position
root.geometry(f"+{x_position}+{y_position}")

root.mainloop()

if(os.path.isdir(source_directory) is False):
    sys.exit()

def select_destination_folder():
    global destination_directory

    folder_path = filedialog.askdirectory()
    if folder_path:
        destination_directory = folder_path
        root.destroy()
    else:
        label.config(text="Nenhuma pasta selecionada.")

root = tk.Tk()
root.title("Selecione a pasta para onde irão os documentos")
label = tk.Label(root, text="Nenhuma pasta selecionada.")
label.pack(pady=10)
select_button = tk.Button(root, text="Seleciona a pasta", command=select_destination_folder)
select_button.pack(pady=130)

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window position
root.geometry(f"+{x_position}+{y_position}")

root.mainloop()

if(os.path.isdir(destination_directory) is False):
    sys.exit()
# Specify the path of the folder you want to create

destination_directory = destination_directory + '/Documentos Organizados'
surpassed_directory = destination_directory + '/Superados'
disordered_directory = destination_directory + '/Desordenado'

# Create the folder
os.makedirs(destination_directory, exist_ok=True)
os.makedirs(surpassed_directory, exist_ok=True)
os.makedirs(disordered_directory, exist_ok=True)

def CheckForSurpassedAndMoveDocument(file_name):
    filename_without_extension, file_extension = os.path.splitext(file_name)
    last_digit = filename_without_extension[-1]
    twolastDigits = filename_without_extension[-2] + last_digit
    threelastDigits = filename_without_extension[-2] + twolastDigits

    irregular = False

    if twolastDigits.isdigit():
        last_digit = twolastDigits
    #Documento com texto apos o nome
    if threelastDigits.isalpha():
        irregular = True
    #Documento com parenteses no final
    if not last_digit.isalnum():
        irregular = True
    #Documentos com data no final
    if twolastDigits.isdigit() and not threelastDigits.isalnum():
        irregular = True

    files = sorted(os.listdir(destination_directory), reverse=False)
    if not irregular:
        disordered_path = os.path.join(destination_directory, file_name)
        disordered_destination_path = os.path.join(disordered_directory, file_name)
        shutil.move(disordered_path, disordered_destination_path)
        filtered_files = []
    elif last_digit == twolastDigits:
        filtered_files = [file for file in files if file.startswith(filename_without_extension[:-2])]
    else:
        filtered_files = [file for file in files if file.startswith(filename_without_extension[:-1])]

    for file in filtered_files:
        newfilename_without_extension, newfile_extension = os.path.splitext(file)
        newlastdigit = newfilename_without_extension[-1]
        newtwolastDigits = newfilename_without_extension[-2] + newlastdigit
        newthreelastDigits = filename_without_extension[-2] + newtwolastDigits

        if newtwolastDigits.isdigit():
            newlastdigit = newtwolastDigits

        irregular = False

        # Documento com texto apos o nome
        if newthreelastDigits.isalpha():
            irregular = True
        # Documento com parenteses no final
        if not newlastdigit.isalnum():
            irregular = True
        # Documentos com data no final
        if newtwolastDigits.isdigit() and not newthreelastDigits.isalnum():
            irregular = True



        #print(filtered_files)
        #print(file_extension + " : "+ newfile_extension)

        #print(filename_without_extension + " : "+ newfilename_without_extension)

        #print(irregular)

        print(last_digit + " : " + newlastdigit)
        print(irregular)

        if (file_extension == newfile_extension
                and filename_without_extension != newfilename_without_extension
                and not irregular):
            print("a")
            if newlastdigit.isdigit() and last_digit.isdigit() and int(newlastdigit) < int(last_digit):
                surpassed_path = os.path.join(destination_directory, file)
                surpassed_destination_path = os.path.join(surpassed_directory, file)
                print("b")
            elif not newlastdigit.isdigit() and not last_digit.isdigit():
                if newlastdigit < last_digit:
                    surpassed_path = os.path.join(destination_directory, file)
                    surpassed_destination_path = os.path.join(surpassed_directory, file)
                    print("c")
                else:
                    surpassed_path = os.path.join(destination_directory, file_name)
                    surpassed_destination_path = os.path.join(surpassed_directory, file_name)
                    print("d")
            else:
                #manda o numerado para outra pasta
                if not newlastdigit.isdigit() and last_digit.isdigit():
                    surpassed_path = os.path.join(destination_directory, file)
                    surpassed_destination_path = os.path.join(surpassed_directory, file)
                    print("f")
                else:
                    surpassed_path = os.path.join(destination_directory, file_name)
                    surpassed_destination_path = os.path.join(surpassed_directory, file_name)
                    print("g")
            if os.path.exists(surpassed_path):

                shutil.move(surpassed_path, surpassed_destination_path)

def CopyAllItemsToDestination(sourse):
    for file_name in os.listdir(sourse):
        print("file copied")
        # Construct the full paths for the source
        filepath = os.path.join(sourse, file_name)

        if os.path.isfile(filepath):
            destination_path = os.path.join(destination_directory, file_name)
            shutil.copyfile(filepath, destination_path)
        elif os.path.isdir(filepath):
            CopyAllItemsToDestination(filepath)

def CopyAllItemsToDestinationScreen():
    # Open the loading screen
    loading_screen = root

    # Simulate the code execution
    CopyAllItemsToDestination(source_directory)

    # Close the loading screen
    loading_screen.destroy()

def OrganizeItemsToDestinationScreen():
    # Open the loading screen
    loading_screen = root

    # Simulate the code execution
    for file_name in sorted(os.listdir(destination_directory), reverse=False):
        file_path = os.path.join(destination_directory, file_name)
        print(file_name)
        if os.path.isfile(file_path):
            CheckForSurpassedAndMoveDocument(file_name)

    # Close the loading screen
    loading_screen.destroy()

# Create the main window
root = tk.Tk()
root.title("Aguarde")

label = tk.Label(root, text="Aguarde... Copiando arquivos...")
label.pack(padx=20, pady=20)

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window position
root.geometry(f"+{x_position}+{y_position}")

root.after(100, CopyAllItemsToDestinationScreen)
# Run the application
root.mainloop()

root = tk.Tk()
root.title("Aguarde")

label = tk.Label(root, text="Aguarde um pouco mais... Organizado arquivos...")
label.pack(padx=20, pady=20)

window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window position
root.geometry(f"+{x_position}+{y_position}")

root.after(100, OrganizeItemsToDestinationScreen)
# Run the application
root.mainloop()



#if os.path.exists(destination_directory):
   # print(destination_directory)
    #if os.name == 'nt':  # For Windows
        #subprocess.Popen(['explorer', os.path.normpath(destination_directory)])
    #elif os.name == 'posix':  # For macOS and Linux
        #subprocess.Popen(['xdg-open', os.path.normpath(destination_directory)])