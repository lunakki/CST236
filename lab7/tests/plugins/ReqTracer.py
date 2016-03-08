# pylint: disable=invalid-name
# nose doesn't seem to like renaming the module
"""
For annotating tests with requirements
Prints results to a file
"""
from nose2.events import Plugin


# pylint: disable=too-few-public-methods
# just using it as a struct type object
class RequirementTrace(object):
    """Holds info about a requirement"""

    req_text = ""

    def __init__(self, text):
        """Initialization"""
        self.req_text = text
        self.func_name = []

# pylint: disable=too-few-public-methods
# just using it as a struct type object
class JobStoryTrace(object):
    """Holds info about a job story"""
    def __init__(self):
        """Initalization"""
        self.func_name = []

# Pylint thinks these are constants but they aren't
# pylint: disable=invalid-name
Requirements = {}
# pylint: disable=invalid-name
JobStories = {}


def requirements(req_list):
    """To tag tests"""
    def wrapper(func):
        """To tag tests"""
        def add_req_and_call(*args, **kwargs):
            """Adds tagged test to an array to output later"""
            for req in req_list:
                if req not in Requirements.keys():
                    raise Exception('Requirement {0} not defined'.format(req))
                Requirements[req].func_name.append(func.__name__)
            return func(*args, **kwargs)

        return add_req_and_call

    return wrapper


def job_stories(story_list):
    """To tag tests"""
    def wrapper(func):
        """To tag tests"""
        def add_req_and_call(*args, **kwargs):
            """Adds tagged test to an array to output later"""
            for story in story_list:
                if story not in JobStories.keys():
                    raise Exception('Story {0} not defined'.format(story))
                JobStories[story].func_name.append(func.__name__)
            return func(*args, **kwargs)

        return add_req_and_call

    return wrapper

with open('ProjectRequirements.txt') as f:
    for line in f.readlines():
        if '#0' in line:
            req_id, desc = line.split(' ', 1)
            Requirements[req_id] = RequirementTrace(desc)
        elif '*' in line:
            dummy, jobStory = line.split(' ', 1)
            JobStories[jobStory] = JobStoryTrace()

# pylint: disable=no-init
# Don't need it
class PrintOut(Plugin):
    """Plugin to track requirements for each test"""
    configSection = 'req-tracer'

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    # I was told it had to be exactly like this to work
    def afterSummaryReport(self, event):
        """Logs tests associated with reqs to a file after tests complete"""
        with open('outputfile.txt', 'w') as outfile:
            for story in JobStories:
                outfile.write("\n" + story)
                for funct in JobStories[story].func_name:
                    outfile.write("\t" + funct + "\n")

            for req in Requirements:
                outfile.write("\n" + req + " " + Requirements[req].req_text)
                for funct in Requirements[req].func_name:
                    outfile.write("\t" + funct + "\n")
            outfile.close()
