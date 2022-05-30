import sqlite3


class Connection:
    def __init__(self, dbName="empower") -> None:
        self.conn = sqlite3.connect(dbName+".db")

    def prepareStatement(self, d):
        filtered_dict = {
            k: v for (k, v) in d.items() if not 'conn' in k and not 'tableName' in k}
        statement = f"INSERT INTO {self.tableName} (" + \
            ','.join(list(filtered_dict.keys())) + ') VALUES (' + \
            ','.join([f"'{i}'" if type(i) == type(
                'a') else str(i) for i in filtered_dict.values()]) + ')'
        return statement

    def save(self):
        try:
            self.conn.execute(self.prepareStatement(self.__dict__))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print('😠', e)

    def load(self, condition={}, clause='LIKE', sep=' AND '):
        if condition == {}:
            return [i for i in self.conn.execute(f'SELECT * FROM {self.tableName}')]
        try:
            if clause == 'LIKE':
                prepareConditions = [f"{k} LIKE '{v}%'" if type(v) == type(
                    'a') else f"{k}={v}" for (k, v) in condition.items()]
                return [i for i in self.conn.execute(f"SELECT * FROM {self.tableName} WHERE "+sep.join(prepareConditions))]
            prepareConditions = [f"{k}='{v}'" if type(v) == type(
                'a') else f"{k}={v}" for (k, v) in condition.items()]
            return [i for i in self.conn.execute(f"SELECT * FROM {self.tableName} WHERE "+sep.join(prepareConditions))]
        except sqlite3.OperationalError as e:
            print('😠', e)
            return False

    def createTable(self, statement):
        try:
            self.conn.execute(statement)
            return True
        except sqlite3.OperationalError as e:
            print('😠', e)

    def dropTable(self):
        try:
            self.conn.execute(f'DROP TABLE {self.tableName}')
            return True
        except sqlite3.OperationalError as e:
            print('😠', e)
