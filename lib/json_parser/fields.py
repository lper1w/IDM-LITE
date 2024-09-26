from typing import Any


class Field:
    def __init__(self, field_type):
        self.field_type = field_type


class IntField(Field):
    def __init__(self):
        super().__init__(int)


class StrField(Field):
    def __init__(self):
        super().__init__(str)


class BoolField(Field):
    def __init__(self):
        super().__init__(bool)


class JsonField(Field):
    def __init__(self):
        super().__init__(dict[str, Any])


class ListField(Field):
    def __init__(self, field_type):
        super().__init__(list[field_type])
