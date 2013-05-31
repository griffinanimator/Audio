import maya.cmds as cmds
import os

class Audio_UI:
          
    def __init__(self):

        """ Create a dictionary to store UI elements """
        self.UIElements = {}
        
        """ Check to see if the UI exists """
        self.windowName = "AudioWindow"
        if cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName)
        """ Define UI elements width and height """    
        self.windowWidth = 120
        self.windowHeight = 200
        buttonWidth = 100
        buttonHeight = 30

        """ Define a window"""
        self.UIElements["window"] = cmds.window(self.windowName, width=self.windowWidth, height=self.windowHeight, title="AudioWindow", sizeable=True)
        
        self.UIElements["rowColumnLayout"] = cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 120)], cs=[2, 10] )
       
        """ Use a flow layout for the  UI """
        self.UIElements["guiFlowLayout"] = cmds.flowLayout(v=True, width=110, height=self.windowHeight, bgc=[0.4, 0.4, 0.4])
        cmds.setParent(self.UIElements["rowColumnLayout"])

        # Alternative way to make buttons
        self.UIElements["audioNodeButton"] = cmds.button(c=self.createAudioNode)

        """ Show the window"""
        cmds.showWindow(self.windowName)

    def createAudioNode(self, *args):
        # Create an audio node
        cmds.createNode('audioNode')