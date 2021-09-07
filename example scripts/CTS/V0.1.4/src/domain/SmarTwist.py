class SmarTwistData:

    def __init__(self) -> None:
        self.__id = str()
        self.__total = int()

    @property
    def Id(self):
        return self.__id

    @Id.setter
    def Id(self, value):
        self.__id = value

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

    def __hash__(self) -> int:
        return super().__hash__()

