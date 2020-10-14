import astroid
import pytest
import quacking
from pylint.testutils import UnittestLinter, Message
from pylint.interfaces import UNDEFINED


class DisablingUnittestLinter(UnittestLinter):
    def __init__(self, *args, **kwargs):
        self._disabled = set()
        super().__init__(*args, **kwargs)

    def is_message_enabled(self, key, *args, **kwargs):
        return key not in self._disabled

    def disable(self, key):
        self._disabled.add(key)

@pytest.fixture
def linter():
    return DisablingUnittestLinter()

@pytest.fixture
def checker(linter):
    return quacking.Quacking(linter)


def test_annotated_assignment(checker, linter):
    stmt = astroid.extract_node("""
    a: int = 2
    """)
    checker.visit_annassign(stmt)
    expected = Message("no-type-hints", node=stmt.annotation, args=('variable assignments',), confidence=UNDEFINED)
    assert expected in linter.release_messages()

def test_annotated_assignment_disabled(checker, linter):
    stmt = astroid.extract_node("""
    a: int = 2
    """)
    linter.disable("no-type-hints")
    checker.visit_annassign(stmt)
    assert not linter.release_messages()

def test_commented_assignment(checker, linter):
    stmt = astroid.extract_node("""
    b = 3  # type: int
    """)
    checker.visit_assign(stmt)
    expected = Message("no-type-hints", node=stmt.type_annotation, args=('variable assignments',), confidence=UNDEFINED)
    assert expected in linter.release_messages()

def test_commented_assignment_disabled(checker, linter):
    stmt = astroid.extract_node("""
    b = 3  # type: int
    """)
    linter.disable("no-type-hints")
    checker.visit_assign(stmt)
    assert not linter.release_messages()

def test_function_return(checker, linter):
    stmt = astroid.extract_node("""
def foo(bar: int, quux: int=3) -> int:
    pass
""")
    checker.visit_functiondef(stmt)
    expected = Message("no-type-hints", node=stmt.returns, args=('function signatures',), confidence=UNDEFINED)
    assert expected in linter.release_messages()

def test_function_return_disabled(checker, linter):
    stmt = astroid.extract_node("""
def foo(bar: int, quux: int=3) -> int:
    pass
""")
    linter.disable("no-type-hints")
    checker.visit_functiondef(stmt)
    assert not linter.release_messages()

def test_function_arguments(checker, linter):
    stmt = astroid.extract_node("""
def foo(bar: int, quux: int=3, *args: 'List[int]', **kwargs: 'Dict[str, int]') -> int:
    pass
""")
    checker.visit_arguments(stmt.args)
    expected = Message("no-type-hints", node=stmt.args.annotations[0], args=('function signatures',), confidence=UNDEFINED)
    expected = Message("no-type-hints", node=stmt.args.annotations[1], args=('function signatures',), confidence=UNDEFINED)
    assert expected in linter.release_messages()

def test_function_arguments_disabled(checker, linter):
    stmt = astroid.extract_node("""
def foo(bar: int, quux: int=3, *args: 'List[int]') -> int:
    pass
""")
    linter.disable("no-type-hints")
    checker.visit_arguments(stmt.args)
    assert not linter.release_messages()

def bar(quux, flubber):
    pass
