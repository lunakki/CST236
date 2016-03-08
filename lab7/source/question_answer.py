"""For keeping track of questions and answers in main"""


# pylint: disable=too-few-public-methods
# more of a struct than a class
class QA(object):
    """A question answer object"""
    def __init__(self, question, answer):
        """Initialization"""
        self.question = question
        self.function = None
        self.value = None
        if hasattr(answer, '__call__'):
            self.function = answer
        else:
            self.value = answer
