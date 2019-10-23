"""
If you are looking at this without doing the test,
it will provide you with the answers.
Cheating is fine by me, it is the easiest way to get the answers of course.
But points mean nothing so proceed with caution.
"""
from collections import namedtuple
import sys

if sys.version_info.major == 2:
    get_input = raw_input
else:
    get_input = input
Line = namedtuple('Line', ['line_no', 'line', 'length'])

FILE_TO_CONV = "fresh_prince.txt"
# Record line number and line

import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = get_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


lines = []
with open(FILE_TO_CONV, "r") as fp:
    for line_no, line in enumerate(fp.readlines()):
        line = line.rstrip("\n")
        lines.append(Line(line_no+1, line, len(line)))

by_line_length = sorted([_ for _ in lines], key=lambda l: l.length, reverse=True)

first_three = [_.line for _ in lines[:3]]

question = {
    "1": {"question": "Begin by downloading the file (fresh_prince.txt)?",
          "answer": "I would be using curl or wget, but you could also use the library httpie it's pretty neat"
          },
    "2": {"question": "Can you extract the first three lines from fresh_prince.txt?",
          "answer": "\n".join(first_three),
          "explanation": "The most simple command would be to use `head -n 3 fresh_prince.txt` , "
                         "but you could also used `sed -n 1,3p fresh_prince.txt`, or "
                         " `awk 'FNR <= 3' fresh_prince.txt` ."},
    "3": {"question": "Can you print all the lines in the text to the terminal?",
          "answer": "\n ... \n".join(["\n".join([_.line for _ in lines[:3]]),
                                      "\n".join([_.line for _ in lines[-3:]])]),
          "explanation": "This is easy just use cat or less, you could go crazy and use awk I guess"},
    "4": {"question": "How many lines are in file that aren't empty?",
          "answer": len([_ for _ in lines if _.length]),
          "explanation": "The command to count lines is wc -l, however to exclude the blank spaces use grep or egrep"
                         r"`grep -c -v '^$'  fresh_prince.txt` or `egrep '\w' fresh_prince.txt | wc -l `"},

    "5": {"question": "Can you find the longest line in the file fresh_prince.txt, what is the text of that line?",
          "answer": by_line_length[0].line,
          "explanation": "This is quite hard I don't actually expect you to use  awk all that much."
                         " `awk ' { if ( length > x ) { x = length } }END{ print x }' fresh_prince.txt` or "
                         " `cat fresh_prince.txt |awk '{print length, NR, $0}'|sort -nr | cut -d' ' -f 1 | head -n1` "},
    "6": {"question": "What is the position (line number) of the line from question 5?",
          "answer": by_line_length[0].line_no,
          "explanation": "These commands are quite long without wc -L aren't they ? "
                         "Anyway I would use "
                         "`cat fresh_prince.txt |awk '{print length, NR, $0}'|sort -nr | cut -d' ' -f 2 | head -n 1`"},
    "7": {"question": "How long is the line from question 5?",
          "explanation": "The easiest way would be to use wc -L. However the wc program differs on mac to that on unix."
                         "Therefore we would use something like "
                         "`cat fresh_prince.txt |awk '{print length, NR, $0}'|sort -nr | cut -d' ' -f 1 | head -n1`",
          "answer": by_line_length[0].length},
    "8": {"question": 'Run the command `echo "echo Hello World" > hw.sh`, how would make this an executable?',
          "answer": "Easy yo, `chmod +x hw.sh`."},
    "9": {"question": "Can you make the script print out `Hello Michael` with out changing the contents of the file?",
          "answer": "If you have made the file executable ./hw.sh | sed 's/World/Michael/', "
                    "if you haven't (sh hw.sh | sed 's/World/Michael/')"},
    "10": {"question": "Excluding whitespace, what is the most common start of each line in "
                       "the fresh_prince.txt file and how many times does it appear?",
           "explanation": "I used "
                          r"`cut -d ' ' -f 1 fresh_prince.txt | egrep '\w' |  sort -nr |  uniq -c | sort -nr | head -n 1` "
                          "`egrep` is there solely to exclude whitespace, you could use awk or sed though."
           },
    "11": {"question": "What does it `Secure Shell` mean and how would you go about doing it on a server?",
           "answer":"Assuming your id_rsa file exists on a server ssh username@ip_address. ",
            "explanation": "Secure Shell or ssh is a way of logging into a remote server and something we will be using quite a bit"}
}

for i, values in sorted(question.items(), key=lambda x: int(x[0])):
    print("\n{i}) {q}".format(i=i, q=values['question']))
    query_yes_no("See Answer?")
    if 'answer' in values:
        print("\n{a}".format(a=values['answer']))
    if 'explanation' in values:
        print("\n{e}".format(e=values['explanation']))
