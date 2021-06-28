from rlib import jit

from som.vmobjects.abstract_object import AbstractObject
from som.vmobjects.primitive import Primitive
from som.interpreter.bc.frame import create_frame, copy_arguments_from


class BcBlock(AbstractObject):

    _immutable_fields_ = ["_method", "_context"]

    def __init__(self, method, context):
        AbstractObject.__init__(self)
        self._method = method
        self._context = context

    def get_method(self):
        return jit.promote(self._method)

    def get_context(self):
        return self._context

    def get_class(self, universe):
        return universe.block_classes[self._method.get_number_of_arguments()]

    class Evaluation(Primitive):

        _immutable_fields_ = ["_number_of_arguments"]

        def __init__(self, num_args, universe, invoke):
            Primitive.__init__(
                self, self._compute_signature_string(num_args), universe, invoke
            )
            self._number_of_arguments = num_args

        @staticmethod
        def _compute_signature_string(num_args):
            # Compute the signature string
            signature_string = "value"
            if num_args > 1:
                signature_string += ":"
                if num_args > 2:
                    # Add extra with: selector elements if necessary
                    signature_string += "with:" * (num_args - 2)

            # Return the signature string
            return signature_string


def block_evaluation_primitive(num_args, universe):
    return BcBlock.Evaluation(num_args, universe, _invoke)


def block_evaluate(block, frame):
    from som.interpreter.bc.interpreter import interpret

    context = block.get_context()
    method = block.get_method()
    new_frame = create_frame(
        copy_arguments_from(frame, method.get_number_of_arguments()),
        method,
        context,
    )

    try:
        result = interpret(method, new_frame)
        frame.pop_old_arguments_and_push_result(method, result)
    finally:
        new_frame.get_on_stack_marker().mark_as_no_longer_on_stack()


def _invoke(ivkbl, frame):
    assert isinstance(ivkbl, BcBlock.Evaluation)
    rcvr = frame.get_stack_element(ivkbl._number_of_arguments - 1)  # pylint: disable=W
    block_evaluate(rcvr, frame)
