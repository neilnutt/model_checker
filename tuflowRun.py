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
        self.textEditor = 'C:\\Program Files (x86)\\Notepad++\\notepad++.exe'

        self.tcfFileLabel = wx.StaticText(self, -1, ".tcf file" ) 
        self.tbcFileLabel = wx.StaticText(self, -1, ".tbc file" )
        self.bc_db_fileLabel = wx.StaticText(self, -1, "bc database" )  
        self.tgcFileLabel = wx.StaticText(self, -1, ".tgc file") 
        self.tmfFileLabel= wx.StaticText(self, -1, ".tmf file")
        self.ecfFileLabel = wx.StaticText(self, -1, ".ecf file") 
        self.projectionLabel = wx.StaticText(self, -1, "Projection")
        
        self.nwk_ndsLabel = wx.StaticText(self, -1, "Network nodes" )
        self.nwk_linesLabel = wx.StaticText(self, -1, "Network lines" )
        self.wllLabel = wx.StaticText(self, -1, ".wll file" )
         
        self.results_dirLabel = wx.StaticText(self, -1, "Results dir" ) 
        self.tlfFileLabel = wx.StaticText(self, -1, ".tlf file" ) 
        self.log_dirLabel = wx.StaticText(self, -1, "Log dir" ) 
        self.check_dirLabel = wx.StaticText(self, -1, "Check dir" )

        self.results_formatLabel = wx.StaticText(self, -1, "Results format" )
        self.results_variablesLabel = wx.StaticText(self, -1, "Results variables" )
      
        self.resultsFileLabel = wx.StaticText(self, -1, "Results file" )
        self.inFileTimeLabel = wx.StaticText(self, -1, "Input file last edit" )
        self.resultsTimeLabel = wx.StaticText(self, -1, "Results write time" )
        self.resultsSizeLabel = wx.StaticText(self, -1, "Results size" )
        self.cpuTimeLabel = wx.StaticText(self, -1, "CPU time" )
        self.setupWarningsLabel = wx.StaticText(self, -1, "Setup warnings" )
        self.runWarningsLabel = wx.StaticText(self, -1, "Run warnings" )
        self.peakInflowLabel = wx.StaticText(self, -1, "Peak inflow" )
        self.peakOutflowLabel = wx.StaticText(self, -1, "Peak outflow" )         
        self.finalCumulativeMBLabel = wx.StaticText(self, -1, "Final cumulative MB (%)" )
        self.peakCumulativeMBLabel = wx.StaticText(self, -1, "Peak cumulative MB (%)" )      
 
        self.tcfFile = wx.TextCtrl(self, -1, "-",size=(800,20))
        self.tbcFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.bc_db_file = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.tgcFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.tmfFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.ecfFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.projection = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY) 
        
        self.nwk_nds = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.nwk_lines = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.wll = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)            

        self.results_dir = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.tlfFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.log_dir = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.check_dir = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)

        self.resultsFile = wx.TextCtrl(self, -1, "-",size=(800,20), style =wx.TE_READONLY)
        self.results_format = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.results_variables = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        
        self.inFileTime = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.resultsTime = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.resultsSize = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.cpuTime = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.setupWarnings = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.runWarnings = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.peakInflow = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.peakOutflow = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.finalCumulativeMB = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
        self.peakCumulativeMB = wx.TextCtrl(self, -1, "-",size=(400,20), style =wx.TE_READONLY)
          
        self.tcfFile_btn = wx.Button(self, -1, '...')
        self.tcfFileEdit_btn = wx.Button(self, -1, 'Edit') 
        self.tmfFileEdit_btn = wx.Button(self, -1, 'Edit') 
        self.tbcFileEdit_btn = wx.Button(self, -1, 'Edit') 
        self.tgcFileEdit_btn = wx.Button(self, -1, 'Edit')
        self.ecfFileEdit_btn = wx.Button(self, -1, 'Edit') 
        
        #  Assign actions to buttons
        self.tcfFile_btn.Bind(wx.EVT_BUTTON, self.changeTcf)
        self.tcfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTcf)
        self.tmfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTmf)
        self.tbcFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTbc)
        self.tgcFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTgc)
        self.ecfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editEcf)
        
        # use gridbagsizer for layout of widgets
        sizer = wx.GridBagSizer(vgap=2, hgap=10)
        
        sizer.Add(self.tcfFileLabel,pos=(0,0))
        sizer.Add(self.tbcFileLabel,pos=(1,0))        
        sizer.Add(self.bc_db_fileLabel,pos=(2,0)) 
        sizer.Add(self.tgcFileLabel,pos=(3,0)) 
        sizer.Add(self.tmfFileLabel,pos=(4,0)) 
        sizer.Add(self.ecfFileLabel,pos=(5,0)) 
        sizer.Add(self.projectionLabel,pos=(6,0)) 
        
        sizer.Add(self.nwk_ndsLabel,pos=(7,0))
        sizer.Add(self.nwk_linesLabel,pos=(8,0))
        sizer.Add(self.wllLabel,pos=(9,0))
        
        sizer.Add(self.results_dirLabel,pos=(10,0))
        sizer.Add(self.tlfFileLabel,pos=(11,0))
        sizer.Add(self.log_dirLabel,pos=(12,0))
        sizer.Add(self.check_dirLabel,pos=(13,0))

        sizer.Add(self.resultsFileLabel,pos=(14,0))
        sizer.Add(self.results_formatLabel,pos=(15,0))
        sizer.Add(self.results_variablesLabel,pos=(16,0))
        
        sizer.Add(self.inFileTimeLabel,pos=(17,0))
        sizer.Add(self.resultsTimeLabel,pos=(18,0))
        sizer.Add(self.resultsSizeLabel,pos=(19,0))
        sizer.Add(self.cpuTimeLabel,pos=(20,0))
        sizer.Add(self.setupWarningsLabel,pos=(21,0))
        sizer.Add(self.runWarningsLabel,pos=(22,0))
        sizer.Add(self.peakInflowLabel,pos=(23,0))
        sizer.Add(self.peakOutflowLabel,pos=(24,0))
        sizer.Add(self.finalCumulativeMBLabel,pos=(25,0))
        sizer.Add(self.peakCumulativeMBLabel,pos=(26,0))
                 

        sizer.Add(self.tcfFile,pos=(0,1),span=(1,2))
        sizer.Add(self.tbcFile,pos=(1,1),span=(1,2))        
        sizer.Add(self.bc_db_file,pos=(2,1),span=(1,2)) 
        sizer.Add(self.tgcFile,pos=(3,1),span=(1,2)) 
        sizer.Add(self.tmfFile,pos=(4,1),span=(1,2)) 
        sizer.Add(self.ecfFile,pos=(5,1),span=(1,2)) 
        sizer.Add(self.projection,pos=(6,1),span=(1,2)) 
        
        sizer.Add(self.nwk_nds,pos=(7,1),span=(1,2))
        sizer.Add(self.nwk_lines,pos=(8,1),span=(1,2))
        sizer.Add(self.wll,pos=(9,1),span=(1,2))
        
        sizer.Add(self.results_dir,pos=(10,1),span=(1,2))
        sizer.Add(self.tlfFile,pos=(11,1),span=(1,2))
        sizer.Add(self.log_dir,pos=(12,1),span=(1,2))
        sizer.Add(self.check_dir,pos=(13,1),span=(1,2))

        sizer.Add(self.resultsFile,pos=(14,1),span=(1,2))
        sizer.Add(self.results_format,pos=(15,1))
        sizer.Add(self.results_variables,pos=(16,1))
        
        sizer.Add(self.inFileTime,pos=(17,1))
        sizer.Add(self.resultsTime,pos=(18,1))
        sizer.Add(self.resultsSize,pos=(19,1))
        sizer.Add(self.cpuTime,pos=(20,1))
        sizer.Add(self.setupWarnings,pos=(21,1))
        sizer.Add(self.runWarnings,pos=(22,1))
        sizer.Add(self.peakInflow,pos=(23,1))
        sizer.Add(self.peakOutflow,pos=(24,1))
        sizer.Add(self.finalCumulativeMB,pos=(25,1))
        sizer.Add(self.peakCumulativeMB,pos=(26,1))        
       
    
        sizer.Add(self.tcfFileEdit_btn,pos=(0,4))
        sizer.Add(self.tmfFileEdit_btn,pos=(4,4))
        sizer.Add(self.tbcFileEdit_btn,pos=(1,4))
        sizer.Add(self.tgcFileEdit_btn,pos=(3,4))
        sizer.Add(self.ecfFileEdit_btn,pos=(5,4))
        
        sizer.Add(self.tcfFile_btn,pos=(0,5))
        
        self.tcfFile_btn.Bind(wx.EVT_BUTTON, self.changeTcf)
        self.tcfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTcf)
        self.tmfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTmf)
        self.tbcFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTbc)
        self.tgcFileEdit_btn.Bind(wx.EVT_BUTTON, self.editTgc)
        self.ecfFileEdit_btn.Bind(wx.EVT_BUTTON, self.editEcf)
                
        # use boxsizer to add border around sizer
        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizerAndFit(border)
        self.Fit()
    
    def editTmf(self,event):
      if os.path.isfile(self.p.tcf.tmfFile):
        subprocess.call([self.textEditor,self.p.tcf.tmfFile])
      else:
        pass
        #self.iefFileMsg.SetValue('File not found')

    def editTbc(self,event):
      if os.path.isfile(self.p.tcf.tbcFile):
        subprocess.call([self.textEditor,self.p.tcf.tbcFile])
      else:
        pass
        #self.iefFileMsg.SetValue('File not found')

    def editTgc(self,event):
      if os.path.isfile(self.p.tcf.tgcFile):
        subprocess.call([self.textEditor,self.p.tcf.tgcFile])
      else:
        pass
        #self.iefFileMsg.SetValue('File not found')

    def editEcf(self,event):
      if os.path.isfile(self.p.tcf.ecfFile):
        subprocess.call([self.textEditor,self.p.tcf.ecfFile])
      else:
        pass
        #self.iefFileMsg.SetValue('File not found')
  
    def editTcf(self,event):
      if os.path.isfile(self.p.tcf.tcfFile):
        subprocess.call([self.textEditor,self.p.tcf.tcfFile])
      else:
        pass
        #self.iefFileMsg.SetValue('File not found')      
        
         
    def changeTcf(self,event):
      """ File|Open event - Open dialog box. """
      dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                         "ISIS event file (*.tcf)|*.tcf", wx.FD_OPEN)
      if (dlg.ShowModal() == wx.ID_OK):
          self.fileName = dlg.GetFilename()
          self.dirName = dlg.GetDirectory()
          filePath=os.path.join(self.dirName,self.fileName)
          self.tcfFile.SetValue(str(os.path.join(self.dirName,self.fileName)))
          self.fname = os.path.join(self.dirName,self.fileName)
      dlg.Destroy()
      self.refreshTcf()
        
    def refreshTcf(self):
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
      self.icMsg.SetValue(self.p.ief.icMsg)
      self.tcfFileMsg.SetValue(self.p.ief.tcfFileMsg)                  