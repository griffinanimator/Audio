import maya.cmds as cmds

import wave, struct, math

waveFile = wave.open("C:/Users/rgriffin/Music/drumTest.wav", 'rb')

volume = []

length = waveFile.getnframes()

for i in range(0,length):
    waveData = waveFile.readframes(1)
    data = struct.unpack("<h", waveData)
    temp = (int(data[0]) - 128) / 128
    volume.append(20 * math.log10( abs(temp) + 1))

waveFile.close()

noise =  20

for i in range(len(volume)):
    if volume[i] < noise:
        volume[i] = 0
    
x = 0

for i in range(0, len(volume), 200):
    cube = cmds.polyCube(h=1, w=0.1, d=1)
    cmds.setAttr('%s.sy' % cube[0], volume[i] / 10)
    cmds.setAttr('%s.tx' % cube[0], x)
    x = x + 0.1
    
