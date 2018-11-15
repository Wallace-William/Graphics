# Wallace, William
# wlw9276
# 2018-11-8 

import sys

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.xmin = float('inf')
    self.xmax = float('-inf')
    self.ymin = float('inf')
    self.ymax = float('-inf')
    self.zmin = float('inf')
    self.zmax = float('-inf')

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
                # BOUNDING BOX LOGIC
                if line[0] < self.xmin:
                    self.xmin = line[0]
                if line[0] > self.xmax:
                    self.xmax = line[0]
                if line[1] < self.ymin:
                    self.ymin = line[1]
                if line[1] > self.ymax:
                    self.ymax = line[1]
                if line[2] < self.zmin:
                    self.zmin = line[2]
                if line[2] > self.zmax:
                    self.zmax = line[2]
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

  def getBoundingBox( self ) :
    return (self.xmin,self.xmax,self.ymin,self.ymax,self.zmin,self.zmax)

  def specifyTransform( self, ax, ay, sx, sy, dist ) :
    self.ax = ax
    self.ay = ay
    self.sx = sx
    self.sy = sy
    self.dist = dist

  def getTransformedVertex( self, vNum, persp ) :
    x_ = self.m_Vertices[vNum][0]
    y_ = self.m_Vertices[vNum][1]
    z_ = self.m_Vertices[vNum][2]
    
    if persp is True :
      if z_ >= self.dist : # If z is greater than or equal to view distance, set x and y to 0.0
        x_ = 0.0
        y_ = 0.0
      else :
        x_ = self.sx * (x_/(1-z_/self.dist)) + self.ax
        y_ = self.sy * (y_/(1-z_/self.dist)) + self.ay
    else :
        x_ = self.sx * x_ + self.ax
        y_ = self.sy * y_ + self.ay        

    return (x_, y_, z_)

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
  fx = -1*(w[0])
  fy = -1*(w[1])
  gx = width*v[0]
  gy = height*v[1]

  sx = (width*(v[2]-v[0]))/(w[2]-w[0])
  sy = (height*(v[3]-v[1]))/(w[3]-w[1])
  ax = fx * sx + gx
  ay = fy * sy + gy

  return (ax,ay,sx,sy)

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load and the canvas size.
  fName  = sys.argv[1]
  width  = int( sys.argv[2] )
  height = int( sys.argv[3] )

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

  w = model.getWindow()
  v = model.getViewport()
  print( 'Window line:', w )
  print( 'Viewport line:', v )
  print( 'Canvas size:', width, height )
  print( 'Bounding box:', model.getBoundingBox() )

  ( ax, ay, sx, sy ) = constructTransform( w, v, width, height )
  print( f'Transform is {ax} {ay} {sx} {sy}' )

  model.specifyTransform( ax, ay, sx, sy )

  print( 'First 3 transformed vertices:' )
  for vNum in range( 3 ) :
    print( '     ', model.getTransformedVertex( vNum ) )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
