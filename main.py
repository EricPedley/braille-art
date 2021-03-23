import cv2
import numpy as np
img = cv2.imread("head pic.png")
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
outputWidth = 30
ratio = 4*outputWidth/img.shape[1]
img = cv2.resize(img,dsize=(int(ratio*img.shape[1]),int(ratio*img.shape[0])))
output=""
for y in range(0,img.shape[0]-img.shape[0]%4,4):
    for x in range(0,img.shape[1]-img.shape[1]%2,2):
        selectedPixels = img[y:y+4,x:x+2]#4x2 area that braille text encompasses(⡀ to ⣿)
        #braille characters start at unicde 0x2800 and end at 0x28ff. the first 8-dot braille characer is 2840
        #try something with bitwise operators and adding to characters to generate the unicode characters
        #http://xahlee.info/comp/unicode_braille.html
        #there are 3 sets of characters for 8-dot, and we can check with a condition
        #which of the three sets the current pixels are in(dot at topleft or topright or both bottoms), then use the bitwise operators
        if img[y+3][x] >125 and img[y+3][x+1]>125:#both bottom dots, use [28c0,28ff]
            base = 0x28c0
        elif img[y+3][x]>125:#only bottom left dot, use [2840,287f]
            base = 0x2840
        elif img[y+3][x+1]>125:#only bottom right dot, use [2880,228bf]
            base = 0x2880
        else:#neither bottom dot, use 6-dot pattern [2800,283f]
            base = 0x2800#blank braille pattern is 2800
        modifier = 0b0
        count=0
        for y1 in range(y,y+3):
            for x1 in range(x,x+2):
                selectedPixel = img[y1,x1]
                if selectedPixel>127:
                    modifier = modifier | 0b1<<count
                count+=1
        character = base+modifier
        output+=chr(character)
    output+="\n"
print(output)