from PIL import Image
stop = False
buffsize = 11090
lines = 0
channel_1 = []
channel_2 = []
channel_3 = []
channel_4 = []
channel_5 = []
state_list = []
def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def read_AVHRR(buff):
    global state_list
    if len(state_list) == 0:
        state_list.append(buff)
        return 0
    else:
        state_list.append(buff)
        #buff = (state_list[1] << 16) | state_list[0]
        buff = int.from_bytes(state_list[0], "big")<<8| int.from_bytes(state_list[1], "big")
        #print(type(buff))
        #print(buff)
        buff =  int_to_bytes(buff)
        #buff = int.to_bytes(int(int(state_list[0]) + int(state_list[1])),"big")
        
        state_list = []
    global lines
    global stop
    resolution = 2048
    pos = 750 #AVHRR data
    channel = 3 #change to decode data
    for channel in range(5):
        for i in range(resolution):
            try:
                pixel = buff[750 + channel + i * 5]
            except:
                print("ERROR READING PIXEL...")
                stop = True
            if channel == 0:
                channel_1.append(pixel*5)
            if channel == 1:
                channel_2.append(pixel*5)
            if channel == 2:
                channel_3.append(pixel*5)
            if channel == 3:
                channel_4.append(pixel*5)
            if channel == 4:
                channel_5.append(pixel*5)
    lines = lines + 1
        
        
def read_in_chunks(file_object,chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
def process_AVHRR():
    w = 2048
    ch1 = Image.new('RGB',(2048,lines))
    ch2 = Image.new('RGB',(2048,lines))
    ch3 = Image.new('RGB',(2048,lines))
    ch4 = Image.new('RGB',(2048,lines))
    ch5 = Image.new('RGB',(2048,lines))
    px, py = 0, 0
    for p in range(lines*w):
        if px == w:
            py = py+1
            #print(py)
            px = 0
        else:
            #print(py,px)
            #print(round(channel_3[py*w + px]/6))
            ch1.putpixel((px, py), (int(round(channel_1[py*w + px]/2)),int(round(channel_1[py*w + px]/2)),int(round(channel_1[py*w + px]/2))))
            ch2.putpixel((px, py), (int(round(channel_2[py*w + px]/2)),int(round(channel_2[py*w + px]/2)),int(round(channel_2[py*w + px]/2))))
            ch3.putpixel((px, py), (int(round(channel_3[py*w + px]/2)),int(round(channel_3[py*w + px]/2)),int(round(channel_3[py*w + px]/2))))
            ch4.putpixel((px, py), (int(round(channel_4[py*w + px]/2)),int(round(channel_4[py*w + px]/2)),int(round(channel_4[py*w + px]/2))))
            ch5.putpixel((px, py), (int(round(channel_5[py*w + px]/2)),int(round(channel_5[py*w + px]/2)),int(round(channel_5[py*w + px]/2))))
            px = px+1
    ch1.save("ch1.png")
    ch2.save("ch2.png")
    ch3.save("ch3.png")
    ch4.save("ch4.png")
    ch5.save("ch5.png")
with open("hrpt.raw16",'rb') as f:
    print("READING RAW BUFFER")
    for buffer in read_in_chunks(f,buffsize):
        read_AVHRR(buffer)
    print("Output images...")
    process_AVHRR()
        
    f.close()
print("Finished")
