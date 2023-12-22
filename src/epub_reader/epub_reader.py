from ebooklib import ITEM_DOCUMENT
from ebooklib import epub
from bs4 import BeautifulSoup
from re import split, sub


class EpubParser:
    def __init__(self, path: str):
        self.book = epub.read_epub(path)
        texts = []
        for item in self.book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                # Parse the HTML content
                soup = BeautifulSoup(item.content, 'html.parser')
                texts.append(soup.get_text())
        self.text = "".join(texts)

    def get_text(self) -> str:
        return self.text

    def write_to_file(self, output_path: str):
        with open(output_path, "a") as file:
            sentences = self.to_sentences()
            for sentence in sentences:
                file.write(sentence + '.\n')

    def to_sentences(self):
        cleaned_string = sub(r'\s+', ' ', self.text)
        abbreviations = {'Dr.': 'Dr_PLACEHOLDER', 'Mr.': 'Mr_PLACEHOLDER', 'Mrs.': 'Mrs_PLACEHOLDER',
                         'a.m.': 'am_PLACEHOLDER', 'p.m.': 'pm_PLACEHOLDER'}
        for abbr, placeholder in abbreviations.items():
            cleaned_string = cleaned_string.replace(abbr, placeholder)
        sentences = split(r'\.\s+|\.?$', cleaned_string)
        for i in range(len(sentences)):
            for abbr, placeholder in abbreviations.items():
                sentences[i] = sentences[i].replace(placeholder, abbr)
        return sentences
