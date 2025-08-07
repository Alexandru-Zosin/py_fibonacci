# 1. Data Structures and Algorithms: Trie exercise
from typing import Any, Dict, List, Optional


class _TrieNode:
    __slots__ = ("children", "is_end_of_word")

    def __init__(self) -> None:
        self.children: Dict[str, '_TrieNode'] = {}  # '' undefined atm
        self.is_end_of_word: bool = False


class Trie:
    def __init__(self) -> None:
        self.root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = _TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


class _Node:
    __slots__ = ("value", "next", "left", "right")
    # only these attributes are allowed in _Node instances
    # because we might create many of them, this saves memory

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional["_Node"] = None
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None
    # redenumirea cu _a atributelor este redundanta, intrucat
    # _node este deja doar pt. uz intern + node.value etc. se intalneste in
    # queue si in stack


class Queue:
    def __init__(self) -> None:
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None
        self._size: int = 0

    def enqueue(self, item: Any) -> None:
        new_node = _Node(item)
        if self._tail:
            self._tail.next = new_node
        else:
            self._head = new_node
        self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        if not self._head:
            raise IndexError("dequeue from empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:  # now queue is empty
            self._tail = None
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if not self._head:
            raise IndexError("peek from empty queue")
        return self._head.value

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


class Stack:
    def __init__(self) -> None:
        self._top: Optional[_Node] = None
        self._size: int = 0

    def push(self, item: Any) -> None:
        node = _Node(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self) -> Any:
        if not self._top:
            raise IndexError("pop from empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if not self._top:
            raise IndexError("peek from empty stack")
        return self._top.value

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

# 2.a Example that triggers an MRO conflict

class Root:
    def who_am_i(self) -> str:
        return "I am Root"


class BranchA(Root):
    def who_am_i(self) -> str:
        return "I am BranchA"


class BranchB(Root):
    def who_am_i(self) -> str:
        return "I am BranchB"

class SubA(BranchA, BranchB):
    pass # brA via MRO

class SubB(BranchB, BranchA):
    pass #!brB via MRO

#class Conflicted(SubA, SubB):
#    pass #subA + subB cant be linearized
# This will trigger error if uncommented
# created by the diamond inheritance pattern
# Cannot create consistent method orderingPylancereportGeneralTypeIssues

# 2b. example inheritance scenario inspired from head first design patterns ive been
# reading lately and the mixins
class FlyWithWings:
    def fly(self) -> None:
        print(f"{self.__class__.__name__} flaps wings")

class FlyNoWay:
    def fly(self) -> None:
        print(f"{self.__class__.__name__} can't fly")

class Quack:
    def quack(self) -> None:
        print("Quack")

class Squeak:
    def quack(self) -> None:
        print("Squeak")

class Duck:
    """Concrete behaviours come from mixins (not quite strategy DP, you'd need)
     concrete classes for that, but this is a somewhat similar pattern
     (it's not quite program to an interface, but rather to a.. mixin)
       """

    def __init__(self, name: str) -> None:
        self.name = name

    def display(self) -> None:  # to be overridden
        raise NotImplementedError

    def swim(self) -> None:
        print(f"{self.name} is swimming.")

# Mix in behaviors: mixins first because they add functionality so 
# they should be first in the MRO
class Mallard(FlyWithWings, Quack, Duck):
    def display(self) -> None:
        print(f"I'm a Mallard named {self.name}.")

class Rubber(FlyNoWay, Squeak, Duck):
    def display(self) -> None:
        print(f"I'm a Rubber Duck named {self.name}.")

#gpt generated tests
def _test_trie() -> None:
    trie = Trie()
    trie.insert("duck")
    assert trie.search("duck")
    assert not trie.search("duk")
    assert trie.starts_with("du")
    #assert trie.starts_with("duckling") - this will error

def _test_queue_stack() -> None:
    q = Queue()
    for i in range(3):
        q.enqueue(i)
    assert len(q) == 3 and q.dequeue() == 0 and q.peek() == 1

    s = Stack()
    for ch in "abc":
        s.push(ch)
    assert len(s) == 3 and s.pop() == "c" and s.peek() == "b"


def _test_ducks() -> None:
    mallard = Mallard("Mike")
    rubber = Rubber("Bubbles")

    mallard.display()
    mallard.fly()
    mallard.quack()
    mallard.swim()

    rubber.display()
    rubber.fly()
    rubber.quack()
    rubber.swim()


def _test_mro_conflict() -> None:
    try:
        class Conflicted(SubA, SubB):  # noqa: F811  (intentionally conflicting)
            pass

    except TypeError as err:
        print("Expected MRO error:", err)


if __name__ == "__main__":
    _test_trie()
    _test_queue_stack()
    _test_ducks()
    _test_mro_conflict()
    print("All tests passed!")