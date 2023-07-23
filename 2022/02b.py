import fileinput


def translate(letter):
    if letter.lower() in ["a", "x"]:
        return "Rock"
    if letter.lower() in ["b", "y"]:
        return "Paper"
    if letter.lower() in ["c", "z"]:
        return "Scissors"


def shape_value(shape):
    shape = translate(shape)
    if shape == "Rock":
        return 1
    if shape == "Paper":
        return 2
    if shape == "Scissors":
        return 3


def outcome_value(outcome):
    if outcome == "lost":
        return 0
    if outcome == "draw":
        return 3
    if outcome == "won":
        return 6


def evaluate_play(p1, p2):
    """Evaluate play according to player 1"""
    tp1 = translate(p1)
    tp2 = translate(p2)
    if (
        tp1 == "Rock"
        and tp2 == "Scissors"
        or tp1 == "Scissors"
        and tp2 == "Paper"
        or tp1 == "Paper"
        and tp2 == "Rock"
    ):
        return "won"
    if tp1 == tp2:
        return "draw"
    return "lost"


def play_for(other, outcome):
    """Calculate your play in order to get an outcome given the other players play"""
    plays = "XYZ"
    for play in plays:
        if evaluate_play(play, other) == outcome:
            return play


def translate_outcome(outcome):
    if outcome.lower() == "x":
        return "lost"
    if outcome.lower() == "y":
        return "draw"
    if outcome.lower() == "z":
        return "won"


def main():
    score = 0
    for line in fileinput.input():
        [other, outcome] = line.split()
        outcome = translate_outcome(outcome)
        you = play_for(other, outcome)
        score += outcome_value(outcome) + shape_value(you)
    print(score)


if __name__ == "__main__":
    main()
