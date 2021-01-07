import png
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("image", help = "image file", type = str )
parser.add_argument("-w", help = "switch to writing mode", action = "store_true")
parser.add_argument("-f", help = "read message from file", type = str)
parser.add_argument("-t", help = "read message from text", type = str)
parser.add_argument("-filename", help = 'filename', type = str )
parser.add_argument("-message", help = 'message', type = str )

def text_to_bin(text):
    ''' convert text into arrays of bins:
        Input:
            - text (str)
        Ouput:
            - Binary arrays
    '''
    # EOM (END OF MESSAGE) signals that it's the end of the message
    chars = bytearray(text+"EOM", "utf8")
    bins = []

    for char in chars:
        bin_char = bin(char)[2:].zfill(8)
        bin_char = list(bin_char)
        bins += bin_char

    return bins


def readFromFile(filename):
    ''' allows to read the content of a file:
        input:
            - filename
        output:
            - file content (str)
    '''
    file = open(filename, "r")
    text = file.read()
    file.close()
    return text

def check_conditions(ASCII, conditions):
    ''' This method checks if the conditions are met to stop reading the file
        input:
            ASCII char
        output:
            True if conditions are met
            False if conditions are not met
    '''
    keys = conditions.keys()
    for i in keys:
        if not conditions[i] and ASCII == i:
            conditions[i] = True
            break

        elif not conditions[i] and ASCII != i:
            for condition in conditions:
                condition = False
            break
       
    return conditions["M"]


def read(file_encrypted):
    ''' Read encrypted message in png image : 
        Input:
            - filename_encrypted (str)
        Output:
            - Message (str)
    '''
    f = png.Reader(file_encrypted)
    f = f.asRGBA() # Every png is converted in a RGBA format
    img= []
    list_binaries_of_files = []
    for x in f[2]:
        img.append(list(x))
        list_binaries_of_files += list(x)
    
    i = 0
    ASCIIS = []
    ASCII = []

    stop_Condition = {"E" : False, "O" : False, "M" : False}

    for img_value in list_binaries_of_files:
        value = '{0:08b}'.format(img_value)[-1:] # get low weight bit
        ASCII.append(value)
        i+=1

        if i == 8: # every 8 binary we get the new ascii and append it
            i = 0
            ASCII = "".join(ASCII)
            ASCII_char = chr(int(ASCII, 2))
            ASCIIS.append(ASCII_char)
            ASCII = []

            if check_conditions(ASCII_char, stop_Condition) :
                break

    return "".join(ASCIIS)[:-3]

def write(file, bins):
    ''' Write ASCII message in png image :
        input:
            - filename (str)
            - array of ASCII in binary
        errors:
            - code is to long too fit in image
    '''
    f = png.Reader(file)
    f = f.asRGBA() # Every png is converted in a RGBA format
    list_binaries_of_files = []
    img= []
    for x in f[2]:
        img.append(list(x))
        list_binaries_of_files += list(x)

    if len(list_binaries_of_files) < len(bins):
        SystemError("Message is to long in order to fit in this image.")

    newImg = []
    for img_value, encrypted_value  in zip(list_binaries_of_files, bins):
        bin_value = '{0:08b}'.format(img_value)
        list_bins_values = list(bin_value)
        
        if encrypted_value == '1':
            list_bins_values[7] = '1'
        elif list_bins_values[7] == '1' and encrypted_value == '0':
            list_bins_values[7] = '0'
        
        new_bin = ''.join(list_bins_values)
        newImg.append(int(new_bin, 2))

    i = 0
    for x in range(len(img)):
        for y in range(len(img[x])):
            img[x][y] = newImg[i]
            i+=1
            if i == len(newImg):
                break
        if i == len(newImg):
            break

    f_encrypted = open(file[:-4] + '_encrypted.png', 'wb')
    w = png.Writer(f[0], f[1], greyscale=False, bitdepth=f[3]["bitdepth"], alpha=True)
    w.write(f_encrypted, img)
    f_encrypted.close()
    


def main():
    ''' Main function '''
    args = parser.parse_args()
    if args.w:
        if args.t:
            message = args.t
        elif args.f:
            message = readFromFile(args.f)
        else:
            message = input('Please write your message: ')

        bins = text_to_bin(message)
        write(args.image, bins)

    else:
        message = read(args.image)
        try:
            p1 = subprocess.Popen(["echo",message], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["strings","-n","1"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()  
            output = p2.communicate()[0]
            print(output)
        except :
            print("error message not found")



if __name__ == '__main__':
    main()
