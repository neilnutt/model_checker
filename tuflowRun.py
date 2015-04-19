'''
Created on 27 Apr 2014

@author: Neil Nutt, neilnutt[at]googlemail[dot]com

Front page tab for calculation, used to hold catchment title, author and checking etc

    Statistical Flood Estimation Tool
    Copyright (C) 2014  Neil Nutt, neilnutt[at]googlemail[dot]com
    https://github.com/OpenHydrology/StatisticalFloodEstimationTool

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

'''
import wx,time,os

class Fpanel(wx.Panel):
    def __init__(self, parent,p):
        wx.Panel.__init__(self, parent)
        self.p=p
        self.dirName = ''
        self.fileName = ''

        self.iefFileLabel = wx.StaticText(self, -1, ".ief file" ) 
        self.datFileLabel = wx.StaticText(self, -1, ".dat file" )  
        self.iedFileLabel = wx.StaticText(self, -1, ".ied file") 
        self.resultsDirLabel= wx.StaticText(self, -1, "Results dir")
        self.icLabel = wx.StaticText(self, -1, "Initial conditions") 
        self.tcfFileLabel = wx.StaticText(self, -1, ".tcf file")      

        self.iefFile = wx.TextCtrl(self, -1, "-",size=(800,25))
        self.datFile = wx.TextCtrl(self, -1, "-",size=(800,25), style =wx.TE_READONLY)
        self.iedFile = wx.TextCtrl(self, -1, "-",size=(800,25), style =wx.TE_READONLY)
        self.resultsDir = wx.TextCtrl(self, -1, "-",size=(800,25), style =wx.TE_READONLY)
        self.ic = wx.TextCtrl(self, -1, "-",size=(800,25), style =wx.TE_READONLY)
        self.tcfFile = wx.TextCtrl(self, -1, "-",size=(800,25), style =wx.TE_READONLY)
        
          
        self.iefFile_btn = wx.Button(self, -1, '...')
        #self.datFile_btn = wx.Button(self, -1, '...')
        #self.iedFile_btn = wx.Button(self, -1, '...')
        #self.resltsDir_btn = wx.Button(self, -1, '...')
        #self.ic_btn  = wx.Button(self, -1, '...')
        #self.tfc_btn = wx.Button(self, -1, '...')
        
        #  Assign actions to buttons
        self.iefFile_btn.Bind(wx.EVT_BUTTON, self.changeIef)

        
        # use gridbagsizer for layout of widgets
        sizer = wx.GridBagSizer(vgap=10, hgap=10)
        
        sizer.Add(self.iefFileLabel,pos=(0,0),span=(1,1))
        sizer.Add(self.datFileLabel,pos=(1,0))
        sizer.Add(self.iedFileLabel,pos=(2,0))
        sizer.Add(self.resultsDirLabel,pos=(3,0))
        sizer.Add(self.icLabel,pos=(4,0))
        sizer.Add(self.tcfFileLabel,pos=(5,0))
        
        sizer.Add(self.iefFile,pos=(0,1),span=(1,1))
        sizer.Add(self.datFile,pos=(1,1))
        sizer.Add(self.iedFile,pos=(2,1))
        sizer.Add(self.resultsDir,pos=(3,1))
        sizer.Add(self.ic,pos=(4,1))
        sizer.Add(self.tcfFile,pos=(5,1))
    
        sizer.Add(self.iefFile_btn,pos=(0,2))
                
        # use boxsizer to add border around sizer
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizerAndFit(border)
        self.Fit()
        
    def changeIef(self,event):
      """ File|Open event - Open dialog box. """
      dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                         "ISIS event file (*.ief)|*.ief", wx.FD_OPEN)
      if (dlg.ShowModal() == wx.ID_OK):
          self.fileName = dlg.GetFilename()
          self.dirName = dlg.GetDirectory()
          filePath=os.path.join(self.dirName,self.fileName)
          self.iefFile.SetValue(str(os.path.join(self.dirName,self.fileName)))
          self.fname = os.path.join(self.dirName,self.fileName)
      dlg.Destroy()
      self.refreshIef()
        
    def refreshIef(self):
      self.p.ief.checkIef(self.fname)
      self.datFile.SetValue(self.p.ief.datFile)
      self.iedFile.SetValue(self.p.ief.iedFile)
      self.ic.SetValue(self.p.ief.iCsFrom)
      self.resultsDir.SetValue(self.p.ief.resultLocation)
      self.tcfFile.SetValue(self.p.ief.tcfFile)
      