import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class Quacking(BaseChecker):
    """Ensure there are no PEP 484 type hints"""

    # This class variable defines the type of checker that we are implementing.
    # In this case, we are implementing an AST checker.
    __implements__ = IAstroidChecker

    # The name defines a custom section of the config for this checker.
    name = "quacking"
    # The priority indicates the order that pylint will run the checkers.
    priority = -1
    # This class variable declares the messages (ie the warnings and errors)
    # that the checker can emit.
    msgs = {
        # Each message has a code, a message that the user will see,
        # a unique symbol that identifies the message,
        # and a detailed help message
        # that will be included in the documentation.
        "E3107": ("\U0001F986 Type hints are banned in %s \U0001F986", "no-type-hints", "Type hints are banned, walk like a duck")
    }
    options = ()

    def visit_arguments(self, node):
        """Called when a :class:`.astroid.node_classes.Arguments` node is visited.
        See :mod:`astroid` for the description of available nodes.
        :param node: The node to check.
        :type node: astroid.node_classes.Call
        """
        if not self.linter.is_message_enabled("no-type-hints", node.fromlineno):
            return
        for annotation in node.annotations:
            if annotation is not None:
                self.add_message("no-type-hints", node=annotation, args=("function signatures",))
        if node.kwargannotation is not None:
            self.add_message("no-type-hints", node=node.kwargannotation, args=("function signatures",))
        if node.varargannotation is not None:
            self.add_message("no-type-hints", node=node.varargannotation, args=("function signatures",))

    def visit_annassign(self, node):
        "ensure variable assignments don't have annotations"
        if not self.linter.is_message_enabled("no-type-hints", node.fromlineno):
            return
        if node.annotation is not None:
            self.add_message("no-type-hints", node=node.annotation, args=("variable assignments",))

    def visit_assign(self, node):
        "ensure variable assignments don't have annotations"
        if not self.linter.is_message_enabled("no-type-hints", node.fromlineno):
            return
        if node.type_annotation is not None:
            self.add_message("no-type-hints", node=node.type_annotation, args=("variable assignments",))

    def visit_functiondef(self, node):
        "ensure functions don't have annotations"
        if not self.linter.is_message_enabled("no-type-hints", node.fromlineno):
            return
        if node.returns is not None:
            self.add_message("no-type-hints", node=node.returns, args=("function signatures",))

    visit_asyncfunctiondef = visit_functiondef
