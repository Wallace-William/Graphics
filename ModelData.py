# 2018-09-09

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open(inputFile, 'r') as fp:                                          
      lines = fp.read().replace('\r','').split('\n')
    # Initialize window and viewport false to check for duplicates                   
    w = False                                           
    s = False                                            
    for(index, line) in enumerate(lines, start=1):
      line = line.strip()
      if not line:                                        # Check for comments
        continue
      if '#' in line:                                           # Check for blank lines
        continue
      line = line.split()                                    # Convert lines into lists to get data
      if line[0] == 'w':                                     # Check for window
        if w == True:
          print("Line %d is a duplicate window spec." % index)    # ERROR: Duplicate window, duplicates replace previous values
        line = line[1:]                                          # Remove 'w' 
        if len(line) != 4:                                       # ERROR: Invalid size
          print("Line %d is a malformed window spec." % index)
        else:
          for x in range(0,len(line)):                           # Convert each string in list to float
            try:
              line[x] = float(line[x])
              if x == len(line)-1:                               # If no exceptions occur, save in self.m_Window as tuple
                self.m_Window = (line[0],line[1],line[2],line[3])
                w = True                                         # Set w to True to catch any duplicate window specs in file
            except:                                              # ERROR: String conversion
              print("Line %d is a malformed window spec." % index)
              break
      elif line[0] == 's':                                   # Check for viewport
        if s == True:
          print("Line %d is a duplicate viewport spec." % index)  # ERROR: Duplicate viewport
        line = line[1:]
        if len(line) != 4:                                       # ERROR: Invalid size
          print("Line %d is a malformed viewport spec." % index)
        else:
          for x in range(0,len(line)):
            try:
              line[x] = float(line[x])
              if x == len(line)-1:
                self.m_Viewport = (line[0],line[1],line[2],line[3])
                s = True
            except:                                              # ERROR: String conversion
              print("Line %d is a malformed viewport spec." % index)
              break
      elif line[0] == 'v':                                   # Check for vertex
        line = line[1:]
        if len(line) != 3:                                       # ERROR: Invalid size
          print("Line %d is a malformed vertex spec." % index)
          continue
        else:
          for x in range(0,len(line)):
            try:
              line[x] = float(line[x])
              if x == len(line)-1:                               
                self.m_Vertices.append((line[0],line[1],line[2]))
            except:                                              # ERROR: String conversion
              print("Line %d is a malformed vertex spec." % index)
              break
      elif line[0] == 'f':                                   # Check for face
        line = line[1:]
        if len(line) != 3:
          print("Line %d is a malformed face spec." % index)      # ERROR: Invalid size
        else:
          for x in range(0,len(line)):
            try:
              line[x] = int(line[x])
              if x == len(line)-1:                               
                self.m_Faces.append((line[0]-1,line[1]-1,line[2]-1))
            except:                                              # ERROR: String conversion 
              print("Line %d is a malformed face spec." % index)
              break
      else:                                                  # ERROR: None of the above
        print("INVALID LINE")

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load.
  fName = sys.argv[1]

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( "%s: %d vert%s, %d face%s" % (
    fName,
    len( model.getVertices() ), 'ex' if len( model.getVertices() ) == 1 else 'ices',
    len( model.getFaces() ), '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( '     ', v )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( '     ', f )

  print( 'Window line:', model.getWindow() )
  print( 'Viewport line:', model.getViewport() )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
