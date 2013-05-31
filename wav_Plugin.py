"""  To Run
import maya.cmds as cmds

scene = cmds.file(q=True, sn=True)
cmds.file(f=True, new=True)
cmds.unloadPlugin('wav_Plugin.py', f=True)
cmds.loadPlugin( 'C:/Users/Griffy/Google Drive/RG_ARTTOOLS/PythonWaveExp/wav_Plugin.py')
cmds.file(scene, o=True)

# Create an audio node
cmds.createNode('audioNode')


# Setup objects
CHANNEL = 'sy'
OFFSET = -1

objs = cmds.ls(sl=True)
node = cmds.createNode('audioNode')
cmds.connectAttr('time1.outTime', '%s.time' % node)
cmds.setAttr('%s.offset' % node, OFFSET)

OFFSET = OFFSET - 1

for obj in objs:
    cmds.connectAttr('%s.out' % node, '%s.%s' % (obj, CHANNEL))

"""



import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import wave, struct, math

class AudioNode(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000001)
    
    aBase = OpenMaya.MObject()
    aOffset = OpenMaya.MObject()
    aMultiplier = OpenMaya.MObject()

    aTime = OpenMaya.MObject()
    aNoise = OpenMaya.MObject()
    aOutput = OpenMaya.MObject()
    aData = []

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        """
        waveFile = wave.open("C:/Users/Griffy/Google Drive/RG_ARTTOOLS/PythonWaveExp/drumTest.wav", 'rb')

        length = waveFile.getnframes()

        for i in range(0,length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            temp = (int(data[0]) - 128) / 128
            AudioNode.aData.append(20 * math.log10( abs(temp) + 1))

        waveFile.close()
        """
    def compute(self, plug, data):
        if plug != AudioNode.aOutput:
            return OpenMaya.MStatus.kUnknownParameter

        timeData = data.inputValue(AudioNode.aTime)
        tempTime = timeData.asTime()

        length = len(AudioNode.aData)  - 1

        frame = int( tempTime.asUnits(OpenMaya.MTime.kFilm) )
        if frame < 0: frame = 0

        hOutput = data.outputValue(AudioNode.aOutput)

        offset = data.inputValue(AudioNode.aOffset).asInt()

        element = (frame + offset) * 1900
        if element > length: element = length

        value = abs(AudioNode.aData[element])
        multiplier =  data.inputValue(AudioNode.aMultiplier).asFloat()
        base =  data.inputValue(AudioNode.aMultiplier).asFloat()

        noise = data.outputValue(AudioNode.aBase).asFloat()

        if value < noise:
            value = 0

        hOutput.setFloat(base + (value * multiplier))

        data.setClean(plug) 

        return OpenMaya.MStatus.kSuccess


def creator():
    return OpenMayaMPx.asMPxPtr(AudioNode())

def initialize():
    print "AudioNode initialized."

    nAttr = OpenMaya.MFnNumericAttribute()

    AudioNode.aOutput = nAttr.create('output', 'out', OpenMaya.MFnNumericData.kFloat)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    AudioNode.addAttribute(AudioNode.aOutput)

    AudioNode.aBase = nAttr.create('base', 'bs', OpenMaya.MFnNumericData.kFloat, 0.0)
    nAttr.setKeyable = (True)
    AudioNode.addAttribute(AudioNode.aBase)

    AudioNode.aOffset = nAttr.create('offset', 'of', OpenMaya.MFnNumericData.kInt)
    nAttr.setKeyable = (True)
    AudioNode.addAttribute(AudioNode.aOffset)

    AudioNode.aMultiplier = nAttr.create('multiplier', 'mu', OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.setKeyable = (True)
    AudioNode.addAttribute(AudioNode.aMultiplier)

    AudioNode.aNoise = nAttr.create('noise', 'ns', OpenMaya.MFnNumericData.kFloat, 20.0)
    nAttr.setKeyable = (True)
    AudioNode.addAttribute(AudioNode.aNoise)

    unitAttr = OpenMaya.MFnUnitAttribute()

    AudioNode.aTime = unitAttr.create('time', 'tm', OpenMaya.MFnUnitAttribute.kTime, 0.0)
    AudioNode.addAttribute(AudioNode.aTime)
    AudioNode.attributeAffects(AudioNode.aTime, AudioNode.aOutput)

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, "Ryan Griffin", '1.0', 'Any')
    try:
        plugin.registerNode('audioNode', AudioNode.kPluginNodeId, creator, initialize)
    except:       
        raise RuntimeError, 'Failed to register node'

def uninitializePlugin(obj):
    print "AudioNodePlugin initialized."
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(AudioNode.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to deregister node'