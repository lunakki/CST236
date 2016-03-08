"""
Test for source.main
"""
import time
import getpass
import datetime
import os
from unittest import TestCase
import mock
from tests.plugins.ReqTracer import requirements, job_stories
from source.main import Interface
from source.git_utils import get_git_file_info, get_repo_root, has_untracked_files

# pylint: disable=too-many-public-methods
# it probably is too many but I can't think of a logical way to split them up
class TestQuestionTypes(TestCase):
    """Tests the program that lets you ask questions"""
    qa_inst = Interface()

    @requirements(['#0017'])
    def test_teach_no_question(self):
        """Tests trying to teach when no question was asked"""
        qa_inst = Interface()
        result = Interface.teach(qa_inst, "Julie")
        self.assertEquals(result, "Please ask a question first")

    @requirements(['#0021'])
    def test_correct_no_question(self):
        """Tests trying to correct when no question was asked"""
        qa_inst = Interface()
        result = Interface.correct(qa_inst, "Julie")
        self.assertEquals(result, "Please ask a question first")

    @requirements(['#0007'])
    def test_ask_who(self):
        """Tests asking a question starting with 'who'"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Who am I?")
        self.assertNotEquals(result, 'Was that a question?')
        self.assertNotEquals(result, 'Please ask a question first')
        self.assertNotEquals(result, 'I don\'t know about that. I was taught differently')

    @requirements(['#0007'])
    def test_ask_what(self):
        """Tests asking a question starting with 'what'"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What am I?")
        self.assertNotEquals(result, 'Was that a question?')
        self.assertNotEquals(result, 'Please ask a question first')
        self.assertNotEquals(result, 'I don\'t know about that. I was taught differently')

    @requirements(['#0007'])
    def test_ask_how(self):
        """Tests asking a question starting with 'how'"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "How are you?")
        self.assertNotEquals(result, 'Was that a question?')
        self.assertNotEquals(result, 'Please ask a question first')
        self.assertNotEquals(result, 'I don\'t know about that. I was taught differently')

    @requirements(['#0007', '#0050'])
    def test_ask_why(self):
        """Ask a question starting with 'why'; also tests logging question with no answer"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Why is the sky blue?")
        self.assertNotEquals(result, 'Was that a question?')
        self.assertNotEquals(result, 'Please ask a question first')
        self.assertNotEquals(result, 'I don\'t know about that. I was taught differently')

        with open('questionAnswerLog.txt') as outfile:
            for line in outfile.readlines():
                last_line = line

        self.assertEquals(last_line, "Question: Why is the sky blue?\n")

    @requirements(['#0007'])
    def test_ask_where(self):
        """Tests asking a question starting with 'where'"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Where am I?")
        self.assertNotEquals(result, 'Was that a question?')
        self.assertNotEquals(result, 'Please ask a question first')
        self.assertNotEquals(result, 'I don\'t know about that. I was taught differently')

    @requirements(['#0008'])
    def test_no_keyword(self):
        """Ask a question with no indicator keyword"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "The sky is blue?")
        self.assertEquals(result, 'Was that a question?')

    @requirements(['#0009'])
    def test_no_question_mark(self):
        """Ask a question with no question mark"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Who am I")
        self.assertEquals(result, 'Was that a question?')

    @requirements(['#0006', '#0013', '#0050', '#0051', '#0052'])
    def test_match(self):
        """Test asking about a triangle with perfect match and logging reqs"""
        start = time.clock()
        result = Interface.ask(TestQuestionTypes.qa_inst, "What type of triangle is 1 1 1?")
        end = time.clock()
        self.assertEquals(result, 'equilateral')
        self.assertLess(end-start, 50)

        last_line = ""
        penultimate_line = ""
        with open('questionAnswerLog.txt') as out_file:
            for line in out_file.readlines():
                penultimate_line = last_line
                last_line = line

        self.assertEquals(last_line, "Answer: equilateral\n")
        self.assertEquals(penultimate_line, "Question: What type of triangle is 1 1 1?\n")

    @requirements(['#0011'])
    def test_keywords_near_match(self):
        """Keywords close to a match"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What typ of triangle i 1 1 1?")
        self.assertEquals(result, 'equilateral')

    @requirements(['#0011'])
    def test_keywords_not_near_enough(self):
        """Keywords not quite close enough to a match"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What typ of tiagle i 1 1 1?")
        self.assertEquals(result, "I don't know, please provide the answer")

    @requirements(['#0010'])
    def test_different_spaces(self):
        """No space after indicator keyword"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Whattype of triangle is 1 1 1?")
        self.assertEquals(result, "Was that a question?")

    @requirements(['#0012'])
    def test_numbers(self):
        """Test that numbers will be pulled from anywhere in the question"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What 1 type 1 of triangle 1 is?")
        self.assertEquals(result, "equilateral")

    @requirements(['#0014'])
    def test_no_match(self):
        """Test there being no match to the question"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is the meaning of life?")
        self.assertEquals(result, "I don't know, please provide the answer")

    @requirements(['#0015', '#0016', '#0020'])
    def test_teach(self):
        """Test teaching an answer to a question"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Who am I?")
        self.assertEquals(result, "I don't know, please provide the answer")
        result = Interface.teach(TestQuestionTypes.qa_inst, "Kat")
        self.assertEqual(result, None)
        result = Interface.ask(TestQuestionTypes.qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")

    @requirements(['#0018'])
    def test_teach_ask_again(self):
        """Test trying to teach an existing question"""
        qa_inst = Interface()
        Interface.ask(qa_inst, "Who am I?")
        Interface.teach(qa_inst, "Kat")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")
        result = Interface.teach(qa_inst, "Julie")
        self.assertEquals(result, "I don't know about that. I was taught differently")

    @requirements(['#0019'])
    def test_correct(self):
        """Text correcting an existing question"""
        qa_inst = Interface()
        Interface.ask(qa_inst, "Who am I?")
        Interface.teach(qa_inst, "Kat")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")
        Interface.correct(qa_inst, "Julie")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Julie")

    @job_stories(["When I ask 'What is digit n of fibonacci?' I want to receive the answer so "
                  "I don't have to figure it out myself\n"])
    def test_fibonacci_first(self):
        """Get a fibonacci number"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "What is digit 1 of fibonacci?")
        self.assertEqual(result, "0")

    @job_stories(["When I ask 'What is digit n of fibonacci?' I want to receive the answer so I "
                  "don't have to figure it out myself\n"])
    @requirements(['#0053'])
    def test_fibonacci_fifth(self):
        """Get a bigger fibonacci number. Also test performance."""
        qa_inst = Interface()
        start = time.clock()
        result = Interface.ask(qa_inst, "What is digit 25 of fibonacci?")
        end = time.clock()
        self.assertEqual(result, "46368")
        self.assertLess(end-start, 50)

    @job_stories(["When I ask 'What time is it?' I want to be given the current date and time "
                  "so I can stay up to date\n"])
    @requirements(["#0055"])
    def test_fibonacci_second(self):
        """Get the time/date"""
        qa_inst = Interface()
        start = time.clock()
        result = Interface.ask(qa_inst, "What time is it?")
        end = time.clock()
        self.assertEqual(result, time.strftime("%d/%m/%Y %H:%M"))
        self.assertLess(end-start, 50)

    @job_stories(["When I ask 'What is digit n of pi?' I want to receive the answer so I don't"
                  " have to figure it out myself\n"])
    def test_pi_first(self):
        """Get a digit of pi"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "What is digit 1 of pi?")
        self.assertEqual(result, "1")

    @job_stories(["When I ask 'What is digit n of pi?' I want to receive the answer so I don't "
                  "have to figure it out myself\n"])
    @requirements(["#0054"])
    def test_pi_1000(self):
        """Get a large digit of pi. Also test performance."""
        qa_inst = Interface()
        start = time.clock()
        result = Interface.ask(qa_inst, "What is digit 1000 of pi?")
        end = time.clock()
        self.assertEqual(result, "9")
        self.assertLess(end-start, 50)

    @job_stories(["When I say 'Open the door hal', I want the application to say 'I'm afraid I"
                  " can't do that <user name>' so I know that is not an option\n"])
    def test_open_door_hal(self):
        """Testing response to 'open the door hal'"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "Open the door hal")
        self.assertEqual(result, "I'm afraid I can't do that " + getpass.getuser())

    @job_stories(["When I ask 'Please clear memory' I was the application to clear user set "
                  "questions and answers so I can reset the application\n"])
    def test_clear_memory(self):
        """Clear saved questions"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "I don't know, please provide the answer")
        Interface.teach(qa_inst, "Kat")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")
        Interface.ask(qa_inst, "Please clear memory")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "I don't know, please provide the answer")

    @job_stories(["When I ask 'How many <units> is <number> <units>?' I want to receive the"
                  " converted value and units so I can know the answer\n",
                  "When I ask for a numeric conversion I want at least 10 different units I "
                  "can convert from/to\n"])
    def test_convert_feet_inches(self):
        """Conversion test"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "How many inches is 12 feet?")
        self.assertEquals(result, "144.00 inches")
        result = Interface.ask(qa_inst, "How many feet is 30 inches?")
        self.assertEquals(result, "2.50 feet")

    @job_stories(["When I ask 'How many <units> is <number> <units>?' I want to receive the"
                  " converted value and units so I can know the answer\n",
                  "When I ask for a numeric conversion I want at least 10 different units I"
                  " can convert from/to\n"])
    def test_convert_liters_gallons(self):
        """Conversion test"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "How many liters is 5 gallons?")
        self.assertEquals(result, "18.93 liters")
        result = Interface.ask(qa_inst, "How many gallons is 5 liters?")
        self.assertEquals(result, "1.32 gallons")

    @job_stories(["When I ask 'How many <units> is <number> <units>?' I want to receive the"
                  " converted value and units so I can know the answer\n",
                  "When I ask for a numeric conversion I want at least 10 different units I"
                  " can convert from/to\n"])
    def test_convert_teaspoons_cups(self):
        """Conversion test"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "How many teaspoons is 2 cups?")
        self.assertEquals(result, "96.00 teaspoons")
        result = Interface.ask(qa_inst, "How many cups is 100 teaspoons?")
        self.assertEquals(result, "2.08 cups")

    @job_stories(["When I ask 'How many <units> is <number> <units>?' I want to receive the "
                  "converted value and units so I can know the answer\n",
                  "When I ask for a numeric conversion I want at least 10 different units I "
                  "can convert from/to\n"])
    def test_convert_miles_km(self):
        """Conversion test"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "How many miles is 10 km?")
        self.assertEquals(result, "6.21 miles")
        result = Interface.ask(qa_inst, "How many km is 100 miles?")
        self.assertEquals(result, "160.93 km")

    @job_stories(["When I ask 'How many <units> is <number> <units>?' I want to receive the "
                  "converted value and units so I can know the answer\n",
                  "When I ask for a numeric conversion I want at least 10 different units I "
                  "can convert from/to\n"])
    def test_convert_acres_sq_feet(self):
        """Conversion test"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "How many acres is 100000 square feet?")
        self.assertEquals(result, "2.30 acres")
        result = Interface.ask(qa_inst, "How many square feet is 2 acres?")
        self.assertEquals(result, "87120.00 square feet")

    @job_stories(["When I ask 'What type of rectangle is n n n n' I want to receive the "
                  "answer so I can finish my homework faster\n"])
    def test_ask_rectangle(self):
        """Ask about a rectangle"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What type of rectangle is 1 1 1 1?")
        self.assertEquals(result, 'square')

    @job_stories(["When I ask 'What is Jenny's number?' I want to be given her number so I "
                  "can call her\n"])
    def test_ask_jenny_number(self):
        """Ask for Jenny's number"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is Jenny's number?")
        self.assertEquals(result, '867-5309')

    @job_stories(["When I ask 'What is the hex code for <color>?' I want to be given the hex "
                  "code so I can use it in my graphics program\n",
                  "When I ask for a color hex code I want to have at least 15 colors I can "
                  "choose\n"])
    @requirements(["#0056"])
    def test_ask_colors(self):
        """Ask for all possible hex code values; also test performance"""
        colors = ["<red>", "<blue>", "<green>", "<darkred>", "<darkblue>", "<darkgreen>",
                  "<yellow>", "<pink>", "<purple>", "<cyan>", "<orange>", "<white>", "<black>",
                  "<lightgrey>", "<grey>"]
        hex_codes = ["#FF0000", "#0000FF", "#00FF00", "#990000", "#000088", "#008800", "#FFFF00",
                     "#FF0088", "#880088", "#00FFFF", "#FF8800", "#FFFFFF", "#000000", "#DDDDDD",
                     "#888888"]

        i = 0
        while i < len(colors):
            start = time.clock()
            result = Interface.ask(TestQuestionTypes.qa_inst, "What is the hex code for " +
                                   colors[i] + "?")
            end = time.clock()
            self.assertEquals(result, hex_codes[i])
            self.assertLess(end-start, 50)
            i += 1

    @job_stories(["When I ask 'Please restore memory' I want the application to restore user set "
                  "questions so I can recover questions after clearing\n"])
    def test_reset_questions(self):
        """Restore memory after clearing"""
        qa_inst = Interface()
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "I don't know, please provide the answer")
        Interface.teach(qa_inst, "Kat")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")
        Interface.ask(qa_inst, "Please clear memory")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "I don't know, please provide the answer")
        Interface.ask(qa_inst, "Please restore memory")
        result = Interface.ask(qa_inst, "Who am I?")
        self.assertEquals(result, "Kat")

    @requirements(["#0022"])
    def test_bad_question(self):
        """Ask a question with no letters"""
        try:
            Interface.ask(TestQuestionTypes.qa_inst, 10998)
            # pylint: disable=broad-except
            # this is the exception it throws
        except Exception as except_str:
            self.assertEquals(str(except_str), 'Not A String!')

    @requirements(["#0023"])
    def test_too_many_params(self):
        """Give too many paramaters for the question"""
        try:
            Interface.ask(TestQuestionTypes.qa_inst, "What is digit 1 2 54 of fibonacci?")
            # pylint: disable=broad-except
            # this is the exception it throws
        except Exception as except_str:
            self.assertEquals(str(except_str), 'Too many extra parameters')

    @job_stories(["When I ask 'Is n divisible by n?' I want to receive the answer so I don't have"
                  " to figure it out myself\n"])
    def test_divisible_no(self):
        """Check if a number is not divisible"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Is 6 divisible by 5?")
        self.assertEquals(result, 'No')

    @job_stories(["When I ask 'Is n divisible by n?' I want to receive the answer so I don't have"
                  " to figure it out myself\n"])
    def test_divisible_yes(self):
        """Check if a number IS divisible"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "Is 6 divisible by 3?")
        self.assertEquals(result, 'Yes')

    @job_stories(["When I ask 'How old is someone born on <month> <day> <year>?' I want to receive"
                  " the answer so I don't have to figure it out myself\n"])
    def test_ask_age(self):
        """Get someone's age"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "How old is someone born on 06 06 1988?")
        self.assertEquals(result, '27')

    @job_stories(["When I ask 'How many days until <month> <day>?' I want to receive the answer so"
                  " I don't have to figure it out myself\n"])
    def test_ask_days_until_date(self):
        """Get days until a date"""
        date = datetime.date.today() + datetime.timedelta(days=60)
        result = Interface.ask(TestQuestionTypes.qa_inst, "How many days until " +
                               date.strftime("%m %d") + "?")
        self.assertEquals(result, "60")

    @job_stories(["When I ask 'How many days until <month> <day>?' I want to receive the answer"
                  " so I don't have to figure it out myself\n"])
    def test_ask_days_until_date_2(self):
        """Get days until a date before today"""
        date = datetime.date.today() + datetime.timedelta(days=363)
        result = Interface.ask(TestQuestionTypes.qa_inst, "How many days until " +
                               date.strftime("%m %d") + "?")
        self.assertEquals(result, "363")

    @job_stories(["When I ask 'What lottery numbers under <limit> should I play?' I want to"
                  " receive the answer so I can win the lottery\n"])
    @requirements(["#0057"])
    def test_lotto(self):
        """Get lotto numbers"""
        start = time.clock()
        result = Interface.ask(TestQuestionTypes.qa_inst, "What lottery numbers under 65 should I "
                                                          "play?")
        end = time.clock()
        result = result.split()
        count = 0
        for num in result:
            self.assertGreater(int(num), 0)
            self.assertLessEqual(int(num), 65)
            count += 1

        self.assertEqual(count, 5)
        self.assertLess(end-start, 50)

    @job_stories(["When I ask 'What is n raised to the n?' I want to receive the answer so I don't "
                  "have to figure it out myself\n"])
    def test_exponent(self):
        """Get some numbers raised to other numbers"""
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is 2 raised to the 3?")
        self.assertEquals(result, '8')
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is 2 raised to the 0?")
        self.assertEquals(result, '1')

    @requirements(['#0100'])
    @mock.patch('subprocess.Popen')
    def test_in_repo(self, mock_func):
        """Check for file in repo"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "Is the <requirements.txt> in the repo?")
        self.assertEquals(result, "Yes")


    @requirements(['#0100'])
    @mock.patch('subprocess.Popen')
    def test_in_repo_doesnt_exist(self, mock_func):
        """Check for file that doesn't exist"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "Is the <.\\source\\ajsdlkasjdl> in the "
                                                          "repo?")
        self.assertEquals(result, "No")

    @requirements(['#0100'])
    @mock.patch('subprocess.Popen')
    def test_exception(self, mock_func):
        """Check for an error"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('', 1)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        self.assertRaises(Exception, TestQuestionTypes.qa_inst.ask,
                          "Is the <.\\source\\__init__.pyc> in the repo?")

    @requirements(['#0100'])
    @mock.patch('subprocess.Popen')
    def test_not_tracked(self, mock_func):
        """Check for a file not tracked"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (os.path.abspath('.\\source\\__init__.pyc'), 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "Is the <.\\source\\__init__.pyc> in "
                                                          "the repo?")
        self.assertEquals(result, "No")


    @requirements(['#0101'])
    def test_invalid_path(self):
        """Ask about status of invalid path"""
        self.assertRaises(Exception, TestQuestionTypes.qa_inst.ask, "What is the status "
                                                                    "of <blah>?")

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def test_modified_file(self, mock_func):
        """Get status of modified file"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (os.path.abspath('requirements.txt'), 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is the status of "
                                                          "<requirements.txt>?")
        self.assertEquals(result, "requirements.txt has been modified locally")

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def test_file_dirty(self, mock_func):
        """Get status of file in dirty repo"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('aFile', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is the status of <nose2.cfg>?")
        self.assertEquals(result, "nose2.cfg is a dirty repo")

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def test_file_up_to_date(self, mock_func):
        """Get status of file that's up to date"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is the status of <nose2.cfg>?")
        self.assertEquals(result, "nose2.cfg is up to date")

    @requirements(['#0103'])
    @mock.patch('subprocess.Popen')
    def test_get_branch(self, mock_func):
        """Get the name of a branch"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('BranchName', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "What branch is <nose2.cfg>?")
        self.assertEquals(result, "BranchName")

    @requirements(['#0104'])
    @mock.patch('subprocess.Popen')
    def test_get_url(self, mock_func):
        """Get the URL of a repo"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('RepoURL', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "Where did <nose2.cfg> come from?")
        self.assertEquals(result, "RepoURL")

    @requirements(['#0102'])
    @mock.patch('subprocess.Popen')
    def test_get_file_info(self, mock_func):
        """Get info about a file"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('1234, 03-5-2016, Kat Valentine', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = Interface.ask(TestQuestionTypes.qa_inst, "What is the deal with <nose2.cfg>?")
        self.assertEquals(result, "1234, 03-5-2016, Kat Valentine")

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def test_get_repo_root(self, mock_func):
        """Get root of a repo"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (os.path.abspath('.\\source\\__init__.pyc'), 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = get_repo_root(".\\source\\__init__.py")
        self.assertEquals(result, os.path.abspath('.\\source\\__init__.pyc'))

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def broken_test_file_not_checked_in(self, mock_func):
        """Ask about file not checked in"""
        process_mock = mock.Mock()
        attrs = {'communicate.side_effect': [(os.path.abspath('requirements.txt'), 0),
                                             (os.path.abspath('requirements.txt'), 0),
                                             (os.path.abspath('nose2.cfg'), 0),
                                             (os.path.abspath('nose2.cfg'), 0)]}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = get_git_file_info("nose2.cfg")
        # result = Interface.ask(TestQuestionTypes.qa_inst, "What is the status of <nose2.cfg>?")
        self.assertEquals(result, "nose2.cfg is not checked in")

    @requirements(['#0101'])
    @mock.patch('subprocess.Popen')
    def test_file_untracked(self, mock_func):
        """Ask about untracked file"""
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': ('aFile', 0)}
        process_mock.configure_mock(**attrs)
        mock_func.return_value = process_mock
        result = has_untracked_files(".\\source\\__init__.py")
        self.assertTrue(result)
