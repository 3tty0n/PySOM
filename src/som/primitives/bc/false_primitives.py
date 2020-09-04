from som.primitives.primitives import Primitives
from som.vm.globals import trueObject, falseObject
from som.vmobjects.primitive import UnaryPrimitive, BinaryPrimitive


def _not(_rcvr):
    return trueObject


def _or(ivkbl, frame, interpreter):
    block = frame.pop()
    frame.pop()
    block_method = block.get_method()
    block_method.invoke(frame, interpreter)


def _and(_rcvr, _arg):
    return falseObject


class FalsePrimitives(Primitives):

    def install_primitives(self):
        self._install_instance_primitive(UnaryPrimitive("not", self._universe, _not))
        self._install_instance_primitive(BinaryPrimitive("and:", self._universe, _and))
        self._install_instance_primitive(BinaryPrimitive("&&", self._universe, _and))
        # self._install_instance_primitive(Primitive("or:", self._universe, _or))
        # self._install_instance_primitive(Primitive("||", self._universe, _or))
