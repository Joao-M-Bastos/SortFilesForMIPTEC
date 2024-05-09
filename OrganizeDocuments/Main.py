import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog
import sys

#folder_path = input("Onde estão os arquivos? ")

# Check if the entered path is a valid directory
#if os.path.isdir(folder_path) is False:
    #print(f"O caminho '{folder_path}' não é um diretorio valido.")
#else:
    #source_directory = folder_path


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


# Create the folder
os.makedirs(surpassed_directory, exist_ok=True)

def CheckForSurpassedAndMoveDocument(file_name):
    filename_without_extension, file_extension = os.path.splitext(file_name)
    last_digit = filename_without_extension[-1]
    twolastDigits = filename_without_extension[-2] + filename_without_extension[-1]
    if twolastDigits.isdigit():
        last_digit = twolastDigits

    files = sorted(os.listdir(destination_directory), reverse=False)
    if last_digit == twolastDigits:
        filtered_files = [file for file in files if file.startswith(filename_without_extension[:-2])]
    else:
        filtered_files = [file for file in files if file.startswith(filename_without_extension[:-1])]

    for file in filtered_files:
        newfilename_without_extension, newfile_extension = os.path.splitext(file)
        newlastdigit = newfilename_without_extension[-1]

        newtwolastDigits = newfilename_without_extension[-2] + newfilename_without_extension[-1]
        if newtwolastDigits.isdigit():
            newlastdigit = newtwolastDigits

        if file_extension == newfile_extension and filename_without_extension != newfilename_without_extension:
            if newlastdigit.isdigit() and last_digit.isdigit() and int(newlastdigit) < int(last_digit):
                surpassed_path = os.path.join(destination_directory, file)
                surpassed_destination_path = os.path.join(surpassed_directory, file)
            elif newlastdigit.isdigit() is False and last_digit.isdigit() is False:
                if newlastdigit < last_digit:
                    surpassed_path = os.path.join(destination_directory, file)
                    surpassed_destination_path = os.path.join(surpassed_directory, file)
                else:
                    surpassed_path = os.path.join(destination_directory, file_name)
                    surpassed_destination_path = os.path.join(surpassed_directory, file_name)
            else:
                #manda o numerado para outra pasta
                if newlastdigit.isdigit() is False and last_digit.isdigit():
                    surpassed_path = os.path.join(destination_directory, file)
                    surpassed_destination_path = os.path.join(surpassed_directory, file)
                else:
                    surpassed_path = os.path.join(destination_directory, file_name)
                    surpassed_destination_path = os.path.join(surpassed_directory, file_name)
            if os.path.exists(surpassed_path):
                shutil.move(surpassed_path, surpassed_destination_path)



def CopyAllItemsToDestination(sourse):
    for file_name in os.listdir(sourse):
        # Construct the full paths for the source
        filepath = os.path.join(sourse, file_name)

        if os.path.isfile(filepath):
            destination_path = os.path.join(destination_directory, file_name)
            shutil.copyfile(filepath, destination_path)
        elif os.path.isdir(filepath):
            CopyAllItemsToDestination(filepath)


CopyAllItemsToDestination(source_directory)

for file_name in sorted(os.listdir(destination_directory), reverse=False):
    file_path = os.path.join(destination_directory, file_name)
    print(file_name)
    if os.path.isfile(file_path):
        CheckForSurpassedAndMoveDocument(file_name)