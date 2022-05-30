from utils.connection import Connection


class Model(Connection):
    def __init__(self, tableName='test') -> None:
        super().__init__()
        self.tableName = tableName
