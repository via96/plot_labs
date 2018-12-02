from enum import Enum

class E(Enum):
    FIRST = 'V'
    SECOND = 'I'
    THIRD = 'R'

    @staticmethod
    def contains(val):
        return val in [item.value for item in E]


if E.contains('V'):
    print("YEs")
else:
    print("NO")