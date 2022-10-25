import os


class PageHandler:
    def __init__(self):
        self.multiple_pages = None
        self.pdf_existance = None
        self.png_existance = None

    @staticmethod
    def list_pages(page_name):
        file_list = []
        for filename in os.listdir("."):
            root, ext = os.path.splitext(filename)
            if root.startswith(page_name):
                file_list.append(filename)
        return file_list

    def delete_pages(self):
        self.multiple_pages = os.path.exists("./lilypond_piano_sheet-page1.png")
        self.pdf_existance = os.path.exists("./lilypond_piano_sheet.pdf")
        self.png_existance = os.path.exists("./lilypond_piano_sheet.png")

        if self.multiple_pages:
            for page in self.list_pages('lilypond_piano_sheet-page'):
                os.remove(page)

        elif self.png_existance:
            os.remove("lilypond_piano_sheet.png")

        if self.pdf_existance:
            os.remove("lilypond_piano_sheet.pdf")

        for page in self.list_pages("SheetPng"):
            os.remove(page)
