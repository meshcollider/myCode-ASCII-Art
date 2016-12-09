# myCode-ASCII-Art
The simple little program generates coloured myCode (BBCode for MyBB Forums) text of your choice based on an image

Verdana.ttf is the font used in this case to match that of the forum. This allows the correct pixel dimensions of the characters to be found.

## Usage

You must have python3 installed along with [Pillow](https://github.com/python-pillow/Pillow). Simply run the script with the following command:

```
myImageCode.py <IMAGE PATH> <OUTFILE> [TEXT] [SCALE FACTOR] [USE TRANSPARENT]
```

IMAGE PATH is the path to the image you wish to use
OUTFILE is the name of a text file to store the output myCode in
TEXT is optional (defaults to MESH) and is the text to tesselate the image with
SCALE FACTOR is the factor by which the output text should be bigger than the original image. Defaults to 1
USE TRANSPARENT will use myCode color="transparent" instead of black for any alpha less than 10%. By default this is turned off (0)

## License

This program is licensed under the GPL3. See LICENSE for more info.