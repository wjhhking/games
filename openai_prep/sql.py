


class Table:

    def __init__(self, col_names) -> None:
        self.column_names = {}
        self.rows = []  # list of list,

        for i, column_name in enumerate(col_names):
            self.column_names[column_name] = i

        self.N = len(self.column_names)

    def insert(self, row):

        row_list = [0] * self.N
        print('inserting row into table:', row)
        for k in row:
            v = row[k]
            print(k, v)
            i = self.column_names[k]
            row_list[i] = v

        self.rows.append(row_list)

    def query_raw(self, cols):
        column_indexes  = [self.column_names[col] for col in cols]
        ans = []
        for row in self.rows:
            ans_row = [row[i] for i in column_indexes]
            ans.append(ans_row)

        return ans

    def query(self, cols, conditions=None, orderby=None,reverse=False):
        rows = self.rows
        print('   -query with condition', rows, conditions)

        if conditions != None:
            ans = []

            for row in rows:
                satisfy = True
                for cond in conditions:
                    k, o, v = cond
                    i = self.column_names[k]
                    print('   -kov', k,o,v,i,row[i])

                    if o == '=':
                        if row[i] != v:
                            satisfy = False
                    elif o == '<':
                        if not row[i] < v:
                            satisfy = False
                    elif o == '>':
                        if not row[i] > v:
                            satisfy = False
                if satisfy:
                    ans.append(row)

            rows = ans

        if orderby != None:
            order_index = [self.column_names[name] for name in orderby]
            rows = sorted(rows, key=lambda x: [x[i] for i in order_index], reverse=reverse)
            print('    -sorted: ', rows)

        print('rows after condition', rows)

        column_indexes  = [self.column_names[col] for col in cols]
        ans = []
        for row in rows:
            ans_row = [row[i] for i in column_indexes]
            ans.append(ans_row)

        return ans




    # def query_with_where(self, cols, conditions):
    #     pass

    # def query_with_order(self, cols, conditions, orderby):
    #     pass


class InMemDb:

    def __init__(self):
        self.tables = {}

    def insert(self, tablename, rows):
        if tablename not in self.tables:
            self.tables[tablename] = Table(rows.keys())

        self.tables[tablename].insert(rows)

    def query(self, table_name: str, columns:list[str]):
        return self.tables[table_name].query(columns)


    def query_with_where(self, table_name, select_columns, conditions):
        return self.tables[table_name].query(select_columns, conditions)

    def query_with_order_by(self, table_name: str, select_columns: list,
                           order_by_columns: list, reverse: bool = False):
        return self.tables[table_name].query(select_columns, orderby=order_by_columns, reverse=reverse)

    def query_king(self, table_name, select_columns, conditions=None, order_by=None, reverse=False):
        return self.tables[table_name].query(select_columns, conditions, order_by, reverse)


db = InMemDb()

db.insert('users', {'id': 101, 'name': 'Alice'})
db.insert('users', {'id': 102, 'name': 'Bob'})
db.insert('users', {'id': 103, 'name': 'Charlie'})

ans = db.query('users', ['id'])

print('1. Naive insert + query\n   ', ans)


print('-'*80)
ans = db.query_with_where('users', ['name'], [['id', '=', 102]])
print('2.a where\n   ', ans)

ans = db.query_with_where('users', ['name'], [['id', '>', 102]])
print('2.b where\n   ', ans)

ans = db.query_with_where('users', ['name'], [['id', '<', 102]])
print('2.c where\n   ', ans)


print('-'*80)
ans = db.query_with_order_by('users', ['name'], order_by_columns=['name'], reverse=False)
print('3.a order by', ans)
ans = db.query_with_order_by('users', ['name'], order_by_columns=['name'], reverse=True)
print('3.b order by', ans)




print('-'*80)
ans = db.query_king('users', ['name'], conditions=[['id', '<', 103]], order_by=['name'], reverse=True)
print('4 where and order by', ans)

