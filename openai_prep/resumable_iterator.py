

import abc
import asyncio

class ResumableIterator(abc.ABC):

    def __iter__(self):
        return self

    @abc.abstractmethod
    def __next__(self):
        pass

    @abc.abstractmethod
    def get_state(self):
        pass

    @abc.abstractmethod
    def set_state(self):
        pass


class ListIterator(ResumableIterator):

    def __init__(self, arr) -> int:
        self.arr = arr
        self.state = 0

    def __next__(self) -> int:
        val = self.arr[self.state]
        self.state += 1
        return val

    def get_state(self) -> int:
        return self.state

    def set_state(self, state) -> None:
        self.state = state


    def __aiter__(self):
        return self

    async def __anext__(self):
        print('   -anext', self.state, self.arr)
        if self.state < len(self.arr):
            self.state += 1
            return self.arr[self.state - 1]
        raise StopAsyncIteration


def test_base_it():
    a = ListIterator([11, 12, 13, 14])

    states = []
    values = []
    for i in range(4):
        value = next(a)
        state = a.get_state()
        states.append(state)
        values.append(value)

    print(states, values)

    for i in range(2, -1, -1):
        a.set_state(states[i])
        val = next(a)
        print(i, values[i], val)
        assert val == values[i+1]


test_base_it()


class MultipleResumableFileIterator(ResumableIterator):

    def __init__(self, files):
        self.its = []
        self.N = len(files)
        for f in files:
            self.its.append(ListIterator(f))
        self.state = (0, 0)

    def __next__(self):
        while self.state[0] < self.N:  # Fix: use < instead of >=
            try:
                next = next(self.its[self.state[0]])
                return next
            except:
                self.state.ind1 += 1
                if self.state[0] < self.N:
                    self.its[self.state[0]].set_state(0)

    def get_state(self):
        print('get_state', self.state, self.its)
        # if self.state[0] < self.N:
        #     print('   ???', (self.state[0], self.its[self.state[0]].get_state()))
        #     return (self.state[0], self.its[self.state[0]].get_state())
        return self.state

    def set_state(self, state):
        self.state = state
        # ???
        if self.state[0] < self.N:
            self.its[self.state[0]].set_state(self.state[1])

    def __aiter__(self):  # Add missing method for async for
        return self

    async def __anext__(self):
        while True:
            if self.state[0] >= self.N:
                raise StopAsyncIteration
            print('anext: ', self.state)
            try:
                val = await(anext(self.its[self.state[0]]))
                self.state = (self.state[0], self.its[self.state[0]].get_state())
                return val
            except:
                self.state = (self.state[0] + 1, 0)
                if self.state[0] < self.N:
                    self.its[self.state[0]].set_state(0)
        raise StopAsyncIteration


async def test_iterator(it, expected):
    states = []
    while True:
        try:
            states.append(it.get_state())
            await anext(it)
        except:
            break

    print('???', states)

    for i, state in enumerate(states):
        it.set_state(state)
        elements = [x async for x in it]
        print('!!!', elements, expected[i:])
        assert elements == expected[i:]

def test_multi_file_it():
    l = [[4,3], [], [2,1]]
    it = MultipleResumableFileIterator(l)
    asyncio.run(test_iterator(it, [4,3,2,1]))


test_multi_file_it()