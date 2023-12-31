import os
import time
import PySimpleGUI as sg
from collections import deque
from dotenv import load_dotenv

load_dotenv()

folderTypes = []
dbPath = os.getenv("DB_PATH")
serverPath = os.getenv("SERVER_PATH")
clientsPath = os.getenv("CLIENTS_PATH")


def dbCheck():
    global folderTypes

    with open(dbPath) as f:
        next(f)
        for line in f:
            folderTypes.append(line.split(",")[1])
            folderTypes[-1] = folderTypes[-1].replace("\n", "")
    f.close()
    return


def userInput(window, clientFolder, file):
    window["-YES_BUTTON-"].update(visible=True)
    window["-NO_BUTTON-"].update(visible=True)
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event == "-YES_BUTTON-":
            try:
                # os.rename(serverPath + "\\" + file, clientsPath + "\\" + clientFolder)
                sg.popup(
                    "File moved to " + clientFolder + " successfully!",
                    keep_on_top=True,
                    title="Success",
                )
                print("File moved successfully!")
            except Exception as e:
                sg.popup("ERROR: File move failed!")
                print("File move failed!")
                print(e)
                break
            window["-OUTPUT-"].update(visible=False)
            window["-YES_BUTTON-"].update(visible=False)
            window["-NO_BUTTON-"].update(visible=False)
            break
        elif event == "-NO_BUTTON-":
            dec = sg.popup_yes_no(
                "Would you like to choose a different folder?", keep_on_top=True
            )
            if dec == "Yes":
                clientFolder = sg.popup_get_folder(
                    "Choose folder for " + file,
                    keep_on_top=True,
                    initial_folder=clientFolder.split("\\")[0],
                )
                if clientFolder == None or clientFolder == "":
                    sg.popup("File not moved!", keep_on_top=True)
                    print("File not moved!")
                    window["-OUTPUT-"].update(visible=False)
                    window["-YES_BUTTON-"].update(visible=False)
                    window["-NO_BUTTON-"].update(visible=False)
                    break
                clientFolder = (
                    clientFolder.split("/")[-2] + "\\" + clientFolder.split("/")[-1]
                )
                # os.rename(serverPath + "\\" + file, clientsPath + "\\" + clientFolder)
                sg.popup(
                    "File moved to " + clientFolder + " successfully!", keep_on_top=True
                )
                print("File moved successfully!")
                window["-OUTPUT-"].update(visible=False)
                window["-YES_BUTTON-"].update(visible=False)
                window["-NO_BUTTON-"].update(visible=False)
                break
            else:
                sg.popup("File not moved!", keep_on_top=True)
                print("File not moved!")
                window["-OUTPUT-"].update(visible=False)
                window["-YES_BUTTON-"].update(visible=False)
                window["-NO_BUTTON-"].update(visible=False)
                break
    return


def start(window, serverPathChange):
    global folderTypes, serverPath

    if serverPathChange != serverPath:
        serverPath = serverPathChange
    window["-START-"].update("Started", disabled=True)
    window["-CHANGE_PATH-"].update(visible=False)
    dbCheck()
    window["-TEXT-"].update("Searching for files...")
    clientFileNames = os.listdir(clientsPath)
    serverFiles = os.listdir(serverPath)
    fileQ = deque()
    folderQ = deque()

    for x in serverFiles:
        temp = x.split()
        if len(temp) <= 2:
            continue
        temp = temp[1]
        for y in clientFileNames:
            if temp in y:
                fileQ.append(x)
                folderQ.append(y)
            else:
                continue
    print(fileQ)
    print(folderQ)

    if len(fileQ) == 0:
        try:
            window["-OUTPUT-"].update(visible=True, value="No files to move")
            return
        except:
            return
    while len(fileQ) > 0:
        file = fileQ.popleft()
        clientFolder = folderQ.popleft()
        global fileFlag
        fileFlag = False
        try:
            window["-TEXT-"].update("Looking for document matches...")
            window["-PROGRESS_BAR-"].update_bar(0)
        except:
            return
        for x in folderTypes:
            try:
                window["-PROGRESS_BAR-"].update_bar((folderTypes.index(x) + 1))
            except:
                return
            if x in file:
                if folderTypes.index(x) < 1:
                    clientFolder = clientFolder + "\\A - CLIENT INFO"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 1 and folderTypes.index(x) < 5:
                    clientFolder = clientFolder + "\\B - CORRESPONDENCE"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 5 and folderTypes.index(x) < 9:
                    clientFolder = clientFolder + "\\C - DISCLOURES"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 9 and folderTypes.index(x) < 10:
                    clientFolder = clientFolder + "\\E - DISCOVERY"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 10 and folderTypes.index(x) < 12:
                    clientFolder = clientFolder + "\\G - PAYMENTS & INVOICES"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 12 and folderTypes.index(x) < 13:
                    clientFolder = clientFolder + "\\H - NOTES"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif folderTypes.index(x) >= 13 and folderTypes.index(x) < 39:
                    clientFolder = clientFolder + "\\I - PLEADINGS"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
                elif (
                    folderTypes.index(x) == 39
                    and x not in file.split()[1]
                    and x not in file.split()[2]
                ):
                    clientFolder = clientFolder + "\\F - CONTRACT"
                    fileFlag = True
                    print(file + " is " + x + "!")
                    break
            else:
                print(file + " is not " + x)
                time.sleep(0.1)
                continue
        if fileFlag == False:
            clientFolder = clientFolder + "\\D - MISCELLANEOUS"
            try:
                window["-TEXT-"].update("Could not find a match")
            except:
                return
        else:
            try:
                window["-TEXT-"].update("Found a match!")
            except:
                return

        try:
            window["-OUTPUT-"].update(
                visible=True,
                value="Move " + file + " to " + clientFolder + " | Is this correct?",
            )
        except:
            return
        userInput(window, clientFolder, file)
    try:
        window["-PROGRESS_BAR-"].update_bar(0)
        return
    except:
        return
