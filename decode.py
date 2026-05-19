import sys

from PQHeap import createEmptyPQ, insert, extractMin
from Element import Element
from Node import Node
import bitIO



class Decoder:
    ALPHABET_SIZE: int = 256

    def __init__(self, compressed_filename: str, decoded_filename: str):
        self.compressed_filename: str = compressed_filename
        self.decoded_filename: str = decoded_filename
        self.frequency_list: list[int] = [0] * self.ALPHABET_SIZE
        self.pq: list[Element] = createEmptyPQ()
        self.root: None | Node = None
        self.total_original_bytes: int = 0

    def _create_huffman_tree(self) -> None:
        for data, key in enumerate(self.frequency_list):
            outer_node: Node = Node(
                    left=None,
                    right=None,
                    byte_value=data
                    )

            insert(self.pq, Element(key, outer_node))

        while len(self.pq) > 1:
            left_child: Element = extractMin(self.pq)
            right_child: Element = extractMin(self.pq)

            parent_key: int = left_child.key + right_child.key
            inner_node: Node = Node(left_child.data, right_child.data, None)

            insert(self.pq, Element(parent_key, inner_node))

        self.root = extractMin(self.pq).data

    def decode(self) -> None:
        with open(self.compressed_filename, "rb") as input_file:
            with open(self.decoded_filename, "wb") as output_file:
                reader: bitIO.BitReader = bitIO.BitReader(input_file)

                for i in range(self.ALPHABET_SIZE):
                    freq = reader.readint32bits()
                    self.frequency_list[i] = freq
                    self.total_original_bytes += freq

                self._create_huffman_tree()

                written_bytes = 0
                current_node = self.root

                while written_bytes < self.total_original_bytes:
                    bit = reader.readbit()

                    if bit == 0:
                        current_node = current_node.left
                    elif bit == 1:
                        current_node = current_node.right

                    if current_node.byte_value is not None:
                        output_file.write(bytes([current_node.byte_value]))
                        written_bytes += 1
                        current_node = self.root



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python Decode.py <compressed_file> <decoded_file>")
        sys.exit(1)

    compressed_file = sys.argv[1]
    decoded_file = sys.argv[2]

    decoder = Decoder(compressed_file, decoded_file)
    decoder.decode()