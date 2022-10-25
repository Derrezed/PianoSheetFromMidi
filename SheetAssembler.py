import mingus.extra.lilypond as LilyPond
from PIL import Image
import os
from PageHandler import PageHandler


class SheetAssembler:
    def __init__(self):
        self.page_handler = PageHandler()

    def midi_output_handler(self, left, right, imagename, title, composer, subtitle, time, key_signature):
        splitted_key_signature = key_signature.split()
        start = (f"""
                    \\header{{
                    title = "{title}"
                    composer = "{composer}"
                    subtitle = "{subtitle}"
                    }}
                    upper = 
                    {{\\key {splitted_key_signature[0]} \\{splitted_key_signature[1]} \\time {time} 
                    """)

        mid = f"""
                    }}
                    lower = 
                    {{\\key {splitted_key_signature[0]} \\{splitted_key_signature[1]} \\time {time}
                     \\clef bass
                    """

        end = """
                    }
                    \score {
                    \\new PianoStaff \with { instrumentName = "Piano" }
                    <<
                    \\new Staff = "upper" \\upper
                    \\new Staff = "lower" \lower
                    >>
                    \layout { }
                    }
                        """
        result = start + right + mid + left + end
        print(result)

        LilyPond.to_png(result, "lilypond_piano_sheet")

        if not os.path.exists("./lilypond_piano_sheet-page1.png"):
            image = Image.open("lilypond_piano_sheet.png")
            image = image.resize((600, 800), Image.ANTIALIAS)
            image.save(fp=f"{imagename}.png")
        else:
            pages = self.page_handler.list_pages("lilypond_piano_sheet-page")
            for page in enumerate(pages):
                image = Image.open(str(page[1]))
                image = image.resize((600, 800), Image.ANTIALIAS)
                image.save(fp=f"{imagename}{page[0]+1}.png")
