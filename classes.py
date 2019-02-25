"""classes.py
contains Player and Game class definitions.

"""


class Player:
    """blueprint for player objects to be instantiated dynamically."""

    def __init__(self, name="", word_list=[], pass_taken=0):
        """
        Args:
            name: str
            word_list: list
            pass_taken: int
        """
        self.name = name
        self.word_list = word_list
        self.pass_taken = pass_taken
