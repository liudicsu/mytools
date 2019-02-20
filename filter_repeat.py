import pybloom
import sys

if __name__ == "__main__":
    capacity = sys.argv[1]
    bf = pybloom.BloomFilter(capacity=int(capacity), error_rate=0.001)
    for line in sys.stdin:
        if not bf.add(line.strip()):
            print line.strip()
