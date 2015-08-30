''' 
Created by Neil Nutt without any warranty 
v0.0.1
''' 
import os,time
import check_1d2d_linkage


def identifyFileType(filePath):
  filePath = filePath.lower()
  fileName = os.path.split(filePath)[-1]
  print fileName
  ief = IefCheck()
  tcf = TcfCheck() 
  
  if fileName.endswith('.ief'):

    
    ief.checkIef(filePath)
    for error in ief.iefErrors:
      print error

    if ief.tcfFile != 'None':
      tcf.checkTcf(ief.tcfFile)
      
      for error in tcf.tcfErrors:
        print error

      if tcf.nwk_nds != 'None':
        notFoundReaches,notFoundNodes = check_1d2d_linkage.checkLinkage(tcf.nwk_nds, tcf.nwk_lines, ief.datFile)
      
        print "Following reaches not found in ISIS dat",notFoundReaches
        print "Following nodes not found in ISIS dat",notFoundNodes

  elif fileName.endswith('.tcf'):
    tcf.checkTcf(filePath)
    
    for error in tcf.tcfErrors:
      print error
  #  for item in tcf.tcfParameters:
  #    print item, tcf.tcfParameters[item]
  else:
    print 'File type not recognised:',fileName
  
  print(filePath+'_log.csv')
  f = open(filePath+'_log.csv','w')
  f.write('iefFile'+', '+filePath+'\n')
  f.write('datFile'+', '+ief.datFile+'\n')
  f.write('iedFile'+', '+ief.iedFile+'\n')
  f.write('iCsFrom'+', '+ief.iCsFrom+'\n')
  f.write('zznFile'+', '+ief.zznFile+'\n') 
  f.write('start'+', '+ief.start+'\n') 
  f.write('finish'+', '+ief.finish+'\n') 
  f.write('timestep'+', '+ief.timestep+'\n')
  f.write('2DTimestep'+', '+ief.timestep2D+'\n')
  f.write('tcfFile'+', '+ief.tcfFile+'\n')
  
  if ief.tcfFile != 'None':
    f.write('filepath'+', '+tcf.filepath+'\n')
    f.write('projection'+', '+tcf.projection+'\n')
    f.write('tbcFile'+', '+tcf.tbcFile+'\n')
    f.write('tgcFile'+', '+tcf.tgcFile+'\n')
    f.write('tmfFile'+', '+tcf.tmfFile+'\n')
    f.write('bc_db_file'+', '+tcf.bc_db_file+'\n')
    f.write('nwk_nds'+', '+tcf.nwk_nds+'\n')
    f.write('nwk_lines'+', '+tcf.nwk_lines+'\n')
    f.write('wll'+', '+tcf.wll+'\n')
    f.write('log_dir'+', '+tcf.log_dir+'\n')
    f.write('results_dir'+', '+tcf.results_dir+'\n')
    f.write('check_dir'+', '+tcf.check_dir+'\n')
    f.write('\n')
  
  f.write('zznTime'+', '+ief.zznTime+'\n')
  if ief.tcfFile != 'None':
    f.write('2D results time'+', '+tcf.resultsTimestamp+'\n')
  
  f.write('zznSize (MB)'+', '+ief.zznSize+'\n')
  if ief.tcfFile != 'None':
    f.write('2D results size (MB)'+', '+tcf.resultsSize+'\n')
    f.write('2DcpuTime'+', '+tcf.cpuTime+'\n')
    f.write('2DsetupWarnings'+', '+tcf.setupWarnings+'\n')
    f.write('2DrunWarnings'+', '+tcf.runWarnings+'\n')
    f.write('2DpeakInflow'+', '+tcf.peakInflow+'\n')
    f.write('2DpeakOutflow'+', '+tcf.peakOutflow+'\n')
    f.write('2DfinalCumulativeMB'+', '+tcf.finalCumulativeMB+'\n')
    f.write('2DpeakCumulativeMB'+', '+tcf.peakCumulativeMB+'\n')
  

class IefCheck():
  def __init__(self):
    self.iefErrors = list()
    
    self.iefFile = 'None'
    self.datFile = 'None'
    self.runType = 'None'
    self.start = 'None'
    self.finish = 'None'
    self.timestep = 'None'
    self.iCsFrom = ''
    self.icFile = ''
    self.iedFile = 'None'
    self.resultLocation = 'None'
    self.zznFile = 'None'
    self.zznSize = 'None'
    self.zznTime = 'None'
    self.zzdFile = 'None'
    self.zznFile = 'None'
    self.timestep2D  = 'None'
    self.tcfFile = 'None'
    self.lastEditTime1D = 0
    self.zzdMessage = 'None'

    self.iefFileMsg= 'None'
    self.datFileMsg ='None'
    self.iedFileMsg = 'None'
    self.resultsDirMsg = 'None'
    self.icFileMsg = 'From steady state results'
    self.tcfFileMsg = 'None'   
  
  def checkIef(self,filePath):
    print "Starting to check:",filePath
    if os.path.isfile(filePath) == False:
      print "File doesn't exist:", filePath
      return 1 

    os.chdir(os.path.split(filePath)[0])
    
    if os.path.isfile(filePath):
      if os.path.getmtime(filePath) > self.lastEditTime1D:
        self.lastEditTime1D = os.path.getmtime(filePath)
    else:
      self.iefFileMsg = 'File not found'
    
    f = open(filePath)
    
    self.iefFile = filePath
    for line in f.readlines():
      line = line.split('\n')[0]
      if line.startswith('Datafile'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("ERROR ISIS file (.dat) doesn't exist:", fname))
          self.datFileMsg = 'File not found'
        else:
          pass # Could check the dat file, i.e. number of nodes etc
          self.datFile = fname
          if os.path.getmtime(fname) > self.lastEditTime1D:
            self.lastEditTime1D = os.path.getmtime(fname)
      elif line.startswith('Results'):
        self.zznFile = line.split('=')[-1]+'.zzn'
        self.zzdFile = line.split('=')[-1]+'.zzd'
        dirName = os.path.split(line.split('=')[-1])[0]
        self.resultLocation = dirName
        if ':' not in dirName: ##then it is relative to the cwd and need to convert to abs  
          self.resultLocation = os.path.join(os.path.split(self.iefFile)[0],self.resultLocation)
        elif os.path.isdir(dirName)==False:
          self.iefErrors.append(("Results location doesn't exist:", dirName))
          self.resultsDirMsg = 'Directory not found'
        else:
          # Check you have write premission at this location
          try:
            temp = os.path.join(self.resultLocation,'model_checker_temp_safe_to_delete')
            t = open(temp,'w')
            t.write('model_checker_temp_file_safe_to_delete')
            t.close()
            os.unlink(temp)
          except:
            self.resltsDirMsg = 'No write access'

        if os.path.isfile(self.zznFile):
          self.zznTime = os.path.getmtime(self.zznFile)
          self.zznSize = str(round(os.path.getsize(self.zznFile)/1024/1024.0),2)
        
        if os.path.isfile(self.zzdFile):
          d = open(self.zzdFile)
          self.zzdMessage = 'run not completed'
          for dline in d:
            if dline.startswith('run completed'):
              self.zzdMessage = 'run completed'
          d.close()
    
            
      elif line.startswith('Timestep'):
        self.timestep = line.split('=')[-1]
      elif line.startswith('RunType'):
        self.runType= line.split('=')[-1]
      elif line.startswith('2DTimestep'):
        self.timestep2D = line.split('=')[-1]  
      elif line.startswith('ICsFrom'):
        id=line.split('=')[-1]
        if id == '1':
          #self.iCsFrom = 'From dat file'
          self.icFileMsg = 'From dat file'
        id=line.split('=')[-1]
        if id == '2':
          #self.iCsFrom = 'From file'
          self.icFileMsg = 'From file'
      elif line.startswith('InitialConditions'):
        fname  = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        self.icFile = fname
        if os.path.isfile(self.icFile):
          if os.path.getmtime(self.icFile) > self.lastEditTime1D:
              self.lastEditTime1D = os.path.getmtime(self.icFile)
      elif line.startswith('Start'):
        self.start = line.split('=')[-1]
      elif line.startswith('Finish'):
        self.finish = line.split('=')[-1]
      elif line.startswith('EventData'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        self.iedFile = fname          
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("Event data file (.ied) doesn't exist:", fname))
          self.iedFileMsg = 'File not found'
        else:
          pass # could check that the nodes listed in the ied exist in the dat
          if os.path.getmtime(fname) > self.lastEditTime1D:
            self.lastEditTime1D = os.path.getmtime(fname)
          
      elif line.startswith('2DFile'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        self.tcfFile = fname
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("2D file (.tcf) doesn't exist:", fname))
          self.tcfFileMsg = 'File not found'
        if os.path.getmtime(fname) > self.lastEditTime1D:
            self.lastEditTime1D = os.path.getmtime(fname)
          
    if len(self.iefErrors)== 0:
      print "No errors found in ief"
    else:
      print len(self.iefErrors)," errors found in ief"
      
    
    

  
  
class TcfCheck():
  def __init__(self):
    self.tcfErrors = list()
    self.filepath = 'None'
    self.projection = 'None'
    self.tbcFile =  'None'
    self.tgcFile = 'None'
    self.tmfFile =  'None'
    self.bc_db_file = 'None'
    self.nwk_nds = 'None'
    self.nwk_lines = 'None'
    self.wll = 'None'
    self.log_dir = 'None'
    self.results_dir = 'None'
    self.check_dir = 'None'
    self.generic_read = 'None'
    self.resolution = 'None'
    self.timestep = 'None'
    self.start = 'None'
    self.end = 'None'
    self.results_format = 'None'
    self.results_variables = 'None'
    self.resultsTimestamp = 'None'
    self.resultsSize = 'None'
    
    self.cpuTime = 'None'
    self.setupWarnings = 'None'
    self.runWarnings = 'None'
    self.peakInflow = 'None'
    self.peakOutflow = 'None'
    self.finalCumulativeMB = 'None'
    self.peakCumulativeMB = 'None'
    
    
  def checkTcf(self,filePath):  
    print "Starting to check:",filePath
    if os.path.isfile(filePath) == False:
      self.tcfErrors.append("File doesn't exist:"+ filePath)
      print "File doesn't exist:", filePath
      return 1 
    self.filepath = os.path.split(filePath)[0]
    self.tcfFile = filePath
    
    os.chdir(os.path.split(filePath)[0])
  
    f = open(filePath)
    
    for line in f.readlines():
      line = line.split('\n')[0].lower()
      if line.startswith('!') or line.startswith('#') or len(line.replace(' ','')) == 0:
        continue
      
      line = line.split('!')[0]
      
      if line.startswith('shp projection'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR projection file (.prj) doesn't exist:", fname))
        else:
          pass # Could store the projection file and ensure all other projection files are the same
          self.projection = fname
      
      elif line.startswith('bc control file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR bc control file (.tbc) doesn't exist:", fname))
        else:
          self.tbcFile = fname
   
      elif line.startswith('geometry control file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gc control file (.tgc) doesn't exist:", fname))
        self.tgcFile = fname

      elif line.startswith('start time'):
        self.start = line.split('==')[-1].replace(' ','').rstrip()

      elif line.startswith('end time'):
        self.end = line.split('==')[-1].replace(' ','').rstrip()        

      elif line.startswith('timestep'):
        self.timestep = line.split('==')[-1].replace(' ','').rstrip()  
    
      elif line.startswith('read materials file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR materials file (.tmf) doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
          self.tmfFile = fname
   
      elif line.startswith('bc database'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR bc databse (bc*.csv) doesn't exist:", fname))
        else:
          self.bc_db_file = fname
  
      elif line.startswith('read gis isis network'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis network (1d_nwk_*_L.shp) doesn't exist:", fname))
        else:
          self.nwk_lines=fname
  
      elif line.startswith('read gis isis nodes'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis nodes (1d_nd_*_P.shp) doesn't exist:", fname))
        else:
          self.nwk_nds=fname

      elif line.startswith('read mi isis nodes'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR mi isis nodes (1d_nd_*.mif) doesn't exist:", fname))
        else:
          self.nwk_nds=fname
   
      elif line.startswith('read gis isis wll'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis wll (1d_wll_*_L.shp) doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
        self.wll = fname
        
      elif line.startswith('log folder'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]
        path = os.path.abspath(path)
        if os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR log directory doesn't exist:", path))
        else:
          pass # Could check for write access
          self.log_dir = path
   
      elif line.startswith('output folder'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]
        path = os.path.abspath(path)
        if '\\' not in path:
          self.results_dir='ief dir'
        elif os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR output directory doesn't exist:", path))
        else:
          pass # Could check for write access
          self.results_dir = path
  
      elif line.startswith('write check files'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]       
        path = os.path.abspath(path)
        if os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR check file directory doesn't exist:", path))
        else:
          pass # Could check for write access  
          self.check_dir = path
      
      elif line.startswith('map output format'):
        self.results_format = line.split('==')[-1].replace(' ','').rstrip()
      elif line.startswith('map output data types'):
        self.result_variables = line.split('==')[-1].replace(' ','').rstrip()
      
      elif line.startswith('read'):  ## Generic check of other reads
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR unidentified file doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
          self.generic_read = 'Used'
    
    
    if self.results_dir is not None and self.results_format is not None:
      fname = os.path.join(self.results_dir,os.path.splitext(os.path.split(self.tcfFile)[-1])[0]+'.'+self.results_format)
      if fname.startswith('..'):
          fname = os.path.abspath(fname)
      if os.path.isfile(fname):
        self.resultsTimestamp = time.ctime(os.path.getmtime(fname))
        self.resultsSize = str(os.path.getsize(fname)/1024/1024.0)
      
    if self.log_dir is not None:
      self.tlfFile = os.path.join(self.log_dir,os.path.splitext(os.path.split(self.tcfFile)[-1])[0]+'.tlf')
      if self.tlfFile.startswith('..'):
          self.tlfFile = os.path.abspath(self.tlfFile)
      if os.path.isfile(self.tlfFile):
        f = open(self.tlfFile)
        for line in f:
          line = line.replace('\n','')
          if line.startswith('CPU Time'):
            self.cpuTime = line.split('or')[-1].rstrip().lstrip()
          if line.startswith('WARNINGs prior'):
            self.setupWarnings = line.split(':')[-1].split('[')[0].rstrip().lstrip()
          if line.startswith('WARNINGs during'):
            self.runWarnings = line.split(':')[-1].split('[')[0].rstrip().lstrip()
          if line.startswith ('Peak Flow In'):
            self.peakInflow = line.split(':')[-1].rstrip().lstrip()
          if line.startswith('Peak Flow Out'):
            self.peakOutflow = line.split(':')[-1].rstrip().lstrip()
          if line.startswith('Final Cumulative ME'):
            self.finalCumulativeMB = line.split(':')[-1].rstrip().lstrip()
          if line.startswith('Peak Cumulative ME'):
            self.peakCumulativeMB = line.split(':')[-1][0:35].rstrip().lstrip()        
        
    if self.tbcFile is not None:
      tbcErrors = self.checkTbc(self.tbcFile,self.bc_db_file)
      for error in tbcErrors:
        self.tcfErrors.append(error)
    
    if self.tgcFile is not None:
      tgcErrors = self.checkTgc(self.tgcFile)
      for error in tgcErrors:
        self.tcfErrors.append(error)
    
    if len(self.tcfErrors)== 0:
      print "No errors found in tcf"
    else:
      print len(self.tcfErrors)," errors found in tcf"
    


  def checkTbc(self,filePath,bc_db=None): 
    print "Starting to check:",filePath
    tbcErrors = list()
    if os.path.isfile(filePath) == False:
      tbcErrors.append("File doesn't exist:", filePath)
      return 1 
    os.chdir(os.path.split(filePath)[0])
  
    
    f = open(filePath)
    
    for line in f.readlines():
      line = line.split('\n')[0].lower()
      if line.startswith('!') or line.startswith('#') or len(line.replace(' ','')) == 0:
        continue
      
      line = line.split('!')[0]
      
      if line.startswith('read'):  ## Generic check of other reads
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
            fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          tbcErrors.append(("ERROR unidentified file doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
        
    return tbcErrors


  def checkTgc(self,filePath): 
    print "Starting to check:",filePath
    tgcErrors = list()
    if os.path.isfile(filePath) == False:
      tgcErrors.append(("File doesn't exist:", filePath))
      return 1 
    
    os.chdir(os.path.split(filePath)[0])
    
    f = open(filePath)
    
    for line in f.readlines():
      line = line.split('\n')[0].lower()
      if line.startswith('!') or line.startswith('#') or len(line.replace(' ','')) == 0:
        continue
      
      line = line.split('!')[0]
      
      if line.startswith('cell size'):
        self.resolution = line.split('==')[-1].replace(' ','').rstrip()
      elif line.startswith('read'):
        if '|' in line:
          for geomFile in line.split('|'):
            fname = geomFile.split('==')[-1].replace(' ','').rstrip()
            if fname.startswith('\\'):
              fname = fname[1:]
            fname = os.path.abspath(fname)
            if os.path.isfile(fname)==False:
              tgcErrors.append(("ERROR file does not exist:", fname))
  
        else:
          fname = line.split('==')[-1].replace(' ','').rstrip()
          if fname.startswith('\\'):
            fname = fname[1:]
          absFname = os.path.abspath(fname)
          if os.path.isfile(absFname)==False:
            #print "Rel:",fname
            #print "Abs:",absFname
            tgcErrors.append(("ERROR file does not exist:", absFname))
          else:
            pass # Could check the contents of the file
        
    return tgcErrors


if __name__ == '__main__':
  from sys import argv
  if len(argv) == 1 and argv[0].lower()[-3:] != 'exe':
      filePath = r"P:\Glasgow\WNE\PROJECTS\357291-Aberfan_Weir_NRW\Hydraulics\v2.2\3 Model\1D\Proposed Model\1000yr\Defended\UpperTaff_v2.2_1D-10m-Proposedv32_0m_weir-1000yr.ief"
  elif argv[0].lower() == 'python' and len(argv) != 3:
      print 'Wrong number of parameters'
      print 'EXAMPLE:   python check_routines.py model.ief'
      print ''
  elif len(argv) != 2:
      print 'Wrong number of parameters'
      print 'EXAMPLE:   model_checker.exe model.ief'
      print ''
  else:
    filePath = argv[-1]

  if filePath is not None:
    identifyFileType(filePath)

  