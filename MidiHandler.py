import numpy


class MidiHandler:
    def __init__(self, dataholder, myinput):
        self.myinput = myinput
        self.dataholder = dataholder
        self.keys_down = []
        self.keys_list = []
        self.running = True

    def stop(self):
        self.running = False

    def readInput(self, scale):
        while self.running:
            if self.myinput.poll():
                raw_data = self.myinput.read(1)
                event = raw_data[0]
                data = event[0]
                type = data[0]  # 144 - wciśnięty klawisz, 128 - puszczony klawisz

                if type in (144, 128):
                    print("--------------------------------------------------------------")
                    print(f"Raw Data - {raw_data}")
                    print(f"Event - {event}")
                    print("Key press") if type == 144 else print("Key release")
                    note_number = data[1]
                    velocity = data[2]
                    if velocity > 0 and note_number not in self.keys_down:
                        self.keys_down.append(note_number)
                    elif velocity == 0 and note_number in self.keys_down:
                        key_index = self.keys_down.index(note_number)
                        del self.keys_down[key_index]
                    note = MidiHandler.number_to_note(note_number, scale)
                    print(f"Note - {note}, Note number - {note_number}")
                    self.dataholder.add_keys([note.lower(), event[1], event[0][1]])

    @staticmethod
    def number_to_note(number, scale):
        notes = {
            **dict.fromkeys(["c major", "d major", "e major", "g major", "a major", "b major", "e minor", "fis minor",
                             "cis minor", "b minor"],
                            ['C', 'CIS', 'D', 'DIS', 'E', 'F', 'FIS', 'G', 'GIS', 'A', 'AIS', 'B']),
            **dict.fromkeys(["f major", "c minor", "d minor", "bes minor", "f minor", "g minor", "a minor"],
                            ['C', 'DES', 'D', 'ES', 'E', 'F', 'GES', 'G', 'AS', 'A', 'BES', 'B']),
            **dict.fromkeys(["as major", "bes major", "es major"],
                            ['C', 'DES', 'D', 'ES', 'E', 'F', 'GES', 'G', 'AS', 'A', 'BES', 'B']),
            **dict.fromkeys(["cis major"],
                            ['BIS','CES', 'D', 'DIS', 'E', 'EIS', 'FIS', 'G', 'GIS', 'A', 'AIS', 'B']),
            **dict.fromkeys(["as minor"],
                            ['CES', 'C', 'DES', 'D', 'ES', 'FES', 'F', 'GES', 'G', 'AS', 'A', 'BES']),
            **dict.fromkeys(["es minor"],
                            ['CES', 'C', 'DES', 'D', 'ES', 'E', 'F', 'GES', 'G', 'AS', 'A', 'BES']),
                }
        return notes[scale][number % 12]

    @staticmethod
    def rhythmicity(keys, numbers_check, bpm):

        key_press = []
        key_release = []
        input_notes = ''
        time_frame = (60000 / int(bpm))

        print("Keys list: ", keys)
        for i in range(len(keys)):
            if i % 2 == 0:
                key_press.append(keys[i])
            else:
                key_release.append(keys[i])

        print("Key press", key_press)
        print("Key release", key_release)

        key_press_notes = []
        key_press_time_diff = []

        last_key_time = key_press[-1][1] - key_release[-1][1]

        for i in key_press:
            key_press_notes.append(i[0])
            key_press_time_diff.append(i[1])

        print(key_press_notes)
        print(key_press_time_diff)

        notes_time_diff = numpy.diff(key_press_time_diff)
        notes_time_diff_final = numpy.append(notes_time_diff, abs(last_key_time))

        octaves_dict = {
            **dict.fromkeys([i for i in range(21, 24)], ",,,,,"),
            **dict.fromkeys([i for i in range(24, 36)], ",,,"),
            **dict.fromkeys([i for i in range(36, 48)], ","),
            **dict.fromkeys([i for i in range(48, 60)], ""),
            **dict.fromkeys([i for i in range(60, 72)], "'"),
            **dict.fromkeys([i for i in range(72, 84)], "''"),
            **dict.fromkeys([i for i in range(84, 96)], "'''"),
            **dict.fromkeys([i for i in range(96, 108)], "''''"),
            **dict.fromkeys([108], "'''''")
        }

        for i in enumerate(key_press):
            print(i[1][2])
            if numbers_check:
                numbers = f'-"{i[0] + 1}" '
            else:
                numbers = ' '

            if (time_frame/1.5) + 50 < notes_time_diff_final[i[0]] < time_frame + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '4' + numbers

            elif (time_frame/4) + 50 < notes_time_diff_final[i[0]] < (time_frame/2) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '8' + numbers

            elif (time_frame*1.5) + 50 < notes_time_diff_final[i[0]] < (time_frame*2) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '2' + numbers

            elif (time_frame*2) + 50 < notes_time_diff_final[i[0]] < (time_frame*3) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '2.' + numbers

            elif (time_frame*3) + 50 < notes_time_diff_final[i[0]] < (time_frame*4) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '1' + numbers

            elif 1 < notes_time_diff_final[i[0]] < (time_frame/4) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '16' + numbers

            elif time_frame + 50 < notes_time_diff_final[i[0]] < (time_frame*1.5) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '4.' + numbers

            elif (time_frame/2) + 50 < notes_time_diff_final[i[0]] < (time_frame*0.75) + 50:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + '8.' + numbers

            else:
                input_notes += key_press_notes[i[0]] + octaves_dict[i[1][2]] + numbers

        input_notes += ' \\bar "|."'

        return input_notes
