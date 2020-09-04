from rpython.rlib.objectmodel import compute_hash

from som.primitives.primitives import Primitives
from som.vm.globals import trueObject, falseObject
from som.vm.universe import Universe
from som.vmobjects.primitive import Primitive, UnaryPrimitive, BinaryPrimitive, TernaryPrimitive
from som.vmobjects.string import String
from som.vmobjects.symbol import Symbol


def _concat(rcvr, argument):
    return String(rcvr.get_embedded_string() + argument.get_embedded_string())


def _as_symbol(ivkbl, frame, interpreter):
    rcvr = frame.pop()
    frame.push(interpreter.get_universe().symbol_for(rcvr.get_embedded_string()))


def _length(rcvr):
    return Universe.new_integer(len(rcvr.get_embedded_string()))


def _equals(op1, op2):
    if isinstance(op1, String):
        if isinstance(op1, Symbol) and isinstance(op2, Symbol):
            if op1 is op2:
                return trueObject
            else:
                return falseObject
        if isinstance(op2, String):
            if op1.get_embedded_string() == op2.get_embedded_string():
                return trueObject
    return falseObject


def _substring(rcvr, start, end):
    s      = start.get_embedded_integer() - 1
    e      = end.get_embedded_integer()
    string = rcvr.get_embedded_string()

    if s < 0 or s >= len(string) or e > len(string) or e < s:
        return String("Error - index out of bounds")
    else:
        return String(string[s:e])


def _hashcode(rcvr):
    return Universe.new_integer(compute_hash(rcvr.get_embedded_string()))


def _is_whitespace(self):
    s = self.get_embedded_string()

    for c in s:
        if not c.isspace():
            return falseObject

    if len(s) > 0:
        return trueObject
    else:
        return falseObject


def _is_letters(self):
    s = self.get_embedded_string()

    for c in s:
        if not c.isalpha():
            return falseObject

    if len(s) > 0:
        return trueObject
    else:
        return falseObject


def _is_digits(self):
    s = self.get_embedded_string()

    for c in s:
        if not c.isdigit():
            return falseObject

    if len(s) > 0:
        return trueObject
    else:
        return falseObject


class StringPrimitives(Primitives):

    def install_primitives(self):
        self._install_instance_primitive(BinaryPrimitive("concatenate:", self._universe, _concat))
        self._install_instance_primitive(Primitive("asSymbol",           self._universe, _as_symbol))
        self._install_instance_primitive(UnaryPrimitive("length",        self._universe, _length))
        self._install_instance_primitive(BinaryPrimitive("=",            self._universe, _equals))
        self._install_instance_primitive(TernaryPrimitive("primSubstringFrom:to:", self._universe, _substring))
        self._install_instance_primitive(UnaryPrimitive("hashcode",      self._universe, _hashcode))

        self._install_instance_primitive(UnaryPrimitive("isWhiteSpace", self._universe, _is_whitespace))
        self._install_instance_primitive(UnaryPrimitive("isLetters", self._universe, _is_letters))
        self._install_instance_primitive(UnaryPrimitive("isDigits", self._universe, _is_digits))
