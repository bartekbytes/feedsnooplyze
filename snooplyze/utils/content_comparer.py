import difflib

class ContentComparer:
    """
    A class for comparing two strings and extracting the words added in the new string compared to the old string.
    Attributes:
        new_string (str): The updated string to compare.
        old_string (str): The original string to compare against.
    Methods:
        get_difference():
            Returns a string containing words that were added in the new string compared to the old string.
    """

    def __init__(self, new_string : str, old_string: str):
        self.new_string = new_string
        self.old_string = old_string

    def get_difference(self):
        """
        Computes the words that have been added in the new string compared to the old string.

        Uses difflib.ndiff to compare the old and new strings, splitting them into words.
        Returns a string containing all words that are present in the new string but not in the old string.

        Returns:
            str: A space-separated string of words that were added.
        """
        diff = difflib.ndiff(self.old_string.split(), self.new_string.split())
        added = [word[2:] for word in diff if word.startswith('+ ')]
        return ' '.join(added)


