import PySimpleGUIQt as sg
from MainWindow import MainWindow
from MidiInputSelectorWindow import MidiInputSelectorWindow
from PageHandler import PageHandler
sg.theme('Default1')


class App:
    MAIN_WINDOW_LAYOUT_LEFT = [
        [
            sg.Text("Composer", size=(10, 0.5), justification="r"),
            sg.Input(default_text="Composer", key='-Composer-', justification='c', size=(20, 1))
        ],
        [
            sg.Text("Title", size=(10, 0.5), justification="r"),
            sg.InputText(default_text="Test Title", key='-Title-', justification='c', size=(20, 1))
        ],
        [
            sg.Text("Subtitle", size=(10, 0.5), justification="r"),
            sg.InputText(default_text="Test Subtitle", key='-Subtitle-', justification='c', size=(20, 1))
        ],
        [
            sg.Text("Tempo(bpm)", size=(10, 0.5), justification="r"),
            sg.InputText(default_text="100", key='-Tempo-', justification='c', size=(20, 1))
        ],
        [
            sg.Text("Time Signature", size=(10, 0.5), justification="r"),
            sg.InputText(default_text="4/4", key='-Time Signature-', justification='c', size=(20, 1))
        ],
        [
            sg.Text("Key Signature", size=(10, 0.5), justification="r"),
            sg.InputText(default_text="c major", key='-Key Signature-', justification='c', size=(20, 1))
        ],

        [
            sg.Button(button_text='Midi Listen right hand', size=(15, 1.3)),
            sg.Button(button_text='Midi Listen left hand', disabled=True, size=(15, 1.3)),
            sg.Button(button_text='Make Piano Sheet', disabled=True, size=(15, 1.3)),
            sg.Button('Print', disabled=True, size=(6, 1.3)),
            sg.Button('Quit', size=(6, 1.3))
        ],
        [
            sg.Checkbox('Print numbers', default=False, key='-Numbers-')
        ],
        [
            sg.Input(key="-PathContainer-", visible=False, enable_events=True),
            sg.FolderBrowse(button_text="Choose save location", target="-PathContainer-", key="-FileBrowse-",
                            size=(20, 1), disabled=True),
            sg.Button(button_text="Save piano sheets", key="-SaveNotes-", size=(20, 1), disabled=True)
        ],
        [
            sg.Multiline(default_text='Right hand notes:\n', key="-RightNotesText-", size=(60, 12))
        ],
        [
            sg.Multiline(default_text='Left hand notes:\n', key="-LeftNotesText-", size=(60, 12))
        ]
    ]

    MAIN_WINDOW_LAYOUT_RIGHT = [
        [
            sg.Button(button_text=" < ", size=(3, 1), key="-PreviousPage-", disabled=True),
            sg.Image(key="-IMAGE-", filename="blank_page.png"),
            sg.Button(button_text=" > ", size=(3, 1), key="-NextPage-")
        ],
        [
            sg.Text('Corrections', key="-Corrections-", visible=False)
        ],
        [
            sg.Text('Right hand note number:', visible=False, key='-CorrectionRight-', size=(15, 1)),
            sg.Input(key='-KeyNrRight-', size=(5, 1), visible=False),
            sg.Text("Change to:", size=(8, 1), key="-ChangeToRight-", visible=False),
            sg.Input(key='-KeyChangeRight-', size=(5, 1), visible=False),
            sg.Button('Change', size=(8, 1), visible=False)
        ],
        [
            sg.Text('Left hand note number:', visible=False, key='-CorrectionLeft-', size=(15, 1)),
            sg.Input(key='-KeyNrLeft-', size=(5, 1), visible=False),
            sg.Text("Change to:", size=(8, 1), key="-ChangeToLeft-", visible=False),
            sg.Input(key='-KeyChangeLeft-', size=(5, 1), visible=False),
            sg.Button('Add', size=(8, 1), visible=False)
        ]
    ]

    MAIN_WINDOW_LAYOUT = [
        [
            sg.Column(layout=MAIN_WINDOW_LAYOUT_LEFT, element_justification="c"),
            sg.Column(layout=MAIN_WINDOW_LAYOUT_RIGHT, element_justification="c")
        ]
    ]

    MIDI_INPUT_SELECTOR_LAYOUT = [
        [sg.Text("Select Midi Device\n", auto_size_text=True, font=("Helvetica", 15))],
        [sg.DropDown(values=[""], key="-DropDown-", size=(30, 1), readonly=True)],
        [sg.Text(" ")],
        [sg.Button(button_text="Launch Application", key="-LaunchApp-", size=(20, 1))]
    ]

    MIDI_INPUT_SELECTOR_LAYOUT_FINAL = [
        [sg.Column(layout=MIDI_INPUT_SELECTOR_LAYOUT, element_justification="c")]
    ]

    @staticmethod
    def run():
        page_handler = PageHandler()
        page_handler.delete_pages()

        midi_input_selector_window = MidiInputSelectorWindow(App.MIDI_INPUT_SELECTOR_LAYOUT_FINAL)
        midi_device_id = midi_input_selector_window.run()

        main_window = MainWindow(App.MAIN_WINDOW_LAYOUT, midi_device_id)

        main_window.run()
        midi_input_selector_window.run()


if __name__ == '__main__':
    app = App()
    app.run()
