# Wallace, William
# wlw9276
# 2018-11-8 

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog
from ModelData import ModelData, constructTransform

#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :

    self.m_clip = tk.BooleanVar( )
    self.m_clip.set( True )
    
    self.m_perspective = tk.BooleanVar( )
    self.m_perspective.set( True )
    
    self.m_distance = 1.0

    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.menu = cl_menu( self )

    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )
    

#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='#ff9999' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<ButtonPress-1>',   self.left_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-1>', self.left_mouse_release_callback )
    self.canvas.bind( '<B1-Motion>',       self.left_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-2>',   self.middle_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-2>', self.middle_mouse_release_callback )
    self.canvas.bind( '<B2-Motion>',       self.middle_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-3>',   self.right_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-3>', self.right_mouse_release_callback )
    self.canvas.bind( '<B3-Motion>',       self.right_mouse_down_motion_callback )
    self.canvas.bind( '<Key>',             self.key_pressed_callback )
    self.canvas.bind( '<Up>',              self.up_arrow_pressed_callback )
    self.canvas.bind( '<Down>',            self.down_arrow_pressed_callback )
    self.canvas.bind( '<Right>',           self.right_arrow_pressed_callback )
    self.canvas.bind( '<Left>',            self.left_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Up>',        self.shift_up_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Down>',      self.shift_down_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Right>',     self.shift_right_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Left>',      self.shift_left_arrow_pressed_callback )

  def key_pressed_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Up arrow pressed' )

  def down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Down arrow pressed' )

  def right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Right arrow pressed' )

  def left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Left arrow pressed' )

  def shift_up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift up arrow pressed' )

  def shift_down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift down arrow pressed' )

  def shift_right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift right arrow pressed' )

  def shift_left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift left arrow pressed' )

  def left_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def left_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def left_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def middle_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def middle_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def middle_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def right_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

    self.master.ob_world.redisplay( self.master.ob_canvas_frame.canvas, event )

#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text = "wlw9276: " + formatStr % args )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    self.filemenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = self.filemenu )
    self.filemenu.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    self.filemenu.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    self.filemenu.add_separator()
    self.filemenu.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    self.settingsmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = self.settingsmenu )
    self.settingsmenu.add_checkbutton( label = 'Clip', variable = self.master.m_clip )
    self.settingsmenu.add_checkbutton( label = 'Perspective', variable = self.master.m_perspective )

    self.helpmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = self.helpmenu )
    self.helpmenu.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )
    

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )
    self.button = tk.Button( self.toolbar, text = 'Perspective', width = 16, command = self.toolbar_perspective_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Reset', width = 16, command = self.toolbar_reset_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Load', width = 16, command = self.toolbar_load_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Draw', width = 16, command = self.toolbar_draw_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.toolbar.pack( side = tk.TOP, fill = tk.X )
    
  def toolbar_perspective_callback( self ) :
    f = simpledialog.askfloat(
            'Perspective Dist','Distance?',
            initialvalue = self.master.m_distance, minvalue = 1.0)
    if( f is None ) :
      msg = f'[Cancelled, remains {self.master.m_distance}]'
    else :
      self.master.m_distance = f
      msg = f'Distance is now {f}'
    self.master.statusBar_frame.set( msg )

  def toolbar_reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )

  def toolbar_load_callback( self ) :
    # Get Filename Dialog Box
    fName = tk.filedialog.askopenfilename( filetypes = [ ( "allfiles", "*" )] )
    
    # Check if user didn't choose a file / canceled load
    if ( len( fName ) == 0 ) :
        self.master.statusBar_frame.set( "%s", "[Load was cancelled]" )

    else :
        msg = "Loading data from '%s' ..." % ( fName )
        print( msg )
        self.master.statusBar_frame.set( "%s", msg )

        # Create ModelData object using chosen file
        self.ModelData = ModelData( fName )

  def toolbar_draw_callback( self ) :
    # Check if Model has been loaded first
    try :
      self.ModelData
    except :
      self.ModelData = None

    if( self.ModelData is None ) :
      msg = "[Nothing is loaded]"
      self.master.statusBar_frame.set( "%s", msg )

    else :
      # Get current canvas width and height  
      width = int( self.master.ob_canvas_frame.canvas.cget( 'width' ) )
      height = int( self.master.ob_canvas_frame.canvas.cget( 'height' ) )

      # Get window and viewport info from ModelData instance
      w = self.ModelData.getWindow()
      v = self.ModelData.getViewport()

      # Construct Transform
      ( ax,ay,sx,sy ) = constructTransform( w, v, width, height )

      # Specify Transform
      self.ModelData.specifyTransform( ax, ay, sx, sy, self.master.m_distance )

      # Calculate viewport Rectangle
      xmin = width * v[0]
      ymin = height * v[1]
      xmax = width * v[2]
      ymax = height * v[3]

      # Draw viewport Rectangle
      self.master.ob_canvas_frame.canvas.create_line(xmin, ymin, xmin, ymax, fill="black")
      self.master.ob_canvas_frame.canvas.create_line(xmin, ymin, xmax, ymin, fill="black")
      self.master.ob_canvas_frame.canvas.create_line(xmax, ymin, xmax, ymax, fill="black")
      self.master.ob_canvas_frame.canvas.create_line(xmin, ymax, xmax, ymax, fill="black")
      
      # Pass canvas and ModelData instance
      self.master.ob_world.create_graphic_objects( self.master.ob_canvas_frame.canvas, self.ModelData,
                                                   self.master.m_perspective.get() == 1,
                                                   self.master.m_clip.get() == 1)

      self.master.statusBar_frame.set( 'Draw callback' )

#----------------------------------------------------------------------
