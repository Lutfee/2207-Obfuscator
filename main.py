# importing tkinter and tkinter.ttk
# and all their functions and classes
import os
from tkinter import *
# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile
from tkinter.ttk import *

window = Tk()
window.geometry('480x480')
window.config(background="light blue")
content = ""
file_name = ""


# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    global content
    global file_name
    file = askopenfile(mode='r')
    file_name = os.path.basename(file.name)
    os.system("echo Hello from the other side!")


    if file is not None:
        if file_name.__contains__(".apk"):
            print(file)
            apk_decompile(file.name)
        else:
            content = file.read()
            with open(f'data_files/{file_name}', 'w') as f:
                f.write(content)
                f.close()

        loaded = Label(window, text=f"{file_name} is loaded")
        loaded.config(anchor=CENTER)
        loaded.pack()

# decompile apk
def apk_decompile(apk_file):
    apk_name = os.path.basename(apk_file)
    os.system("java -jar tools/apktool.jar d -f " + apk_file + " -o output/" + apk_name)






# -------------------- Obfuscation Part --------------------
def obfuscate_file():
    return None


def nocomment():
    inFile = open(f"data_files/{file_name}", "r")
    change = ""

    for line in inFile:
        line = line.split("#",1)
        print(line[0])
        change = change + str(line[0])
        print(change)


    inFile.close()
    outFile = open(f"data_files/{file_name}", "w")
    outFile.write(change)
    outFile.close()




# -------------------- GUI Window --------------------
btn = Button(window, text='Open', command=lambda: open_file())
btn2 = Button(window, text='Remove Comments', command=lambda: nocomment())
# btn2 = Button(window, text='Save', command=lambda: apktorar())
btn.pack(side=TOP, pady=10)
btn2.pack(side=TOP, pady=10)

window.mainloop()
