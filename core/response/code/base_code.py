from enum import Enum


class BaseCode(Enum):
    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]

    @property
    def category(self):
        return self.value[2]