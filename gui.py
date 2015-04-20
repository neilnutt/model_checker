# -*- coding: utf-8 -*-

# Copyright (c) 2014  Neil Nutt <neilnutt@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Current package imports
import wx
import os
import isisRun
import tuflowRun
import linkage
import model_checker


class MainFrame(wx.Frame):
  def __init__(self,parent):
      super(MainFrame, self).__init__(parent,title="ISIS-Tuflow checker",size=(700,760))

      # --- initialize other settings
      self.dirName = ""
      self.fileName = ""
      self.windowName = 'Main Window'
      self.SetName(self.windowName)
      
      self.ief = model_checker.IefCheck()
      self.tcf = model_checker.TcfCheck()
      
      self.InitUI()
      self.Centre()
      self.Show()


  def InitUI(self):
        self.panel = wx.Panel(self,-1)
        self.Maximize(True)
      
        menubar = wx.MenuBar()

        #  Defining the file menu
        fileMenu = wx.Menu()
        #mN = wx.MenuItem(fileMenu, wx.ID_NEW, '&New\tCtrl+N')
        #mO = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Open\tCtrl+O')
        #mSA = wx.MenuItem(fileMenu, wx.ID_SAVEAS, '&Save as\tCtrl+ALT+S')
        #mS = wx.MenuItem(fileMenu, wx.ID_SAVE, '&Save\tCtrl+S')
        #fileMenu.Append(mO)
        #fileMenu.Append(mS)
        #fileMenu.Append(mSA)
        #fileMenu.AppendSeparator()
        #mQ = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        #fileMenu.Append(mQ)
        #self.Bind(wx.EVT_MENU, self.OnFileOpen, mO)
        #self.Bind(wx.EVT_MENU, self.OnFileSave, mS)
        #self.Bind(wx.EVT_MENU, self.OnFileSaveAs, mSA)
        #self.Bind(wx.EVT_MENU, self.OnQuit, mQ)
 
        
        # Defining the help menu
        #helpMenu = wx.Menu()
        #mAbout = wx.MenuItem(helpMenu, wx.ID_ABOUT, '&About')
        #helpMenu.Append(mAbout)
        #self.Bind(wx.EVT_MENU, self.OnAbout, mAbout)
         
        # Applying menus to the menu bar
        #menubar.Append(fileMenu, '&File')
        #menubar.Append(helpMenu,'&Help')


        self.SetMenuBar(menubar)


        # Here we create a notebook on the panel
        nb = wx.Notebook(self.panel)

        # create the page windows as children of the notebook
        self.page1 = isisRun.Fpanel(nb,self)
        self.page2 = tuflowRun.Fpanel(nb,self.page1)
        self.page3 = linkage.Fpanel(nb,self.page1)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.page1, "ISIS model")
        nb.AddPage(self.page2, "Tuflow model")
        nb.AddPage(self.page3, "Linkage")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        

        self.panel.Layout()
        self.Layout()
        self.Refresh()
    
  def OnPageChanging(self,e):
      #self.Refresh()
      #self.Update()
      e.Skip()
      
  def OnPageChanged(self,e):
      #self.page2.title_label.SetLabel(str(self.page1.title.GetValue()))
      #self.Refresh()
      #self.Update()
      e.Skip() 
        

  def OnAbout(self, e):
        
        description = """        The Statistical Flood Estimation Tool is a means of implementing current statistical
        procedures for estimating the magnitude of flood flows in the United Kingdom using the methods 
        detailed in the Flood Estimation Handbook and subsequent updates.  It has been developed by the not
        for profit Open Hydrology (OH) community of software developers.  The software makes extensive use 
        of the floodestimation library which is also developed by OH.
        
        This is an early development version, it is intended that additional features will be implemented in 
        the coming months and years.
        
        
"""

        licence = """The Statistical Flood Estimation Tool is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 2 of the License, 
or (at your option) any later version.

The Statistical Flood Estimation Tool is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  02111-1307  USA

EXCEPTION CLAUSE:

A. Organisations (commercial, academic, educational, private individual or
  any other body) must publicly state via this software project's website
  that they have undertaken a validation process of this software prior to 
  its use.  In submitting their public declaration, organisations should 
  provide details of the findings of their review including any caveats or
  exclusions of use.  Organisations must record errors or bugs they find within
  the project's online issue tracking system within its GitHub repository. 
  This exclusion of use permits reasonable use of the software by organisations
  for testing and validation.
  
  Software project website:
  https://github.com/OpenHydrology/StatisticalFloodEstimationTool/wiki


"""

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon('..\\art\\OH.darkgrey.250x250.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Statistical Flood Estimation Tool')
        info.SetVersion('Pre-release 0.0.2')
        info.SetDescription(description)
        info.SetCopyright('(C) 2015 Open Hydrology developer community')
        info.SetWebSite('https://github.com/OpenHydrology/model_checker')
        info.SetLicence(licence)
        info.AddDeveloper('Neil Nutt - Project Founder - neilnutt[at]googlemail[dot]com')
        info.AddDeveloper('\nFlorenz Hollebrandse - Developer - f.a.p.hollebrandse[at]protonmail[dot]ch')
        info.AddDeveloper('\nMichael Spencer - Communications - spencer.mike.r[at]gmail[dot]com')

        wx.adv.AboutBox(info)

  def OnPreferences(self,e):
      '''
      Load up preferences screen
      '''
      pass


  def OnFileOpen(self, e):
        """ File|Open event - Open dialog box. """
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Project directory (*.ini)|*.ini;*.ohp|Project archive (*.ohp)|*.ini;*.ohp", wx.FD_OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            filePath=os.path.join(self.dirName,self.fileName)
            load_project(filePath,self)


        dlg.Destroy()

#---------------------------------------
  def OnFileSave(self, e):
        """ File|Save event - Just Save it if it's got a name. """

        if (self.fileName != "") and (self.dirName != ""):
          saveFile = os.path.join(self.dirName,self.fileName)
          save_project(self,c.analysis.catchment,saveFile)

        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnFileSaveAs(e)

#---------------------------------------
  def OnFileSaveAs(self, e):
        """ File|SaveAs event - Prompt for File Name. """
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, self.fileName,
                           "Project directory (*.ini)|*.ini;*.ohp|Project archive (*.ohp)|*.ini;*.ohp", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.OnFileSave(e):
                self.SetTitle(self.fileName)
                ret = True
        dlg.Destroy()
        return ret
        
  def OnQuit(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()


if __name__ == "__main__":
    app = wx.App(redirect=False)
    #app = wx.App(redirect=True,filename='error_log.txt')
    MainFrame(None).Show()
    app.MainLoop()
