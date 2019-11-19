"""
Rewritten number guesser
See also argparse and sys.argv as a replacement for recieving arguments from CLI.
NOTE: This isn't the best way of writing this.
However consider it an introduction to classes, sets, enums, tuples, dicts, command line args.
"""
import os
from enum import Enum, auto
from random import randint, choice

import click


class ResponseType(Enum):
    GREATER_THAN_MAX_NUMBER = auto()
    LESS_THAN_ZERO = auto()
    CURRENT_GUESS_GREATER_THAN_ANSWER = auto()
    LOWER_THAN_ANSWER_REPEAT = auto()
    CURRENT_GUESS_LESS_THAN_ANSWER = auto()
    HIGHER_THAN_ANSWER_REPEAT = auto()
    REPEAT_ANSWER = auto()
    VICTORY = auto()


# Make sure we insult the user any time they are stupid
SILLY_RESPONSES = {
    ResponseType.LESS_THAN_ZERO,
    ResponseType.LOWER_THAN_ANSWER_REPEAT,
    ResponseType.HIGHER_THAN_ANSWER_REPEAT,
    ResponseType.GREATER_THAN_MAX_NUMBER,
    ResponseType.REPEAT_ANSWER
}

# Maximum number of guess and range limit user is allowed by default
MAX_GUESSES = 10
MAX_NUMBER_RANGE = 100
QUESTIONER = "Cam"
INSULTS_ADJS = (
    "stupid",
    "bloody",
    "forking",
    "waste of space",
    "fucking",
    "assing",
    "spursing"
)
INSULTS_NOUNS = (
    "donkey",
    "moron",
    "butt head",
    "shit for brains",
    "numbskull",
    "jabroni",
    "oxygen thief",
    "mouth breather"
)


def get_insult() -> str:
    """
    Create an insult for the user
    """
    return f"{choice(INSULTS_ADJS)} {choice(INSULTS_ADJS)} {choice(INSULTS_NOUNS)}"


class GuessingGame(object):
    """
    Main class for our simple guessing game
    """

    def __init__(self,
                 previous_count: int = 0,
                 name: str = "Idiot",
                 max_guesses: int = MAX_GUESSES,
                 max_number: int = MAX_NUMBER_RANGE,
                 answer: int = 0):
        self.previous_count = previous_count
        self.current_count = 0
        self.max_guesses = max_guesses
        self.answer = answer
        self.name = name
        self.maximum_number = max_number
        self.current_guess = None
        self.victory = False
        self.current_guess = None
        self.previous_guess = None
        self.keep_playing = True

    def get_response_type(self) -> ResponseType:
        """
        Provides response types based on state of game
        """
        previous_guess_higher_than_ans = self.answer < self.previous_guess if self.previous_guess is not None else False
        previous_guess_lower_than_ans = self.answer > self.previous_guess if self.previous_guess is not None else False
        current_guess_less_than_prev = self.current_guess < self.previous_guess if self.previous_guess is not None else False
        current_guess_greater_than_prev = self.current_guess > self.previous_guess if self.previous_guess is not None else False
        current_guess_less_than_answer = self.current_guess < self.answer
        current_guess_greater_answer = self.current_guess > self.answer
        if self.current_guess <= 0:
            return ResponseType.LESS_THAN_ZERO
        if self.current_guess == self.previous_guess:
            return ResponseType.REPEAT_ANSWER
        if self.current_guess > self.maximum_number:
            return ResponseType.GREATER_THAN_MAX_NUMBER
        if current_guess_less_than_answer and current_guess_less_than_prev and previous_guess_lower_than_ans:
            return ResponseType.LOWER_THAN_ANSWER_REPEAT
        if current_guess_greater_answer and current_guess_greater_than_prev and previous_guess_higher_than_ans:
            return ResponseType.HIGHER_THAN_ANSWER_REPEAT
        if current_guess_less_than_answer:
            return ResponseType.CURRENT_GUESS_GREATER_THAN_ANSWER
        if current_guess_greater_answer:
            return ResponseType.CURRENT_GUESS_LESS_THAN_ANSWER
        return ResponseType.VICTORY

    def response_generator(self) -> str:
        """
        Fetch a response type and generate a response based on it
        """
        prefix_response = f"{self.name}"
        responses = {
            ResponseType.LESS_THAN_ZERO: f"it has to be greater than zero",
            ResponseType.GREATER_THAN_MAX_NUMBER: f"it has to be less than {self.maximum_number}",
            ResponseType.LOWER_THAN_ANSWER_REPEAT: f"I already told you it was higher than {self.previous_guess}",
            ResponseType.HIGHER_THAN_ANSWER_REPEAT: f"I already told you it was lower than {self.previous_guess}",
            ResponseType.CURRENT_GUESS_GREATER_THAN_ANSWER: f"higher than {self.current_guess}",
            ResponseType.CURRENT_GUESS_LESS_THAN_ANSWER: f"lower than {self.current_guess}",
            ResponseType.REPEAT_ANSWER: f"I already told you !!!",
            ResponseType.VICTORY: ""
        }
        res_type = self.get_response_type()
        if res_type in SILLY_RESPONSES:
            prefix_response = f"{prefix_response} you {get_insult()}"
        return f"{prefix_response} {responses[res_type]}".title()

    def check_answer(self) -> (str, bool):
        """
        Logic for checking answers and providing status of game
        """
        return self.response_generator(), self.answer == self.current_guess

    def victory_message(self, guess_count) -> str:
        """
        If a user wins within maximum guesses provide a victory message
        :return: Message for winners
        """
        # TODO: Insert some extra responses based on guess_count divided by max_guesses
        click.secho(f"{self.name} bloody did it, however it would've only taken {QUESTIONER} {guess_count - 1} "
                    f"to guess correctly", color="green")

    def losing_message(self):
        """
        Provide a losing message if they couldn't guess it in time
        :return: Message for losers
        """
        return f"OMG {self.name} you had fucking {self.max_guesses} chances and you" \
            f" couldn't pick {self.answer} you {get_insult()}!!!"

    def run_game(self):
        """
        Main loop for running our game
        """
        while self.keep_playing:
            if self.previous_count:
                if self.previous_count < self.max_guesses:
                    click.secho("You done pretty well last time. Maybe not so lucky this time", color="green")
                else:
                    click.secho(f"Better luck this time you {get_insult()}", color="red")
            for guess_count in range(1, self.max_guesses):
                self.current_guess = click.prompt(f"Guess a number between 1 and {self.maximum_number}", type=int)
                response, correct_guess = self.check_answer()
                if correct_guess:
                    click.secho(self.victory_message(guess_count), color="green")
                    self.previous_count = guess_count
                    break
                click.secho(self.response_generator(), color="red")
                self.previous_guess = self.current_guess
            self.losing_message()
            self.keep_playing = click.confirm(f"Hey {self.name} you {get_insult()} would you like to keep playing")
        click.secho(f"Goodbye {self.name} you {get_insult()}")


@click.command()
@click.option('-g', '--max_guesses', default=MAX_GUESSES, help='Maximum number of guesses user is allowed')
@click.option('-n', '--name', prompt='Name of guesser',
              default=lambda: os.environ.get('USER', ''),
              required=True,
              help='The person doing the guessing.')
@click.option('-r', '--random_number',
              help='The random number the user will guess',
              default=randint(1, MAX_NUMBER_RANGE))
@click.option('-m', '--max_number',
              prompt='The random number will be between 1 and this number. Will overwrite random number if provided',
              help='maximum number range',
              default=MAX_NUMBER_RANGE)
def guessing_game(max_guesses, name, random_number, max_number):
    """Our simple guessing game on ROIDS"""
    if max_number:
        random_number = randint(1, max_number)
    game = GuessingGame(max_guesses=max_guesses,
                        answer=random_number,
                        max_number=max_number,
                        name=name)
    game.run_game()


if __name__ == '__main__':
    guessing_game()
