from tkinter import *
from tkinter import colorchooser
from tkinter import Scale
from tkinter.ttk import Style
from tkinter import Button,Tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from math import *
import math
import random
import PIL.ImageGrab as ImageGrab
from PIL import Image
from PIL import ImageTk
from tkinter import Canvas, NW, PhotoImage
import numpy as np
 
class PaintApp:
    def __init__(self,width,height, title):
            self.screen = Tk()
            self.screen.title(title)
            self.screen.geometry(str(width)+'x'+str(height))
            self.brush_colour = 'black'
            self.last_x, self.last_y = None, None
            self.shape_id = None
            self.brush_width = 5
            self.marker_size = 25
            self.canvas_colour = "white"
            self.n = 5
            self.magnifier_radius = 50
            self.prev_x = 0
            self.prev_y = 0
            self.eraser_colour = 'white'
            self.shape_ids =[]
            self.screen.state("zoomed")
            self.shapes = []
            self.selected_shape = None
            self.selected_area_id = None
            self.selection_start = None
            self.selected_area = None
            self.magnifier = None
            self.screenshot = None
            self.photo = None  # Store the PhotoImage object
            self.control_points = []
            self.curve_id = None

            #Create the canvas
            self.canvas = Canvas(self.screen, bg="white", bd = 5, relief=GROOVE, height = 575, width = 1345)
            self.canvas.place(x=0, y= 100)

            style = Style()
            style.configure('Vertical.TButton', padding=5, compound='top')

            #Frame
            self.color_frame = LabelFrame(self.screen,text="Colour", relief=RIDGE,bg = "white", width = 500)
            self.color_frame.place(x =0, y =0, width = 250, height= 100)

            self.tool_frame = LabelFrame(self.screen,text="Tools", relief=RIDGE,bg = "white", width = 500)
            self.tool_frame.place(x =251, y =0, width = 370, height= 100)

            self.shapes_frame = LabelFrame(self.screen,text="Shapes", relief=RIDGE,bg = "white", width = 500)
            self.shapes_frame.place(x =620, y =0, width = 350, height= 100)

            self.pen_size = LabelFrame(self.screen,text="Size", relief=RIDGE,bg = "white", width = 500)
            self.pen_size.place(x =971, y =0, width = 250, height= 100)

            #-----------------------Buttons--------------------------------------------
            #Colour Button
            self.vertical_button = Button(self.screen, text='C\no\nl\no\nr', command=self.select_color)
            self.vertical_button.place(x=225, y=10)

            #Tool Buttons--------------------------------------------------------------
            self.canvas_color_b1 = Button(self.tool_frame, text ='Canvas',bd = 4, bg ="White", command=self.Canvas_colour, relief=RIDGE)
            self.canvas_color_b1.grid(row = 0, column = 0,padx = 2)

            self.save = Button(self.tool_frame, text = 'Save',bd = 4, bg ="White", command=self.save_canvas, relief=RIDGE)
            self.save.grid(row = 0, column = 1,padx = 2)

            self.save = Button(self.tool_frame, text = 'Load',bd = 4, bg ="White", command=self.load_canvas, relief=RIDGE)
            self.save.grid(row = 0, column = 2,padx = 2)

            self.save = Button(self.tool_frame, text = 'Fill',bd = 4, bg ="White", command=self.on_fillButton_Presses, relief=RIDGE)
            self.save.grid(row = 1, column = 2,padx = 2)

            self.eraser = Button(self.tool_frame, text= 'Eraser',bd = 4, bg ="White", command=self.erase, relief=RIDGE)
            self.eraser.grid(row = 0, column = 3,padx = 2)

            self.clear = Button(self.tool_frame, text= 'Clear',bd = 4, bg ="White", command=self.clear_canvas, relief=RIDGE)
            self.clear.grid(row = 0, column = 4,padx = 2)

            self.magnifier = Button(self.tool_frame, text= 'Magnify',bd = 4, bg ="White", command=self.on_magnifyButton_Pressed, relief=RIDGE)
            self.magnifier.grid(row = 0, column = 5,padx = 2)

            self.brush = Button(self.tool_frame, text ='Brush',bd = 4, bg ="White", command=self.on_brushButton_Pressed, relief=RIDGE)
            self.brush.grid(row = 1, column = 0,padx = 2)

            self.marker = Button(self.tool_frame, text ='Marker',bd = 4, bg ="White", command=self.on_markerButton_Pressed, relief=RIDGE)
            self.marker.grid(row = 1, column = 1,padx = 2)


            self.areaS = Button(self.tool_frame, text ='Select Area',bd = 4, bg ="White", command=self.select_area, relief=RIDGE)
            self.areaS.grid(row = 1, column = 3,padx = 2)

            self.selMove = Button(self.tool_frame, text ='Move',bd = 4, bg ="White", command=self.on_moveButton_Pressed, relief=RIDGE)
            self.selMove.grid(row = 1, column = 4,padx = 2)

            self.selMove = Button(self.tool_frame, text ='Get Colour',bd = 4, bg ="White", command=self.on_getCButton_Presses, relief=RIDGE)
            self.selMove.grid(row = 1, column = 5,padx = 2)

            #Shapes Buttons------------------------------------------------------------
            self.circleB = Button(self.shapes_frame,text="Circle",bd=4, bg= "White", command=self.on_circleButton_Pressed, relief=RIDGE)
            self.circleB.grid(row =0, column=0)

            self.ovalB = Button(self.shapes_frame,text="Oval",bd=4, bg= "White", command=self.on_ovalButton_Pressed, relief=RIDGE)
            self.ovalB.grid(row =1, column=0)

            self.squareB = Button(self.shapes_frame,text="Square",bd=4, bg= "White", command=self.on_squareButton_Pressed, relief=RIDGE)
            self.squareB.grid(row =0, column=3)

            self.squareB = Button(self.shapes_frame,text="Triangle",bd=4, bg= "White", command=self.on_triangleButton_Pressed, relief=RIDGE)
            self.squareB.grid(row =0, column=4)

            self.squareB = Button(self.shapes_frame,text="Line",bd=4, bg= "White", command=self.on_lineButton_Pressed, relief=RIDGE)
            self.squareB.grid(row =0, column=5)

            self.squareB = Button(self.shapes_frame,text="Curve",bd=4, bg= "White", command=self.on_bezierButton_Pressed, relief=RIDGE)
            self.squareB.grid(row =1, column=4)

            self.rectangleB = Button(self.shapes_frame,text="Rectangle",bd=4, bg= "White", command=self.on_rectangleButton_Pressed, relief=RIDGE)
            self.rectangleB.grid(row =1, column=1)


            self.pentagonB = Button(self.shapes_frame,text="Pentagon",bd=4, bg= "White", command=self.on_pentagonButton_Pressed, relief=RIDGE)
            self.pentagonB.grid(row =0, column=2)

            self.hexagonB = Button(self.shapes_frame,text="Hexagon",bd=4, bg= "White", command=self.on_hexagonButton_Pressed, relief=RIDGE)
            self.hexagonB.grid(row =1, column=2)

            self.nPointsB = Button(self.shapes_frame,text="N Points",bd=4, bg= "White", command=self.on_nPointButton_Pressed, relief=RIDGE)
            self.nPointsB.grid(row =0, column=1)

            self.starB = Button(self.shapes_frame,text="Star",bd=4, bg= "White", command=self.on_starButton_Pressed, relief=RIDGE)
            self.starB.grid(row =1, column=3)

           # Pen and Eraser Size

            self.penS = Scale(self.pen_size, orient= HORIZONTAL, from_= 0, to= 10, length= 220, command=self.onScaleChoosed)
            self.penS.set(1)
            self.penS.grid(row =0, column = 0)
          
            

            colors = ["#000000", "#37474F","#5D4037","#5D4037","#FFC107","#8BC34A","#2E7D32","#039BE5","#303F9F","#512DA8","#E91E63","#D32F2F"]
            #Buttons5
            i=j=k=0
            for color in colors:
                idx = k  # Capture the current value of i
                Button(self.color_frame, bd=3, bg=color, relief=RIDGE, width=3, command=lambda col=color, idx=idx: self.select_color2(idx, colors)).grid(row=j, column=i, padx=1)
                i += 1
                k += 1
                if i == 6:
                    j += 1
                    i = 0


                            # Color Variables
            self.lightest_gray = "#%02x%02x%02x" % (230, 230, 230)
            self.light_gray = "#%02x%02x%02x" % (200, 200, 200)
            self.medium_gray = "#%02x%02x%02x" % (150, 150, 150)
            self.dark_gray = "#%02x%02x%02x" % (100, 100, 100)
            self.darkest_gray = "#%02x%02x%02x" % (50, 50, 50)
            self.color_red = "#%02x%02x%02x" % (250, 50, 50)
            self.color_orange = "#%02x%02x%02x" % (250, 100, 50)
            self.color_yellow = "#%02x%02x%02x" % (255, 200, 50)
            self.color_green = "#%02x%02x%02x" % (150, 250, 230)
            self.color_blue = "#%02x%02x%02x" % (230, 230, 230)
            self.color_purple = "#%02x%02x%02x" % (30, 30, 250)
            self.color_random = "#%02x%02x%02x" % (random.randint(1, 255),random.randint(1, 255), random.randint(1, 255))
                
               
                

    def Canvas_colour(self):
        color = colorchooser.askcolor()
        self.canvas.configure(bg=color[1])
        self.eraser_colour = color[1]
        self.canvas_colour = color[1]
    
    def rotate_text(event):
         event.widget.config(text='\n'.join(event.widget['text']))
    def select_color(self):
        selected_colour = colorchooser.askcolor()
        if(selected_colour[1] is not None):
            self.brush_colour = selected_colour[1]

    def onScaleChoosed(self,event):
        x = self.penS.get()
        self.brush_width = x
    def on_magnaifyButton_Pressed(self):
       self.canvas.bind("<Motion>", self.update_magnifier)
    def on_fillButton_Presses(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        
        self.canvas.bind("<ButtonRelease-1>", self.fillShape)
    def on_triangleButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_triangle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_triangle_end)
    def on_circleButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_circle_end)
    def on_rectangleButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>",self.draw_rectangle_end)
    def on_starButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_star)
        self.canvas.bind("<ButtonRelease-1>",self.draw_star_end) 
    def on_brushButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>",self.brush_draw_end)
    def on_markerButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>",self.setPreviousXY)
    def on_getCButton_Presses(self):
        self.canvas.bind("<Button-1>", self.on_canvas_click)
    def on_bezierButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<Button-1>", self.add_control_point)
    def on_magnifyButton_Pressed(self):
        magnifier_window = Toplevel(self.screen)
        magnifier_window.title("Magnifier")
        magnifier_window.geometry("300x300")

        magnifier_canvas = Canvas(magnifier_window, bg="white", bd=5, relief=GROOVE, height=300, width=300)
        magnifier_canvas.pack()

        def update_magnifier(event):
            magnification_factor = 1.5  # Adjust the magnification factor as desired
            magnified_radius = self.magnifier_radius * magnification_factor

            # Calculate the coordinates for capturing the magnified portion of the canvas
            x0 = event.x - magnified_radius
            y0 = event.y - magnified_radius
            x1 = event.x + magnified_radius
            y1 = event.y + magnified_radius

            # Capture the magnified portion of the canvas
            magnified_image = ImageGrab.grab((x0, y0, x1, y1))
            magnified_image = magnified_image.resize((300, 300), Image.ANTIALIAS)
            magnified_photo = ImageTk.PhotoImage(magnified_image)

            # Update the magnifier canvas
            magnifier_canvas.delete("all")
            magnifier_canvas.create_image(0, 0, image=magnified_photo, anchor=NW)
            magnifier_canvas.image = magnified_photo


        self.canvas.bind("<Motion>", update_magnifier)

        def close_magnifier(event=None):
            self.canvas.unbind("<Motion>")
            magnifier_window.destroy()

        magnifier_window.protocol("WM_DELETE_WINDOW", close_magnifier)
    def on_eraserButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.eraser_draw)
        self.canvas.bind("<ButtonRelease-1>", self.eraser_draw_end)
    def on_pentagonButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_pentagon)
        self.canvas.bind("<ButtonRelease-1>",self.draw_pentagon_end)
    def on_hexagonButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_hexagon)
        self.canvas.bind("<ButtonRelease-1>",self.draw_hexagon_end)
    def on_squareButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>",self.draw_square_end)
    def on_ovalButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.draw_oval)
        self.canvas.bind("<ButtonRelease-1>",self.draw_oval_end)
    def on_nPointButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.n = int(input("Enter the n Points : "))

        self.canvas.bind("<B1-Motion>", self.draw_nPoint)
        self.canvas.bind("<ButtonRelease-1>",self.draw_nPoint_end)
    def on_moveButton_Pressed(self):
        shape_id = self.get_closest_shape(self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                                        self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        if shape_id:
            self.select_shape(shape_id)
            self.move_selected_shape()
            self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
    def on_lineButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

    def draw_triangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3, y3 = self.last_x, event.y
        self.shape_id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.brush_colour, width=5, fill = "")
    def draw_triangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
        
    def draw_circle(self,event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        
        radius = abs (self.last_x - event.x) + abs(self.last_y - event.y)
        x1, y1 = (self.last_x - radius), (self.last_y - radius)
        x2, y2 = (self.last_x + radius), (self.last_y + radius)
        self.shape_id = self.canvas.create_oval(x1,y1,x2,y2, outline = self.brush_colour, width = 5)
        self.shapes.append(self.shape_id)
    def draw_circle_end(self,event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_rectangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y

        self.shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)
    def draw_rectangle_end(self,event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_square(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y

        # Calculate the length of the square side
        side_length = min(abs(x2 - x1), abs(y2 - y1))

        # Calculate the coordinates of the square
        if x2 >= x1:
            x2 = x1 + side_length
        else:
            x2 = x1 - side_length

        if y2 >= y1:
            y2 = y1 + side_length
        else:
            y2 = y1 - side_length

        self.shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)
    def draw_square_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_pentagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        
        # Calculate the center point of the pentagon
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        
        # Calculate the distance between the center and the vertices of the pentagon
        distance = math.sqrt((x2 - cx) ** 2 + (y2 - cy) ** 2)
        
        # Calculate the angles between the vertices of the pentagon
        angle = -math.pi / 2
        angle_increment = 2 * math.pi / 5  # 5 vertices for the pentagon
        pentagon_points = []
        
        for _ in range(5):
            vertex_x = cx + distance * math.cos(angle)
            vertex_y = cy + distance * math.sin(angle)
            pentagon_points.extend([vertex_x, vertex_y])
            angle += angle_increment
        
        # Create a list of pentagon vertices in the required order
        pentagon_points.append(pentagon_points[0])
        pentagon_points.append(pentagon_points[1])
        
        self.shape_id = self.canvas.create_polygon(pentagon_points, outline='black', width=2, fill = '')
    def draw_pentagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_star(self, event):
        for shape_id in self.shape_ids:
            self.canvas.delete(shape_id)
        
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        
        # Calculate the center point of the star
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        
        # Calculate the distance between the center and the outer points of the star
        distance = math.sqrt((x2 - cx) ** 2 + (y2 - cy) ** 2)
        
        # Calculate the angles between the points of the star
        angle = -math.pi / 2
        angle_increment = 4 * math.pi / 5  # 5 points for the star
        star_points = []
        
        for _ in range(5):
            outer_x = cx + distance * math.cos(angle)
            outer_y = cy + distance * math.sin(angle)
            star_points.extend([outer_x, outer_y])
            angle += angle_increment
        
        # Create a list of star points in the required order
        star_points.append(star_points[0])
        star_points.append(star_points[1])
        
        # Draw only the outer edges of the star
        for i in range(0, len(star_points) - 2, 2):
            shape_id = self.canvas.create_line(star_points[i], star_points[i+1], star_points[i+2], star_points[i+3], fill='black', width=2)
            self.shape_ids.append(shape_id)
    def draw_star_end(self,event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_hexagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        
        # Calculate the center point of the hexagon
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        
        # Calculate the distance between the center and the vertices of the hexagon
        distance = math.sqrt((x2 - cx) ** 2 + (y2 - cy) ** 2)
        
        # Calculate the angles between the vertices of the hexagon
        angle = -math.pi / 2
        angle_increment = (2 * math.pi) / 6  # 6 vertices for the hexagon
        hexagon_points = []
        
        for _ in range(6):
            vertex_x = cx + distance * math.cos(angle)
            vertex_y = cy + distance * math.sin(angle)
            hexagon_points.extend([vertex_x, vertex_y])
            angle += angle_increment
        
        # Create a list of hexagon vertices in the required order
        hexagon_points.append(hexagon_points[0])
        hexagon_points.append(hexagon_points[1])
        
        self.shape_id = self.canvas.create_polygon(hexagon_points, outline='black', width=2, fill = '')
    def draw_hexagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
        
    def draw_oval(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y

        self.shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline='black', width=2)
    def draw_oval_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_nPoint(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y

        # Calculate the center point of the polygon
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Calculate the radius of the polygon
        radius = math.sqrt((x2 - cx) ** 2 + (y2 - cy) ** 2)

        # Calculate the angles between the points of the polygon
        angle = -math.pi / 2
        angle_increment = 2 * math.pi / self.n

        polygon_points = []
        for _ in range(self.n):
            point_x = cx + radius * math.cos(angle)
            point_y = cy + radius * math.sin(angle)
            polygon_points.extend([point_x, point_y])
            angle += angle_increment

        # Create a list of polygon points in the required order
        polygon_points.append(polygon_points[0])
        polygon_points.append(polygon_points[1])

        self.shape_id = self.canvas.create_polygon(polygon_points, outline='black', width=2, fill = "")
    def draw_nPoint_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def select_color2(self, i, colors):
        self.brush_colour = colors[i]
        print("Button", i, "pressed.")
            
    def brush1(self):
        self.brush_width = 3
    def brush2(self):
        self.brush_width = 4
    def brush3(self):
        self.brush_width = 6
    def fill(self,event):
        item = self.canvas.find_withtag(CURRENT)
        self.canvas.itemconfigure(item, fill=self.fill_color)
        self.canvas.bind("<Button-1>", self.fill_shape)

    def save_canvas(self):
        filename = filedialog.asksaveasfilename(defaultextension=".jpg")
        x = self.screen.winfo_rootx()+self.canvas.winfo_x()
        y = self.screen.winfo_rooty()+self.canvas.winfo_y()

        x1 = self.canvas.winfo_width() + x
        y1 = self.canvas.winfo_height() + y
        ImageGrab.grab().crop((x,y,x1,y1)).save(filename)
        messagebox.showinfo("Paint Notification", "Jahaz File save hogai hai, Happy Happy Happy")
        
    def erase(self):
        #self.brush_colour = self.eraser_colour 
        self.brush_colour = self.canvas_colour
    def clear_canvas(self):
        self.canvas.delete("all")

    def brush_draw(self, event):

        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x,self.last_y, event.x, event.y,width = self.brush_width,capstyle=ROUND, fill = self.brush_colour)
        self.last_x, self.last_y = event.x, event.y
    def brush_draw_end(self,event):
        self.last_x, self.last_y = None, None

    def eraser_draw(self, event):  
        x = self.canvas.canvasx(event.x)  # Use canvasx method to get the correct coordinates
        y = self.canvas.canvasy(event.y)  # Use canvasy method to get the correct coordinates
        self.canvas.create_rectangle(x - self.brush_width, y - self.brush_width, x + self.brush_width, y + self.brush_width,
            fill=self.eraser_colour, outline=self.eraser_colour)
        print("i am here")
        print(self.eraser_colour)
    def eraser_draw_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None  

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
                self.canvas.image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.image)
            except:
                messagebox.showerror("Error", "Failed to load image.")

    def select_area(self):
        if self.selected_area_id:
            self.canvas.delete(self.selected_area_id)
            self.selected_area_id = None
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

    def update_magnifier2(self, event):
        x, y = event.x, event.y
        screenshot = ImageGrab.grab(
            bbox=(
                self.screen.winfo_rootx() + self.canvas.winfo_rootx() + x - self.magnifier_radius,
                self.screen.winfo_rooty() + self.canvas.winfo_rooty() + y - self.magnifier_radius,
                self.screen.winfo_rootx() + self.canvas.winfo_rootx() + x + self.magnifier_radius,
                self.screen.winfo_rooty() + self.canvas.winfo_rooty() + y + self.magnifier_radius
            )
        )
        screenshot = screenshot.resize((self.magnifier_radius*2, self.magnifier_radius*2))
        photo = ImageTk.PhotoImage(screenshot)
        self.magnifier.configure(image=photo)
        self.magnifier.image = photo
        self.magnifier.place(x=self.screen.winfo_pointerx() - self.magnifier_radius, y=self.screen.winfo_pointery() - self.magnifier_radius)

    def update_magnifier1(self, event):
        x, y = event.x, event.y
        try:
            self.screenshot = ImageGrab.grab(
                bbox=(
                    self.screen.winfo_rootx() + self.canvas.winfo_rootx() + x - self.magnifier_radius,
                    self.screen.winfo_rooty() + self.canvas.winfo_rooty() + y - self.magnifier_radius,
                    self.screen.winfo_rootx() + self.canvas.winfo_rootx() + x + self.magnifier_radius,
                    self.screen.winfo_rooty() + self.canvas.winfo_rooty() + y + self.magnifier_radius
                )
            )
            self.screenshot = self.screenshot.resize((self.magnifier_radius * 2, self.magnifier_radius * 2))
            self.photo = ImageTk.PhotoImage(self.screenshot)  # Store the PhotoImage object

            if self.magnifier is None:
                self.magnifier = Button(self.screen, image=self.photo)
            else:
                self.magnifier.configure(image=self.photo)
            self.magnifier.image = self.photo

            self.magnifier.place(x=self.screen.winfo_pointerx() - self.magnifier_radius,
                                 y=self.screen.winfo_pointery() - self.magnifier_radius)
        except Exception as e:
            print("Error occurred while updating magnifier:", str(e))

    
    def fillShape(self, event):
        x = event.x
        y = event.y
        closest_shape = self.canvas.find_closest(x,y)
        if(closest_shape != 1):
            self.canvas.itemconfig(closest_shape,fill = self.brush_colour)
    def get_pixel_color(self, event):
        x, y = event.x, event.y
        
        # Get the screenshot of the screen
        screenshot = ImageGrab.grab()
        
        # Get the color of the selected pixel
        color = screenshot.getpixel((x, y))
        
        # Convert the RGB color values to hexadecimal
        hex_color = '#%02x%02x%02x' % color[:3]
        
        # Set self.brush_colour to the hexadecimal color
        self.brush_colour = hex_color
        print(hex_color)


   
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        x1 = min(self.selection_start[0], event.x)
        y1 = min(self.selection_start[1], event.y)
        x2 = max(self.selection_start[0], event.x)
        y2 = max(self.selection_start[1], event.y)

        self.selected_area = (x1, y1, x2, y2)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        screenshot = ImageGrab.grab()
        color = screenshot.getpixel((x, y))
        hex_color = '#%02x%02x%02x' % color[:3]
        self.brush_colour = hex_color
    def on_canvas_drag(self, event):
        if self.selected_shape is not None:
            x = event.x
            y = event.y

            if self.prev_x is not None and self.prev_y is not None:
                dx = x - self.prev_x
                dy = y - self.prev_y
                self.canvas.move(self.selected_shape, dx, dy)

            self.prev_x = x
            self.prev_y = y
    def on_canvas_release(self, event):
        self.selected_shape = None
        self.prev_x = None
        self.prev_y = None
    def select_shape(self, shape_id):
        self.selected_shape = shape_id
    def move_selected_shape(self):
        pass
    def select_area(self):
        if self.selected_area_id:
            self.canvas.delete(self.selected_area_id)
            self.selected_area_id = None

        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
    def start_selection(self, event):
        self.selection_start = (event.x, event.y)
    def update_selection(self, event):
        if self.selected_area_id:
            self.canvas.delete(self.selected_area_id)

        x1 = self.selection_start[0]
        y1 = self.selection_start[1]
        x2 = event.x
        y2 = event.y

        self.selected_area_id = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="red", width=2
        )
    def end_selection(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        x1 = min(self.selection_start[0], event.x)
        y1 = min(self.selection_start[1], event.y)
        x2 = max(self.selection_start[0], event.x)
        y2 = max(self.selection_start[1], event.y)

        self.selected_area = (x1, y1, x2, y2)
    def get_closest_shape(self, x, y):
        closest = self.canvas.find_closest(x, y)
        if closest:
            return closest[0]
        return None
    def on_moveButton_Pressed(self):
        shape_id = self.get_closest_shape(self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                                          self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        if shape_id:
            self.select_shape(shape_id)
            self.move_selected_shape()
            self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
    def on_stopMoveButton_Pressed(self):
        self.canvas.unbind("<B1-Motion>")

    def setColor(self):
        try:
            val1 = int(self.myEntry1.get())
            val2 = int(self.myEntry2.get())
            val3 = int(self.myEntry3.get())
            if 0 <=(val1 and val2 and val3) <= 255:              
                self.rgb = "#%02x%02x%02x" % (val1, val2, val3)
            self.myEntry1.delete(0, END)
            self.myEntry2.delete(0, END)
            self.myEntry3.delete(0, END)

        except ValueError:
            print("That's not an int!")
        self.focus()
    def setPreviousXY(self, event):
            self.previousX = event.x
            self.previousY = event.y
    def draw(self, event):
        # Bamboo
       
            self.canvas.create_polygon(
                ((event.x +  0) +   0), # X1
                ((event.y +  0) +   0), # Y1
                ((event.x +  5) +   0), # X2
                ((event.y +  5) +   0), # Y2
                ((event.x +  0) -  30), # X3
                ((event.y +  0) +  40), # Y3
                ((event.x -  5) -  30), # X4
                ((event.y -  5) +  40), # Y4
                ((event.x +  0) +   0), # X1
                ((event.y +  0) +   0), # Y1
                fill = self.color_random,
                outline = "purple",
                )
       
    def start_line(self, event):
        self.last_x = event.x
        self.last_y = event.y
    def draw_line(self, event):
        self.canvas.delete("line")  # Delete previously drawn lines
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.brush_colour, tags="line")
    def end_line(self, event):
        self.last_x = None
        self.last_y = None
    def select_color(self):
        selected_colour = colorchooser.askcolor()
        if selected_colour[1] is not None:
            self.brush_colour = selected_colour[1]

    def add_control_point(self, event):
        x = event.x
        y = event.y
        self.control_points.append((x, y))

        # Draw the control point as a small circle
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")

        # Draw the Bézier curve
        if len(self.control_points) >= 2:
            self.draw_bezier_curve()
    def draw_bezier_curve(self):
        if self.curve_id:
            self.canvas.delete(self.curve_id)

        points = self.control_points[:]
        num_points = len(points)

        if num_points < 2:
            return

        # Generate the intermediate points of the curve
        curve_points = []
        for t in range(0, 101):
            t /= 100.0
            x = self.calculate_bezier_point(points, 0, num_points - 1, t, 'x')
            y = self.calculate_bezier_point(points, 0, num_points - 1, t, 'y')
            curve_points.append(x)
            curve_points.append(y)

        # Draw the curve
        self.curve_id = self.canvas.create_line(curve_points, smooth=True, fill="black")
    def calculate_bezier_point(self, points, start_index, end_index, t, coordinate):
        if start_index == end_index:
            return points[start_index][0] if coordinate == 'x' else points[start_index][1]

        p0 = self.calculate_bezier_point(points, start_index, end_index - 1, t, coordinate)
        p1 = self.calculate_bezier_point(points, start_index + 1, end_index, t, coordinate)

        return (1 - t) * p0 + t * p1



    def on_canvas_click(self, event):
        x, y = event.x, event.y
        screenshot = ImageGrab.grab()
        color = screenshot.getpixel((x, y))
        hex_color = '#%02x%02x%02x' % color[:3]
        self.brush_colour = hex_color

    def run(self):
        self.screen.mainloop()


PaintApp(800,600, "PaintApp").run()
