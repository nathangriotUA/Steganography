# Steganography
TP2 sécurité steganography

With this toolkit you can add a message a read a message from a PNG file.

there are multiple arguments:

- image : this argument is used to select the image you cant to write or read the message from/to
- -w : is a switch to activate writing mode
- -f : read message from file you need to specify the name of the file behind
- -t : read message from text, you need to write the message after between quotes

example to write in image:

    python3 main.py shiba.png -w -t "this is a test message"

example to read in image:

    python3 main.py shiba_encrypted.png
