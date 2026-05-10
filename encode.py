import sys

from PQHeap import createEmptyPQ, insert, extractMin
from Element import Element
from Node import Node
import bitIO



class Encoder:
    ALPHABET_SIZE: int = 256

    def __init__(self, filename: str):
        self.frequency_list: list[int] = [0] * self.ALPHABET_SIZE
        self.filename: str = filename
        self.pq: list[Element] = createEmptyPQ()
        self.root: None | Node = None
        self.code_table: list[str] = [""] * self.ALPHABET_SIZE

    def _get_frequency_list(self) -> None:
        with open(self.filename, "rb") as f:
            while True:
                content = f.read(1)
                if len(content) == 0:
                    break
                else:
                    self.frequency_list[content[0]] += 1


    def _generate_codes(self, node: Node, current_code: str):
        if node.byte_value is not None:
            self.code_table[node.byte_value] = current_code
        if node.left is not None:
            self._generate_codes(node.left, current_code + "0")
        if node.right is not None:
            self._generate_codes(node.right, current_code + "1")

    def _create_huffman_tree(self) -> None:
        for data, key in enumerate(self.frequency_list):
            outer_node: Node = Node(
                    left=None,
                    right=None,
                    byte_value=data
                    )

            insert(self.pq, Element(key,outer_node))

        while len(self.pq) > 1:
            left_child: Element = extractMin(self.pq)
            right_child: Element = extractMin(self.pq)

            parent_key: int = left_child.key + right_child.key
            inner_node : Node = Node(left_child.data, right_child.data, None)

            insert(self.pq, Element(parent_key, inner_node))

        self.root = extractMin(self.pq).data

        self._generate_codes(self.root, "")

    def _write_header(self, writer: bitIO.BitWriter):
        for i in self.frequency_list:
            writer.writeint32bits(int(i))


    def encode(self, outputfile: str):
        self._get_frequency_list()
        self._create_huffman_tree()

        with open(self.filename, "rb") as input_file:
            with open(outputfile, "wb") as output_file:
                writer: bitIO.BitWriter = bitIO.BitWriter(output_file)
                self._write_header(writer)

                while True:
                    content = input_file.read(1)
                    if len(content) == 0:
                        break
                    else:
                        for bit in self.code_table[content[0]]:
                            writer.writebit(int(bit))
                writer.close()



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python Encode.py <original_file> <compressed_file>")
        sys.exit(1)

    filename = sys.argv[1]
    output_file = sys.argv[2]

    encoder = Encoder(filename)
    encoder.encode(output_file)


