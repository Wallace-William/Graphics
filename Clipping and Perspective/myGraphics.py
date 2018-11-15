# Wallace, William
# wlw9276
# 2018-11-8 

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
from CohenSutherland import clipLine
#----------------------------------------------------------------------

class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.objects = objects
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    self.objects = []
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def create_graphic_objects( self, canvas, ModelData, persp, doClip ) :
    
    width = int( canvas.cget( 'width' ) )         
    height = int( canvas.cget( 'height' ) ) 
    v = ModelData.getViewport()

    xmin = width * v[0]
    ymin = height * v[1]
    xmax = width * v[2]
    ymax = height * v[3]

    portal = ( xmin, ymin, xmax, ymax )
    
    for face in ModelData.getFaces() :
      v1 = ModelData.getTransformedVertex( face[0], persp )
      v2 = ModelData.getTransformedVertex( face[1], persp )
      v3 = ModelData.getTransformedVertex( face[2], persp )
      if doClip is True :
        line_1 = clipLine( v1[0], v1[1], v2[0], v2[1], portal )
        line_2 = clipLine( v2[0], v2[1], v3[0], v3[1], portal )
        line_3 = clipLine( v3[0], v3[1], v1[0], v1[1], portal )
        if line_1[0] is True :
          self.objects.append( canvas.create_line( line_1[1], line_1[2], line_1[3], line_1[4] ))
        if line_2[0] is True :
          self.objects.append( canvas.create_line( line_2[1], line_2[2], line_2[3], line_2[4] ))
        if line_3[0] is True :
          self.objects.append( canvas.create_line( line_3[1], line_3[2], line_3[3], line_3[4] ))

      else :
          self.objects.append( canvas.create_line( v1[0],  v1[1], v2[0], v2[1] ) )
          self.objects.append( canvas.create_line( v2[0],  v2[1], v3[0], v3[1] ) )
          self.objects.append( canvas.create_line( v3[0],  v3[1], v1[0], v1[1] ) )

  def redisplay( self, canvas, event ) :
    pass
    # if self.objects :
    #   canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
    #   canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
    #   canvas.coords(self.objects[ 2 ],
    #     int( 0.25 * int( event.width ) ),
    #     int( 0.25 * int( event.height ) ),
    #     int( 0.75 * int( event.width ) ),
    #     int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
