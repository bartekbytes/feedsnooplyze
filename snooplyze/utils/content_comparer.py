import difflib

class ContentComparer:

    def __init__(self, new_string : str, old_string: str):
        self.new_string = new_string
        self.old_string = old_string

    def get_difference(self):
        diff = difflib.ndiff(self.old_string.split(), self.new_string.split())
        added = [word[2:] for word in diff if word.startswith('+ ')]
        return ' '.join(added)


