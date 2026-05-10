import bitIO
import sys

# Test program to:
#
#   1) Demonstrate standard usage of bitIO.BitReader and
#      bitIO.BitWriter from the handed-out library bitIO. This usage
#      can be reused in your project part III code.
#
#   2) Demonstrate that a file must contain an integral number of
#      bytes, that is, an multiple of eight bits. Thus, the library
#      may need to add bits to the output when closing an output file.
#      Padding with zero bits is the choice made in the library.
#
# Run the program on some small text file (containing at least four
# bytes, preferably a few more) by
# 
#   python test.py infilename outfilename
# 
# This will copy the infile to outfile, while adding the character '@'
# to the end of it (after any newline, if the file ends with this),
# and along the way write some multi-digit integer and some bits to
# the screen. Read comments below to understand WHY this should be the
# behavior.

# Open input and output files, using binary mode (reading/writing bytes).
infile = open(sys.argv[1], 'rb')
outfile = open(sys.argv[2], 'wb')

# Create the BitReader/BitWriter using these files as input/output.
bitstreamin = bitIO.BitReader(infile)
bitstreamout = bitIO.BitWriter(outfile)

# First read 32 bits (i.e., four bytes) from the input file and
# interpret these as an int. For this, we use the library method
# readint32bits.
i = bitstreamin.readint32bits()

# Print the value on screen (a multi-digit integer, as four bytes in
# this library is interpreted as the bit pattern of some 32 bit
# integer in the range from 0 to 2^32-1 = 4294967295).
print(i)

# Then also write the int to output file (as the same four bytes, so
# these bytes should appear again in output file exactly as they were
# in input file) using the library method writeint32bits().
bitstreamout.writeint32bits(i)

# Now read the last bits of input file. Do this bit by bit using the
# library method readbit(). At the same time, write them again bit by
# bit to the output file using the library method writebit(). Thus,
# also these bits of the file should appear again in the output file
# exactly as they were in the input file. Note the idiom for reading
# bits: a while-expression going through the file until no more bits
# are available, signaled by readsucces() returning false.
while True:
    bit = bitstreamin.readbit() # try to read a bit from input file
                                # (the return value is an int, of
                                # value either 0 or 1)
    if not bitstreamin.readsucces():  # End-of-file?
        break # stop the while loop
    bitstreamout.writebit(bit) # write the same bit to output file
    if bit == 0: # also print a representation of the bit on the screen
        print("0")
    else:
        print("1")

# Write two bits MORE to output file. This will be padded by the library with
# six 0 bits when closing and flushing the output stream, hence give the
# character '@' (which in ASCII has pattern 01000000).
#
# NOTE: this is ONLY to illustrate the effect of writing a number of bits which
# is not a multiple of eight. In Encode in the project, you should NOT add
# these two bits. However, when writing Huffman codes, you may naturally end up
# in a similar situation (because Huffman codes are not multiples of eight),
# which you should be aware of (you must in Decode avoid reading the bits
# padded by the library when closing the output stream in Encode).
bitstreamout.writebit(0)
bitstreamout.writebit(1)

# Flush the BitWriter (of necessity padding output with 0-bits until
# an integral number of bytes (i.e, a multiple of eight bits) have
# been written, as described above) and automatically close the
# underlying file objects (in this program: infile and outfile).
bitstreamout.close()
bitstreamin.close()
