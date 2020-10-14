from pylint_quacking.quacking import Quacking


def register(linter):
    linter.register_checker(Quacking(linter))