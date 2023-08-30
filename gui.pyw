#!/usr/bin/env python
import PySimpleGUI as sg
from functions import *

sg.theme("DarkBlue13")

user_input_column = [
    [
        sg.Text("Click the Start button to begin!", key="-TEXT-"),
        sg.Button("Start", key="-START-"),
    ],
    [
        sg.Text("Current Path is: " + serverPath, key="-PATH-"),
        sg.Button("Change Path", key="-CHANGE_PATH-"),
    ],
    [sg.ProgressBar(40, orientation="h", size=(20, 20), key="-PROGRESS_BAR-")],
    [sg.Text("", key="-OUTPUT-", visible=False)],
    [
        sg.Button("Yes", key="-YES_BUTTON-", visible=False),
        sg.Button("No", key="-NO_BUTTON-", visible=False),
        sg.Exit(visible=False, disabled=True, key="-EXIT-"),
    ],
]

console_colomn = [
    [
        sg.Multiline(
            size=(30, 15),
            expand_x=True,
            expand_y=True,
            write_only=True,
            reroute_stdout=True,
            reroute_stderr=True,
            echo_stdout_stderr=True,
            autoscroll=True,
            auto_refresh=True,
        )
    ]
]

layout = [
    [
        sg.Text(
            "Copy Files Over to Client Folders",
            auto_size_text=True,
            justification="center",
            expand_x=True,
            relief=sg.RELIEF_RIDGE,
            key="-HEADING-",
        )
    ],
    [
        sg.Column(user_input_column, expand_x=True, expand_y=True),
        sg.VSeperator(),
        sg.Column(console_colomn, expand_x=True, expand_y=True),
    ],
]

window = sg.Window(
    "Copy File Script",
    layout,
    icon="icon.ico",
    resizable=True,
    keep_on_top=True,
    element_justification="center",
    finalize=True,
)
window.set_min_size(window.size)

while True:  # Event Loop
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == "-EXIT-":
        break
    elif event == "-START-":
        window["-EXIT-"].update(visible=False, disabled=True)
        print("Starting...")
        start(window, serverPath)
        try:
            if window["-OUTPUT-"].get() != "No files to move":
                window["-OUTPUT-"].update(
                    value="All files processed! Click Exit or close the window",
                    visible=True,
                )
            window["-EXIT-"].update(visible=True, disabled=False)
            window["-TEXT-"].update("Click the Start button to begin!")
            window["-START-"].update("Start", disabled=False)
            window["-CHANGE_PATH-"].update(visible=True)
        except:
            window.close()
    elif event == "-CHANGE_PATH-":
        serverPath = sg.popup_get_folder(
            "Choose folder to search", keep_on_top=True, initial_folder=serverPath
        )
        try:
            window["-PATH-"].update("Current Path is: " + serverPath)
        except:
            window["-PATH-"].update("Current Path is: ")
            pass

window.close()
