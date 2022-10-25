import PySimpleGUIQt as sg
import threading
from DataHolder import DataHolder
from MidiHandler import MidiHandler
import pygame.midi
from SheetAssembler import SheetAssembler
import win32print
import win32api
import os
from PageHandler import PageHandler
from fpdf import FPDF
from shutil import copyfile


class MainWindow:
    def __init__(self, layout, midi_device_id):
        self.layout = layout
        self.midi_device_id = midi_device_id
        self.window = sg.Window('PianoSheetGenerator', self.layout, size=(1300, 950))
        self.left_data_holder = DataHolder()
        self.right_data_holder = DataHolder()
        self.my_input = pygame.midi.Input(int(midi_device_id))
        self.right_midi_handler = MidiHandler(self.right_data_holder, self.my_input)
        self.left_midi_handler = MidiHandler(self.left_data_holder, self.my_input)
        self.thread1 = None
        self.thread2 = None
        self.imagename = "SheetPng"
        self.left_input_notes = None
        self.right_input_notes = None
        self.joined_left_input_notes = None
        self.joined_right_input_notes = None
        self.keys_change = DataHolder()
        self.keys_change_right_holder = None
        self.keys_change_left_holder = None
        self.multiple_pages = None
        self.current_page = 1
        self.page_handler = PageHandler()
        self.sheet_assembler = SheetAssembler()
        self.lilypond_page_name = 'lilypond_piano_sheet-page'

    def run(self):
        while True:
            event, values = self.window.read()

            print(event, values)

            if event == sg.WIN_CLOSED or event == 'Quit':
                break

            elif event == 'Midi Listen right hand':
                self.thread1 = threading.Thread(target=self.right_midi_handler.readInput,
                                                args=(values["-Key Signature-"],))
                self.thread1.start()
                self.window.FindElement('Midi Listen right hand').update(disabled=True)
                self.window.FindElement('Midi Listen left hand').update(disabled=False, button_color=(1, 1))

            elif event == 'Midi Listen left hand':
                self.right_midi_handler.stop()
                self.thread1.join()
                self.thread2 = threading.Thread(target=self.left_midi_handler.readInput,
                                                args=(values["-Key Signature-"],))
                self.thread2.start()
                self.window.FindElement('Midi Listen left hand').Update(disabled=True)
                self.window.FindElement('Make Piano Sheet').Update(disabled=False, button_color=(1, 1))

            elif event == "Make Piano Sheet":
                self.left_midi_handler.stop()
                self.thread2.join()
                self.window.FindElement('Make Piano Sheet').Update(disabled=False, button_color=(1, 1))
                self.window.FindElement('Print').Update(disabled=False, button_color=(1, 1))

                self.right_input_notes = MidiHandler.rhythmicity(self.right_data_holder.keys, values['-Numbers-'],
                                                                 values["-Tempo-"])
                self.left_input_notes = MidiHandler.rhythmicity(self.left_data_holder.keys, values['-Numbers-'],
                                                                values["-Tempo-"])
                self.sheet_assembler.midi_output_handler(self.left_input_notes, self.right_input_notes, self.imagename,
                                                         values['-Title-'], values['-Composer-'], values['-Subtitle-'],
                                                         values['-Time Signature-'], values['-Key Signature-'])
                self.multiple_pages = os.path.exists("./lilypond_piano_sheet-page1.png")

                if self.multiple_pages:
                    self.window['-IMAGE-'].update(f"{self.imagename}{self.current_page}.png")
                else:
                    self.window['-IMAGE-'].update(f"{self.imagename}.png")

                self.keys_change.add_keys_change_right(self.right_input_notes)
                self.keys_change_right_holder = self.keys_change.keys_change_right

                self.keys_change.add_keys_change_left(self.left_input_notes)
                self.keys_change_left_holder = self.keys_change.keys_change_left

                self.window['-RightNotesText-'].update(f'Right hand notes:\n{self.right_input_notes}\n')
                self.window['-LeftNotesText-'].update(f'Left hand notes:\n{self.left_input_notes}\n')

                self.window['-CorrectionRight-'].update(visible=True)
                self.window['-KeyNrRight-'].update(visible=True)
                self.window['-KeyChangeRight-'].update(visible=True)
                self.window['Change'].update(visible=True)
                self.window['-CorrectionLeft-'].update(visible=True)
                self.window['-KeyNrLeft-'].update(visible=True)
                self.window['-KeyChangeLeft-'].update(visible=True)
                self.window['Add'].update(visible=True)
                self.window['-ChangeToRight-'].update(visible=True)
                self.window['-ChangeToLeft-'].update(visible=True)
                self.window['-Corrections-'].update(visible=True)

                self.window.FindElement('-FileBrowse-').update(disabled=False, button_color=(1, 1))

            elif event == "Print":
                images_list = []
                win32print.GetDefaultPrinter()
                pdf = FPDF()
                pdf.set_auto_page_break(0)
                if self.multiple_pages:
                    for pages in self.page_handler.list_pages(self.lilypond_page_name):
                        images_list.append(pages)

                    for image in images_list:
                        pdf.add_page()
                        pdf.image(image, x=0, y=0, w=210,  h=297)
                    pdf.output("lilypond_piano_sheet.pdf", "F")
                    win32api.ShellExecute(0, "print", "lilypond_piano_sheet.pdf", None, ".", 0)

                else:
                    win32api.ShellExecute(0, "print", "lilypond_piano_sheet.png", None, ".", 0)

            elif event == "Change":

                if values['-KeyNrRight-'] == "":
                    self.joined_right_input_notes = self.keys_change_right_holder
                else:
                    split_keys_change_right_holder = self.keys_change_right_holder.split()
                    split_keys_change_right_holder[int(values['-KeyNrRight-']) - 1] = values['-KeyChangeRight-']
                    self.joined_right_input_notes = " ".join(split_keys_change_right_holder)
                    self.keys_change_right_holder = self.joined_right_input_notes

                if values['-KeyNrLeft-'] == "":
                    self.joined_left_input_notes = self.keys_change_left_holder
                else:
                    split_keys_change_left_holder = self.keys_change_left_holder.split()
                    split_keys_change_left_holder[int(values['-KeyNrLeft-']) - 1] = values['-KeyChangeLeft-']
                    self.joined_left_input_notes = " ".join(split_keys_change_left_holder)
                    self.keys_change_left_holder = self.joined_left_input_notes

                self.sheet_assembler.midi_output_handler(self.joined_left_input_notes, self.joined_right_input_notes,
                                                         self.imagename, values['-Title-'], values['-Composer-'],
                                                         values['-Subtitle-'], values['-Time Signature-'],
                                                         values['-Key Signature-'])

                if self.multiple_pages:
                    self.window['-IMAGE-'].update(f"{self.imagename}{self.current_page}.png")
                else:
                    self.window['-IMAGE-'].update(f"{self.imagename}.png")

                self.window['-RightNotesText-'].update(f'Right hand notes:\n{self.joined_right_input_notes}')
                self.window['-LeftNotesText-'].update(f'Left hand notes:\n{self.joined_left_input_notes}')

            elif event == "Add":

                if values['-KeyNrRight-'] == "":
                    self.joined_right_input_notes = self.keys_change_right_holder
                else:
                    split_keys_change_right_holder = self.keys_change_right_holder.split()
                    split_keys_change_right_holder[int(values['-KeyNrRight-']) - 1] = \
                        split_keys_change_right_holder[int(values['-KeyNrRight-']) - 1] + \
                        " " + values['-KeyChangeRight-']
                    self.joined_right_input_notes = " ".join(split_keys_change_right_holder)
                    self.keys_change_right_holder = self.joined_right_input_notes

                if values['-KeyNrLeft-'] == "":
                    self.joined_left_input_notes = self.keys_change_left_holder
                else:
                    split_keys_change_left_holder = self.keys_change_left_holder.split()
                    split_keys_change_left_holder[int(values['-KeyNrLeft-']) - 1] = \
                        split_keys_change_left_holder[int(values['-KeyNrLeft-']) - 1] + " " + values['-KeyChangeLeft-']
                    self.joined_left_input_notes = " ".join(split_keys_change_left_holder)
                    self.keys_change_left_holder = self.joined_left_input_notes

                self.sheet_assembler.midi_output_handler(self.joined_left_input_notes, self.joined_right_input_notes,
                                                   self.imagename, values['-Title-'], values['-Composer-'],
                                                         values['-Subtitle-'], values['-Time Signature-'],
                                                         values['-Key Signature-'])

                if self.multiple_pages:
                    self.window['-IMAGE-'].update(f"{self.imagename}{self.current_page}.png")
                else:
                    self.window['-IMAGE-'].update(f"{self.imagename}.png")

                self.window['-RightNotesText-'].update(f'Right hand notes:\n{self.joined_right_input_notes}')
                self.window['-LeftNotesText-'].update(f'Left hand notes:\n{self.joined_left_input_notes}')

            elif event == "-NextPage-":
                if self.multiple_pages:
                    self.window['-IMAGE-'].update(f'SheetPng{self.current_page+1}.png')
                    self.current_page += 1

                if len(self.page_handler.list_pages(self.lilypond_page_name)) == self.current_page:
                    self.window.FindElement('-NextPage-').update(disabled=True)
                    self.window.FindElement('-PreviousPage-').update(disabled=False, button_color=(1, 1))

                if self.current_page != 1:
                    self.window.FindElement('-PreviousPage-').update(disabled=False, button_color=(1, 1))

            elif event == "-PreviousPage-":
                self.window.FindElement('-NextPage-').update(disabled=False, button_color=(1, 1))
                if self.multiple_pages:
                    self.current_page -= 1
                    self.window['-IMAGE-'].update(f'SheetPng{self.current_page}.png')

                if self.current_page == 1:
                    self.window.FindElement('-PreviousPage-').update(disabled=True)

            elif event == "-SaveNotes-":
                if self.multiple_pages:
                    for page in enumerate(self.page_handler.list_pages(self.lilypond_page_name)):
                        copyfile(page[1], f"{values['-PathContainer-']}/lilypond_piano_sheet-page{page[0]+1}.png")
                else:
                    copyfile("lilypond_piano_sheet.png", f"{values['-PathContainer-']}/lilypond_piano_sheet.png")

            elif values["-PathContainer-"]:
                self.window.FindElement('-SaveNotes-').update(disabled=False, button_color=(1, 1))

        self.window.close()


