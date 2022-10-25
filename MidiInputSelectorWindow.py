import PySimpleGUIQt as sg
import pygame.midi


class MidiInputSelectorWindow:
    def __init__(self, layout):
        pygame.midi.init()
        self.layout = layout
        self.window = sg.Window('PianoSheetGenerator', self.layout, size=(500, 200)).Finalize()
        self.window.FindElement("-DropDown-").Update(values=self.print_midi_devices())

    def run(self):
        while True:
            event, values = self.window.read()
            print(event, values)

            if event == sg.WIN_CLOSED or event == 'Quit':
                break

            if event == "-LaunchApp-":
                self.window.close()
                return int(values["-DropDown-"].split(" ")[1])

    @staticmethod
    def print_midi_devices():
        midi_devices_list = []
        for n in range(pygame.midi.get_count()):
            if pygame.midi.get_device_info(n)[2] == 1:
                midi_devices_list.append(' '.join(("ID:", str(n), pygame.midi.get_device_info(n)[1].decode())))
        return midi_devices_list
