import abc
import asyncio

class ResumableIterator(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def __next__(self):
        pass

    @abc.abstractmethod
    def get_state(self):
        pass

    @abc.abstractmethod
    def set_state(self, state):
        pass



class ListIterator(ResumableIterator):

    def __init__(self, arr):
        self.arr = arr
        self.state = 0
        self.N = len(self.arr)

    def __next__(self):
        if self.state == self.N:
            raise StopIteration
        self.state += 1
        return self.arr[self.state - 1]

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state



def test_list_it():
    l = ListIterator(['a', 'b', 'c'])
    states = []
    values = []

    try:
        while True:
            value = next(l)
            state = l.get_state()
            values.append(value)
            states.append(state)
    except:
        print('Done')

    print(values, ['a', 'b', 'c'])

    l.set_state(states[0])
    new_values = []
    expected = ['b', 'c']

    try:
        while True:
            value = next(l)
            new_values.append(value)
    except:
        print('Done')

    print(new_values, expected)

# test_list_it()

def test_iterator(it_class, init, expected_full_seq):
    it = it_class(init)
    states = []
    vals = []

    while True:
        try:
            states.append(it.get_state())

            vals.append(next(it))
        except StopIteration:
            break

    assert expected_full_seq == vals, ('initial', expected_full_seq, vals)

    for i, state in enumerate(states):
        it.set_state(state)
        vals = []
        while True:
            try:
                vals.append(next(it))
            except StopIteration:
                break
        assert vals == expected_full_seq[i:], ('error', i, state)

    print('Success')



test_iterator(ListIterator, ['a', 'b', 'c'], ['a', 'b', 'c'])


class MultipleIterator(ResumableIterator):

    def __init__(self, its):
        self.its = its
        self.state = (0, 0)
        self.N = len(self.its)

    def __next__(self):

        while True:
            if self.state[0] >= self.N:
                raise StopIteration

            try:
                it = self.its[self.state[0]]
                val = next(it)
                self.state  = (self.state[0], it.get_state())
                return val
            except StopIteration:
                self.state = (self.state[0] + 1, 0)
                if self.state[0] < self.N:
                    self.its[self.state[0]].set_state(0)
                continue

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        if self.state[0] < self.N:
            self.its[state[0]].set_state(state[1])

test_iterator(MultipleIterator, [ListIterator(['a', 'b']), ListIterator([]), ListIterator(['c', 'd'])], ['a', 'b', 'c', 'd'])



class AsyncIterator(abc.ABC):

    def __aiter__(self):
        return self

    @abc.abstractmethod
    async def __anext__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_state(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def set_state(self, state):
        raise NotImplementedError()

class AsyncListIterator(AsyncIterator):

    def __init__(self, arr):
        self.arr = arr
        self.state = 0
        self.N = len(arr)

    async def __anext__(self):
        # await val
        if self.state >= self.N:
            raise StopAsyncIteration
        self.state += 1
        return self.arr[self.state - 1]

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state


class AsyncMultiListIterator(AsyncIterator):

    def __init__(self, its):
        self.its = its
        self.state = (0, 0)
        self.N = len(its)

    async def __anext__(self):

        while True:
            if self.state[0] >= self.N:
                raise StopAsyncIteration
            try:
                it = self.its[self.state[0]]
                val = await anext(it)
                self.state = (self.state[0], it.get_state())
                return val
            except StopAsyncIteration:
                self.state = (self.state[0]+1, 0)
                if self.state[0] < self.N:
                    self.its[self.state[0]].set_state(0)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        if self.state[0] < self.N:
            self.its[state[0]].set_state(state[1])

async def test_aync_it(it_class, init, expected):

    it = it_class(init)
    states = []
    vals = []

    while True:
        try:
            states.append(it.get_state())
            vals.append(await anext(it))
        except StopAsyncIteration:
            break

    assert expected == vals, ('initial', expected, vals)

    for i, state in enumerate(states):
        print(i, state)
        it.set_state(state)
        vals = []
        while True:
            try:
                vals.append(await anext(it))
            except StopAsyncIteration:
                break
        assert vals == expected[i:], ('error', i, state, vals, expected[i:])

    print('Success')

asyncio.run(test_aync_it(AsyncListIterator, [3,2,1], [3,2,1]))

asyncio.run(test_aync_it(AsyncMultiListIterator, [AsyncListIterator(['a', 'b']), AsyncListIterator([]), AsyncListIterator(['c', 'd'])], ['a', 'b', 'c', 'd']))