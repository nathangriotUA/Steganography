import png
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument("type", help = "read or write [ -r | -w ]")
#parser.add_argument("datatype", help = "file or text [ -f | -t ]")
parser.add_argument("data", help = "file name or text", type = str )

def text_to_bin(text):
    chars = bytearray(text, "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)
        bin_char = bin_char[2:]
        bins.append(bin_char)

    return bins

def read(file):
    f = png.Reader(file)
    print(f.read())
    flatImg = f.read_flat()
    

def main():
    args = parser.parse_args()
    read(args.data)


if __name__ == '__main__':
    main()
