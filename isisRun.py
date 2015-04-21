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
import wx,time,os,subprocess

class Fpanel(wx.Panel):
    def __init__(self, parent,p):
        wx.Panel.__init__(self, parent)
        self.p=p
        self.dirName = ''
        self.fileName = ''
        self.iefEditor = 'C:\\Program Files (x86)\\Notepad++\\notepad++.exe'
        self.datEditor = 'C:\\isis\\bin\\Isis3.exe'
        self.iedEditor = 'C:\\isis\\bin\\Isis3.exe'

        self.iefFileLabel = wx.StaticText(self, -1, ".ief file" ) 
        self.datFileLabel = wx.StaticText(self, -1, ".dat file" )  
        self.iedFileLabel = wx.StaticText(self, -1, ".ied file") 
        self.resultsDirLabel= wx.StaticText(self, -1, "Results dir")
        self.icLabel = wx.StaticText(self, -1, "Initial conditions") 
        self.tcfFileLabel = wx.StaticText(self, -1, ".tcf file")
        
        self.runTypeLabel = wx.StaticText(self, -1, "Run type" ) 
        self.startLabel = wx.StaticText(self, -1, "Start time" ) 
        self.finishLabel = wx.StaticText(self, -1, "Finish end" ) 
        self.timestepLabel = wx.StaticText(self, -1, "1D timestep" ) 
        self.timestep2DLabel = wx.StaticText(self, -1, "2D timestep" )
        
        self.zznFileLabel = wx.StaticText(self, -1, ".zzn file" )
        self.lastEditTime1DLabel = wx.StaticText(self, -1, "1D last edit" )
        self.zznTimeLabel = wx.StaticText(self, -1, ".zzn write time" )
        self.zznSizeLabel = wx.StaticText(self, -1, ".zzn size" )
        self.zzdMessageLabel = wx.StaticText(self, -1, ".zzd message" )       

        self.iefFile = wx.TextCtrl(self, -1, "-",size=(800,20))
        self.datFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.iedFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.resultsDir = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.ic = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.tcfFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.zznFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)        
 
        self.iefFileMsg = wx.TextCtrl(self, -1, "-",size=(100,20))
        self.datFileMsg = wx.TextCtrl(self, -1, "-",size=(100,20), style =wx.TE_READONLY)
        self.iedFileMsg = wx.TextCtrl(self, -1, "-",size=(100,20), style =wx.TE_READONLY)
        self.resultsDirMsg = wx.TextCtrl(self, -1, "-",size=(100,20), style =wx.TE_READONLY)
        self.icMsg = wx.TextCtrl(self, -1, "-",size=(100,20), style =wx.TE_READONLY)
        self.tcfFileMsg = wx.TextCtrl(self, -1, "-",size=(100,20), style =wx.TE_READONLY)
        
        self.runType = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.start = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.finish = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.timestep = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.timestep2D = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY) 

        self.lastEditTime1D = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.zznTime = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.zznSize = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.zzdMessage = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
          
        self.iefFile_btn = wx.Button(self, -1, '...')
        self.iefFileEdit_btn = wx.Button(self, -1, 'Edit')
        self.datFileEdit_btn = wx.Button(self, -1, 'Edit')
        self.iedFileEdit_btn = wx.Button(self, -1, 'Edit')  
        
        #  Assign actions to buttons
        self.iefFile_btn.Bind(wx.EVT_BUTTON, self.changeIef)
        self.iefFileEdit_btn.Bind(wx.EVT_BUTTON, self.editIef)
        self.datFileEdit_btn.Bind(wx.EVT_BUTTON, self.editIed)
        
        # use gridbagsizer for layout of widgets
        sizer = wx.GridBagSizer(vgap=2, hgap=10)
        
        sizer.Add(self.iefFileLabel,pos=(0,0))
        sizer.Add(self.datFileLabel,pos=(1,0))
        sizer.Add(self.iedFileLabel,pos=(2,0))
        sizer.Add(self.resultsDirLabel,pos=(3,0))
        sizer.Add(self.icLabel,pos=(4,0))
        sizer.Add(self.tcfFileLabel,pos=(5,0))
        sizer.Add(self.zznFileLabel,pos=(6,0)) 
        
        sizer.Add(self.runTypeLabel,pos=(8,0))
        sizer.Add(self.startLabel,pos=(9,0))
        sizer.Add(self.finishLabel,pos=(10,0))
        sizer.Add(self.timestepLabel,pos=(11,0))
        sizer.Add(self.timestep2DLabel,pos=(12,0))
        
        sizer.Add(self.zzdMessageLabel,pos=(14,0))
        sizer.Add(self.lastEditTime1DLabel,pos=(15,0))
        sizer.Add(self.zznTimeLabel,pos=(16,0))
        sizer.Add(self.zznSizeLabel,pos=(17,0))       
        
        sizer.Add(self.iefFile,pos=(0,1),span=(1,2))
        sizer.Add(self.datFile,pos=(1,1),span=(1,2))
        sizer.Add(self.iedFile,pos=(2,1),span=(1,2))
        sizer.Add(self.resultsDir,pos=(3,1),span=(1,2))
        sizer.Add(self.ic,pos=(4,1),span=(1,2))
        sizer.Add(self.tcfFile,pos=(5,1),span=(1,2))
        sizer.Add(self.zznFile,pos=(6,1))      
 
        sizer.Add(self.iefFileMsg,pos=(0,3))  
        sizer.Add(self.datFileMsg,pos=(1,3))  
        sizer.Add(self.iedFileMsg,pos=(2,3))  
        sizer.Add(self.resultsDirMsg,pos=(3,3))  
        sizer.Add(self.icMsg,pos=(4,3))  
        sizer.Add(self.tcfFileMsg,pos=(5,3))        
        
        sizer.Add(self.runType,pos=(8,1))
        sizer.Add(self.start,pos=(9,1))
        sizer.Add(self.finish,pos=(10,1))
        sizer.Add(self.timestep,pos=(11,1))
        sizer.Add(self.timestep2D,pos=(12,1))           

        sizer.Add(self.zzdMessage,pos=(14,1))
        sizer.Add(self.lastEditTime1D,pos=(15,1))
        sizer.Add(self.zznTime,pos=(16,1))
        sizer.Add(self.zznSize,pos=(17,1))        
    
        sizer.Add(self.iefFileEdit_btn,pos=(0,4))
        sizer.Add(self.datFileEdit_btn,pos=(1,4))
        sizer.Add(self.iedFileEdit_btn,pos=(2,4))
        
        sizer.Add(self.iefFile_btn,pos=(0,5))
                
        # use boxsizer to add border around sizer
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizerAndFit(border)
        self.Fit()
    
    def editIef(self,event):
      if os.path.isfile(self.p.ief.iefFile):
        subprocess.call([self.iefEditor,self.p.ief.iefFile])
      else:
        self.iefFileMsg.SetValue('File not found')

    def editDat(self,event):
      if os.path.isfile(self.p.ief.datFile):
        subprocess.call([self.datEditor,self.p.ief.datFile])
      else:
        self.datFileMsg.SetValue('File not found')

    def editIed(self,event):
      if os.path.isfile(self.p.ief.iedFile):
        subprocess.call([self.datEditor,self.p.ief.iedFile])
      else:
        self.iedFileMsg.SetValue('File not found')
        
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
      self.ic.SetValue(self.p.ief.icFile)
      self.resultsDir.SetValue(self.p.ief.resultLocation)
      self.tcfFile.SetValue(self.p.ief.tcfFile)
      
      self.runType.SetValue(self.p.ief.runType)
      self.start.SetValue(self.p.ief.start)
      self.finish.SetValue(self.p.ief.finish)
      self.timestep.SetValue(self.p.ief.timestep)
      self.timestep2D.SetValue(self.p.ief.timestep2D)
  
      self.zznFile.SetValue(self.p.ief.zznFile)
      self.lastEditTime1D.SetValue(str(time.ctime(self.p.ief.lastEditTime1D)))
      self.zznTime.SetValue(str(time.ctime(self.p.ief.zznTime)))
      self.zznSize.SetValue(self.p.ief.zznSize)
      self.zzdMessage.SetValue(self.p.ief.zzdMessage) 
        
      self.iefFileMsg.SetValue(self.p.ief.iefFileMsg)
      self.datFileMsg.SetValue(self.p.ief.datFileMsg)
      self.iedFileMsg.SetValue(self.p.ief.iedFileMsg)
      self.resultsDirMsg.SetValue(self.p.ief.resultsDirMsg)
      self.icMsg.SetValue(self.p.ief.icFileMsg)
      self.tcfFileMsg.SetValue(self.p.ief.tcfFileMsg)                  