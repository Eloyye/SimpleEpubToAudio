import unittest

from src.epub_reader.epub_reader import EpubParser
# from os import getcwd, path


class MyTestCase(unittest.TestCase):
    def test_simple(self):
        parser = EpubParser()
        sentences = ("How are you today? "
                     "This is a good day in my opinion."
                     " Wow! indeed. "
                     "Mr. Micheal, Mr. John,"
                     "and Mrs. Alice walks"
                     "into a bar")
        parser.set_text(sentences)
        sentences = parser.to_sentences()
        print(f'\n{sentences}\n')


if __name__ == '__main__':
    unittest.main()
