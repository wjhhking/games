
import collections

class Excel:
    def __init__(self):
        self.data = {}
        self.cache = {}
        self.parents = collections.defaultdict(lambda:set())

    def get(self, key):
        if key in self.cache:
            print('used cache', key)
            return self.cache[key]

        if key not in self.data:
            raise ValueError('Invalida key')

        value, format = self.data[key]
        if format == 'v':
            return value
        else:
            c1, c2 = value
            ans = self.get(c1) + self.get(c2)
            self.cache[key] = ans
            return ans

    def set(self, key, value=None, formula=None):
        old_c1, old_c2 = None, None

        if key in self.data:
            old_v, old_f = self.data[key]
            if old_f == 'f':
                old_c1, old_c2 = old_v

        if value != None:
            self.data[key] = (value, 'v')
            if old_c1 or old_c2:
                self.parents[old_c1].remove(key)
                self.parents[old_c2].remove(key)
        elif formula != None:
            self.check_cycle(key, formula)
            # remove parents
            if old_c1 or old_c2:
                self.parents[old_c1].remove(key)
                self.parents[old_c2].remove(key)
            # Add new parenet
            c1,c2=formula
            self.data[key] = (formula, 'f')
            self.parents[c1].add(key)
            self.parents[c2].add(key)

        # invalid cache when success insert
        self.invalidate_cache(key)


    def check_cycle(self, key, formula):
        print('Checking cycle:', key, formula)
        c1, c2 = formula

        visited = {}

        def dfs(curent_node, target):
            print('   -dfs', curent_node, target)
            if curent_node == target:
                return True

            if curent_node in visited:
                return False

            visited[curent_node] = True

            if self.data[curent_node][1] == 'v':
                return False

            child1, child2 = self.data[curent_node][0]
            return dfs(child1, target) or dfs(child2, target)

        has_cycle = dfs(c1, key) or dfs(c2, key)
        if has_cycle:
            raise ValueError('Cycle')

    def invalidate_cache(self, key):
        try:
            del self.cache[key]
        except:
            pass

        ps = self.parents[key]
        for p in ps:
            if p in self.cache:
                del self.cache[p]
                self.invalidate_cache(p)


# Q1
excel = Excel()
excel.set('A1', 2)
excel.set('B2', 3)
q1 = excel.get('A1')
print('1. Naive get\n   ', q1)
print('-'*80)

# Q2
excel.set('C3', formula=('A1', 'B2'))
q2 = excel.get('C3')
print('2. formual:\n   ', q2)
print('-'*80)

# Q3
q3 = excel.get('C3')
print('3. cache:\n   ', q3)
print('-'*80)

# Q4
excel.set('C3', formula=('B2', 'A1'))
print('Current cache', excel.cache)
q4 = excel.get('C3')
print('4. not using cache:\n   ', q3)
print('-'*80)

# Q5 cycle
try:
    excel.set('A1', formula=('B2', 'C3'))
    print('5. Fail')
    print('   data', excel.data)
    print('   cache', excel.cache)
    print('   parents', excel.parents)
except:
    print('5. Success')


