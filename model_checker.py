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
    #for item in ief.iefParameters:
    #  print item, ief.iefParameters[item]

    if ief.iefParameters['tcfFile'] is not None:
      tcf.checkTcf(ief.iefParameters['tcfFile'])
      
      for error in tcf.tcfErrors:
        print error
      #for item in tcf.tcfParameters:
      #  print item, tcf.tcfParameters[item]

      notFoundReaches,notFoundNodes = check_1d2d_linkage.checkLinkage(tcf.tcfParameters['nwk_nds'], tcf.tcfParameters['nwk_lines'], ief.iefParameters['datFile'])
      
      print "Following reaches not found in ISIS dat",notFoundReaches
      print "Following nodes not found in ISIS dat",notFoundNodes

  elif fileName.endswith('.tcf'):
    tcf.checkTcf(filePath)
    
    for error in tcf.tcfErrors:
      print error
    for item in tcf.tcfParameters:
      print item, tcf.tcfParameters[item]
  else:
    print 'File type not recognised:',fileName
  
  print(filePath+'_log.csv')
  f = open(filePath+'_log.csv','w')
  for i in ief.iefParameters:
    print (i)
  f.write('iefFile'+', '+filePath+'\n')
  f.write('datFile'+', '+ief.iefParameters['datFile']+'\n')
  f.write('iedFile'+', '+ief.iefParameters['iedFile']+'\n')
  f.write('ic'+', '+ief.iefParameters['ic']+'\n')
  f.write('zznFile'+', '+ief.iefParameters['zznFile']+'\n') 
  f.write('zznTime'+', '+ief.iefParameters['zznTime']+'\n')
  f.write('zznSize'+', '+ief.iefParameters['zznSize']+'\n')
  f.write('start'+', '+ief.iefParameters['start']+'\n') 
  f.write('finish'+', '+ief.iefParameters['finish']+'\n') 
  f.write('timestep'+', '+ief.iefParameters['timestep']+'\n')
  f.write('2DTimestep'+', '+ief.iefParameters['2DTimestep']+'\n')
  f.write('tcfFile'+', '+ief.iefParameters['tcfFile']+'\n')
      
  

class IefCheck():
  def __init__(self):
    self.iefErrors = list()
    self.iefParameters = dict()
    self.iefParameters['tcfFile'] = None
  
  def checkIef(self,filePath):
    print "Starting to check:",filePath
    if os.path.isfile(filePath) == False:
      print "File doesn't exist:", filePath
      return 1 

    os.chdir(os.path.split(filePath)[0])
    
    f = open(filePath)
    
    for line in f.readlines():
      line = line.split('\n')[0]
      if line.startswith('Datafile'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("ERROR ISIS file (.dat) doesn't exist:", fname))
        else:
          pass # Could check the dat file, i.e. number of nodes etc
          self.iefParameters['datFile'] = fname
      elif line.startswith('Results'):
        zznFile = line.split('=')[-1]+'.zzn'
        dirName = os.path.split(line.split('=')[-1])[0]
        if os.path.isdir(dirName)==False:
          self.iefErrors.append(("Results location doesn't exist:", dirName))
        else:
          pass # Could check you have write premission at this location
          self.iefParameters['resultLocation'] = dirName
          self.iefParameters['zznFile'] = zznFile
          if os.path.isfile(zznFile):
            self.iefParameters['zznTime'] = time.ctime(os.path.getmtime(zznFile))
            self.iefParameters['zznSize'] = str(os.path.getsize(zznFile)/1024/1024.0)+'MB'
          else:
            self.iefParameters['zznTime'] = 'None'
            self.iefParameters['zznSize'] = 'None'
      elif line.startswith('Timestep'):
        self.iefParameters['timestep'] = line.split('=')[-1]
      elif line.startswith('2DTimestep'):
        self.iefParameters['2DTimestep'] = line.split('=')[-1]  
      elif line.startswith('ICsFrom'):
        id=line.split('=')[-1]
        if id == '1':
          self.iefParameters['ic'] = 'From dat file'
      elif line.startswith('Start'):
        self.iefParameters['start'] = line.split('=')[-1]
      elif line.startswith('Finish'):
        self.iefParameters['finish'] = line.split('=')[-1]
      elif line.startswith('EventData'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("Event data file (.ied) doesn't exist:", fname))
        else:
          pass # could check that the nodes listed in the ied exist in the dat
          self.iefParameters['iedFile'] = fname
      elif line.startswith('2DFile'):
        fname = line.split('=')[-1]
        if fname.startswith('..'):
          fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.iefErrors.append(("2D file (.tcf) doesn't exist:", fname))
        else:
          self.iefParameters['tcfFile'] = fname
          
    if len(self.iefErrors)== 0:
      print "No errors found in ief"
    else:
      print len(self.iefErrors)," errors found in ief"
      
    
    

  
  
class TcfCheck():
  def __init__(self):
    self.tcfErrors = list()
    self.tcfParameters = dict()
    self.tcfParameters['bc_db_file'] = None
    self.tcfParameters['nwk_lines'] = None
    
  def checkTcf(self,filePath):  
    print "Starting to check:",filePath
    if os.path.isfile(filePath) == False:
      self.tcfErrors.append("File doesn't exist:", filePath)
      print "File doesn't exist:", filePath
      return 1 
    self.tcfParameters['dir'] = os.path.split(filePath)[0]
    
    os.chdir(os.path.split(filePath)[0])
  
    f = open(filePath)
    
    for line in f.readlines():
      line = line.split('\n')[0].lower()
      if line.startswith('!') or line.startswith('#') or len(line.replace(' ','')) == 0:
        continue
      
      line = line.split('!')[0]
      #print line
      
      if line.startswith('shp projection'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR projection file (.prj) doesn't exist:", fname))
        else:
          pass # Could store the projection file and ensure all other projection files are the same
          self.tcfParameters['projection'] = fname
      
      elif line.startswith('bc control file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR bc control file (.tbc) doesn't exist:", fname))
        else:
          self.tcfParameters['tbcFile'] = fname
   
      elif line.startswith('geometry control file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gc control file (.tgc) doesn't exist:", fname))
          self.tcfParameters['tgcFile'] = fname
        else:
          self.tcfParameters['tgcFile'] = fname
    
      elif line.startswith('read materials file'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR materials file (.tmf) doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
          self.tcfParameters['tmfFile'] = fname
   
      elif line.startswith('bc database'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR bc databse (bc*.csv) doesn't exist:", fname))
        else:
          self.tcfParameters['bc_db_file'] = fname
  
      elif line.startswith('read gis isis network'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis network (1d_nwk_*_L.shp) doesn't exist:", fname))
        else:
          self.tcfParameters['nwk_lines']=fname
  
      elif line.startswith('read gis isis nodes'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis nodes (1d_nd_*_P.shp) doesn't exist:", fname))
        else:
          self.tcfParameters['nwk_nds']=fname

      elif line.startswith('read mi isis nodes'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR mi isis nodes (1d_nd_*.mif) doesn't exist:", fname))
        else:
          self.tcfParameters['nwk_nds']=fname
   
      elif line.startswith('read gis isis wll'):
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR gis isis wll (1d_wll_*_L.shp) doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
        
      elif line.startswith('log folder'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]
        path = os.path.abspath(path)
        if os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR log directory doesn't exist:", path))
        else:
          pass # Could check for write access
   
      elif line.startswith('output folder'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]
        path = os.path.abspath(path)
        if os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR output directory doesn't exist:", path))
        else:
          pass # Could check for write access
  
      elif line.startswith('write check files'):
        path = line.split('==')[-1].replace(' ','').rstrip()
        if path.startswith('\\'):
          path = path[1:]       
        path = os.path.abspath(path)
        if os.path.isdir(path)==False:
          self.tcfErrors.append(("ERROR check file directory doesn't exist:", path))
        else:
          pass # Could check for write access  
      
      elif line.startswith('read'):  ## Generic check of other reads
        fname = line.split('==')[-1].replace(' ','').rstrip()
        if fname.startswith('\\'):
          fname = fname[1:]
        fname = os.path.abspath(fname)
        if os.path.isfile(fname)==False:
          self.tcfErrors.append(("ERROR unidentified file doesn't exist:", fname))
        else:
          pass # Could check the contents of the file
    
    if self.tcfParameters['tbcFile'] is not None:
      tbcErrors = checkTbc(self.tcfParameters['tbcFile'],self.tcfParameters['bc_db_file'])
      for error in tbcErrors:
        self.tcfErrors.append(error)
    
    if self.tcfParameters['tgcFile'] is not None:
      tgcErrors = checkTgf(self.tcfParameters['tgcFile'])
      for error in tgcErrors:
        self.tcfErrors.append(error)
    
    if len(self.tcfErrors)== 0:
      print "No errors found in tcf"
    else:
      print len(self.tcfErrors)," errors found in tcf"
    


def checkTbc(filePath,bc_db=None): 
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


def checkTgf(filePath): 
  print "Starting to check:",filePath
  tgcErrors = list()
  if os.path.isfile(filePath) == False:
    tgcErrors.append("File doesn't exist:", filePath)
    return 1 
  
  os.chdir(os.path.split(filePath)[0])
  
  f = open(filePath)
  
  for line in f.readlines():
    line = line.split('\n')[0].lower()
    if line.startswith('!') or line.startswith('#') or len(line.replace(' ','')) == 0:
      continue
    
    line = line.split('!')[0]
    
    if line.startswith('read'):
      if '|' in line:
        fs = line.split('|')
        for f in fs:
          fname = f.split('==')[-1].replace(' ','').rstrip()
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
      filePath = r"P:\Glasgow\WNE\PROJECTS\345488-Riverside,MerthyrTydfil\Hydraulics\v2.2\3 Model\1D\Baseline Model\100yr\Defended\UpperTaff_v2.2_1D-10m-Baseline2015-100yr.ief"
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

  