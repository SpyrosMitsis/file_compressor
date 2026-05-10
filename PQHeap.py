# Project Part I: PQHeap
# Group: 
#   Erik Tatsumi Leutz, erleu25
#   Georgios Pappas, gepap25
#   Spyridon Mitsis spmit25

from Element import Element


def get_left_child(index: int) -> int:
    return 2 * index + 1

def get_right_child(index: int) -> int:
    return 2 * index + 2

def get_parent(index: int) -> int:
    return (index  - 1) // 2

def swap(A: list[Element], a: int, b: int) -> None:
    A[a], A[b] = A[b], A[a]


def insert(A: list[Element], key: Element) -> None:
    i = len(A)
    A.append(key)
    while i > 0 and A[get_parent(i)] > A[i]:
        swap(A, i, get_parent(i))
        i = get_parent(i)

def createEmptyPQ() -> list[Element]:
    A: list[Element] = []
    return A

def extractMin(A: list[Element]) -> Element:
    min: Element = A[0]
    A[0] =  A[len(A) - 1]
    del A[-1]
    heapify(A, 0)
    return min


def heapify(A: list[Element], i: int) -> None:
    heap_size = len(A)
    left = get_left_child(i)
    right = get_right_child(i)
    if left < heap_size and A[left] < A[i]:
        least = left
    else:
        least = i
    if right < heap_size and A[right] < A[least]:
        least = right
    if least != i:
        swap(A, i, least)
        heapify(A, least)

if __name__ == "__main__":
    import sys

    pq = createEmptyPQ()
    
    n = 0
    for line in sys.stdin:
        insert(pq,int(line))
        n = n+1
    
    print()
    while n > 0:
        print(extractMin(pq))
        n = n-1


