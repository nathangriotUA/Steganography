import png
import argparse


parser = argparse.ArgumentParser()
#parser.add_argument("type", help = "read or write [ -r | -w ]")
#parser.add_argument("datatype", help = "file or text [ -f | -t ]")
parser.add_argument("-w", help = "switch to writing mode")
parser.add_argument("data", help = "file name or text", type = str )

def text_to_bin(text):
    ''' convert text into arrays of bins:
        Input:
            - text (str)

        Ouput:
            - Binary arrays
    '''
    chars = bytearray(text, "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)
        bin_char = bin_char[2:]
        bins.append(bin_char)

    return bins

def read(file):
    ''' Read encrypted message in png image : 
        Input:
            - filename (str)
        Output:
            - Message (str)
    '''


def write(file,bins):
    ''' Write ASCII message in png image :
    input:
        - filename (str)
        - array of ASCII in bin 
    output:
        - True or False (if code was written)
    
    errors:
        - code is to long too fit in image
    '''
    f = png.Reader(file)
    print(f.read())
    flatImg = f.read_flat()
    
def main():
    ''' Main function '''
    args = parser.parse_args()

    if args.w:
        bins = text_to_bin("test")
        write(args.data,bins)
    else:
        read(args.data)


if __name__ == '__main__':
    main()
