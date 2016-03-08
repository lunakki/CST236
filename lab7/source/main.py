"""Answer questions with static values or functions; takes new questions at runtime."""
from copy import deepcopy
import getpass
import difflib
from source.question_answer import QA
from source.shape_checker import get_triangle_type, get_quad_type, get_rectangle_type
from source.question_solvers import get_fibonacci_number, get_date_time, get_pi_digit, \
    convert_feet_to_inches, convert_inches_to_feet, convert_gallons_to_liters, \
    convert_liters_to_gallons, convert_teaspoons_to_cups, convert_cups_to_teaspons, \
    convert_km_to_miles, convert_miles_to_km, convert_acres_to_sqfeet, convert_sqfeet_to_acres, \
    get_rgb_hex, get_is_divisible, get_days_until_date, get_lotto_numbers, get_exponent_result, \
    get_age
from source.git_utils import is_file_in_repo, get_git_file_info, get_repo_branch, get_repo_url, \
    get_file_info

NOT_A_QUESTION_RETURN = "Was that a question?"
UNKNOWN_QUESTION = "I don't know, please provide the answer"
NO_QUESTION = 'Please ask a question first'
NO_TEACH = 'I don\'t know about that. I was taught differently'


class Interface(object):
    """Class for the question/answer interface"""
    # pylint: disable=too-many-instance-attributes
    # This is a reasonable amount and they are all used
    def __init__(self):
        self.how_dict = {}
        self.what_dict = {}
        self.where_dict = {}
        self.who_dict = {}

        self.keywords = ['How', 'What', 'Where', 'Who', "Why", "Is"]
        self.question_mark = chr(0x3F)

        self.question_answers = []
        self.reset_questions()
        self.backup_questions = deepcopy(self.question_answers)
        self.last_question = None

    def ask(self, question=""):
        """Ask a question and get an answer (string)"""
        if not isinstance(question, str):
            self.last_question = None
            raise Exception('Not A String!')
        if question[-1] != self.question_mark or question.split(' ')[0] not in self.keywords:
            self.last_question = None
            if question == "Open the door hal":
                return "I'm afraid I can't do that " + getpass.getuser()
            elif question == "Please clear memory":
                self.reset_questions()
            elif question == "Please restore memory":
                self.restore_questions()
            else:
                return NOT_A_QUESTION_RETURN
        else:
            parsed_question = ""
            args = self.parse_question(question)
            parsed_question = self.last_question

            for answer in self.question_answers.values():
                if difflib.SequenceMatcher(a=answer.question, b=parsed_question).ratio() >= .90:
                    if answer.function is None:
                        self.write_to_file("Answer: " + answer.value)
                        return answer.value
                    else:
                        try:
                            answer_output = answer.function(*args)
                            self.write_to_file("Answer: " + answer_output)
                            return answer_output
                        except:
                            raise Exception("Too many extra parameters")
            return UNKNOWN_QUESTION

    def teach(self, answer=""):
        """Teach an answer to an unknown question"""
        if self.last_question is None:
            return NO_QUESTION
        elif self.last_question in self.question_answers.keys():
            return NO_TEACH
        else:
            self.__add_answer(answer)

    def correct(self, answer=""):
        """Change an answer to a known question"""
        if self.last_question is None:
            return NO_QUESTION
        else:
            self.__add_answer(answer)

    def __add_answer(self, answer):
        """No idea what this is for"""
        self.question_answers[self.last_question] = QA(self.last_question, answer)

    def reset_questions(self):
        """Resets questions back to defaults"""
        self.backup_questions = deepcopy(self.question_answers)
        self.question_answers = {
            'What type of triangle is ': QA('What type of triangle is ', get_triangle_type),
            'What type of quadrilateral is ': QA('What type of quadrilateral is ',
                                                 get_quad_type),
            'What type of rectangle is ': QA('What type of rectangle is ', get_rectangle_type),
            'What is digit n of fibonacci': QA('What is digit n of fibonacci',
                                               get_fibonacci_number),
            'What time is it': QA('What time is it', get_date_time),
            'What is digit of pi': QA('What is digit of pi', get_pi_digit),
            'How many inches is feet': QA('How many inches is feet', convert_feet_to_inches),
            'How many feet is inches': QA('How many feet is inches', convert_inches_to_feet),
            'How many gallons is liters': QA('How many gallons is liters',
                                             convert_liters_to_gallons),
            'How many liters is gallons': QA('How many liters is gallons',
                                             convert_gallons_to_liters),
            'How many teaspoons is cups': QA('How many teaspoons is cups',
                                             convert_cups_to_teaspons),
            'How many cups is teaspoons': QA('How many cups is teaspoons',
                                             convert_teaspoons_to_cups),
            'How many miles is km': QA('How many miles is km', convert_km_to_miles),
            'How many km is miles': QA('How many km is miles', convert_miles_to_km),
            'How many acres is square feet': QA('How many acres is square feet',
                                                convert_sqfeet_to_acres),
            'How many square feet is acres': QA('How many square feet is acres',
                                                convert_acres_to_sqfeet),
            'What is Jenny\'s number': QA('What is Jenny\'s number', "867-5309"),
            'Is divisible by ': QA('Is divisible by', get_is_divisible),
            'How many days until ': QA('How many days until', get_days_until_date),
            'What lottery numbers under should I play': QA(
                'What lottery numbers under should I play', get_lotto_numbers),
            'What is raised to the': QA('What is raised to the', get_exponent_result),
            'How old is someone born on': QA('How old is someone born on', get_age),
            'Is the in the repo': QA('Is the in the repo', is_file_in_repo),
            'What is the status of ': QA('What is the status of ', get_git_file_info),
            'What branch is ': QA('What branch is ', get_repo_branch),
            'Where did come from': QA('Where did come from', get_repo_url),
            'What is the deal with': QA('What is the deal with', get_file_info),
            'What is the hex code for': QA('What is the hex code for', get_rgb_hex)
        }

    def restore_questions(self):
        """Sets questions to values before they were last cleared"""
        self.question_answers = deepcopy(self.backup_questions)

    @staticmethod
    def write_to_file(message=""):
        """Writes a string to questionAnswerLog"""
        with open('questionAnswerLog.txt', 'a') as outfile:
            outfile.write(message + "\n")
            outfile.close()

    def parse_question(self, question):
        """Parses a question to remove args and question mark"""
        parsed_question = ""
        args = []
        for keyword in question[:-1].split(' '):
            try:
                args.append(float(keyword))
            except ValueError:
                if keyword[0] == "<" and keyword[-1] == ">":
                    args.append(keyword[1:-1])
                else:
                    parsed_question += "{0} ".format(keyword)
        parsed_question = parsed_question[0:-1]
        self.last_question = parsed_question
        self.write_to_file("Question: " + question)
        return args
