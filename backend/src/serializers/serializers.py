import uuid


class UUIDSerializer:
    __slots__ = ('uuid_representation', 'uuid_internal')

    def __init__(self, value):
        if isinstance(value, uuid.UUID):
            self.uuid_internal = value
            self.uuid_representation = None
        else:
            self.uuid_representation = value
            self.uuid_internal = None

    def to_internal_value(self) -> uuid.UUID:
        uuid_internal = [i for i in self.uuid_representation]
        _ = [uuid_internal.insert(i, '-') for i in (8, 13, 18, 30)]
        uuid_internal = ''.join(uuid_internal)
        self.uuid_internal = uuid.UUID(uuid_internal)
        return self.uuid_internal

    def to_representation(self) -> str:
        string_uuid = str(self.uuid_internal)
        self.uuid_representation = string_uuid.replace('-', '')
        return self.uuid_representation
