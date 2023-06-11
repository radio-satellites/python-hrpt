from PIL import Image
import os
import struct
from tqdm import tqdm

buffsize = int(11090*16)
buffsize_bytes = int(buffsize/8)
lines = 0

buffer = []

bytes_noframes = os.path.getsize('NOAA19_may13.raw16')

lines = int(bytes_noframes/buffsize_bytes)

ch1 = Image.new('I',(int(2048),lines))
ch2 = Image.new('I',(int(2048),lines))
ch3 = Image.new('I',(int(2048),lines))
ch4 = Image.new('I',(int(2048),lines))
ch5 = Image.new('I',(int(2048),lines))

print("Found "+str(lines)+" frames!")

cur_x = 0

cur_y = 0

with open("NOAA19_may13.raw16",'rb') as f:
    for i in tqdm(range(lines)):
        
        for x in range(int(buffsize_bytes/2)):
            ints = f.read(2)
            current_int = ints[1] << 8 | ints[0] #struct.unpack_from("<H",f.read(2))[0] #
            buffer.append(current_int)
        for k in range(2048):
            #Deinterleave
            #print((k,i))
            #print(buffer[750 + 5*k])
            ch1.putpixel((k,i),buffer[750 + 5*k]*20)
            ch2.putpixel((k,i),buffer[751 + 5*k]*20)
            ch3.putpixel((k,i),buffer[752 + 5*k]*20)
            ch4.putpixel((k,i),buffer[753 + 5*k]*20)
            ch5.putpixel((k,i),buffer[754 + 5*k]*20)
        buffer = []

            
    
ch1.save("AVHRR-CH1.png")
ch2.save("AVHRR-CH2.png")
ch3.save("AVHRR-CH3.png")
ch4.save("AVHRR-CH4.png")
ch5.save("AVHRR-CH5.png") 
    




"""
for i in range(1505,5596,2): #start, stop, step
        current_int = int(bytes(current_frame[i:i+1]))
        if cur_x >= 2048:
            cur_x = 0
            cur_y += 1
        ch1.putpixel((cur_x,cur_y),(current_int,current_int,current_int))
        cur_x += 1
"""
