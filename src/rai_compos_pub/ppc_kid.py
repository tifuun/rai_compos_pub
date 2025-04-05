#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import raimad as rai


class PPCKID_Layers:
    conductor = rai.Layer("Bottom conductive layer fuctioning as inductor and bottom plates of capacitor")
    dielectric = rai.Layer("Dielectric layer in between the top and bottom layer of the capacitor")
    top = rai.Layer("Top conductive material of the capacitor")
    

class PPCKID_Capacitor(rai.Compo):
    """
    A rudimentary ruler shape
    """
    class Layers:
        pass
        
    class Options:
        length = rai.Option.Geometric(
            "length of one of the bottom plates",
            browser_default=50
            )
        width = rai.Option.Geometric(
            "width of on of the bottom plates",
            browser_default=60
            )
        gap = rai.Option.Geometric(
            "distance between the two bottom plates",
            browser_default = 5
            )
        top_overlap = rai.Option.Geometric(
            "overhang of the top plate w.r.t. the bottom plate",
            browser_default=10
            )
        de_overlap = rai.Option.Geometric(
            "overhang of the dielectric wrt the top plate",
            browser_default=10,
            )

    
    def _make(self,
              length: float =50,
              width: float = 60,
              gap: float = 5,
              top_overlap: float = 10,
              de_overlap: float = 10,
             ):


        ### Define components
        plate_bot = rai.RectLW(width, length).proxy()
        plate_top = rai.RectLW(2*width+gap+2*top_overlap, length+2*top_overlap).proxy()
        dielectric = rai.RectLW(2*width+gap+2*top_overlap+de_overlap, length+2*top_overlap+de_overlap).proxy()

        test_marker = rai.Circle(3).proxy()


        ### Assemble subcomponents
        self.subcompos.plate_bot_L = plate_bot.proxy().move(-width/2- gap/2,0).map('bottom')
        self.subcompos.plate_bot_R = plate_bot.proxy().move(width/2 + gap/2,0).map('bottom')

        self.subcompos.plate_top = plate_top.proxy().map('top')

        self.subcompos.dielectric = dielectric.proxy().map('dielectric')
        
        ### Markers
        self.marks.line_L = self.subcompos.plate_bot_L.bbox.mid_left
        self.marks.line_R = self.subcompos.plate_bot_R.bbox.mid_right

class PPCKID_Inductor_Coupler(rai.Compo):
    """
    A rudimentary ruler shape
    """

    class Options:
        line_width = rai.Option.Geometric(
            "linewidth of inductor",
            browser_default=10
            )
        width = rai.Option.Geometric(
            "width of the coupler line",
            browser_default=200
            )
        height = rai.Option.Geometric(
            "from top of the inductor to the start of the meander",
            browser_default=100
            )
    class Marks:
        left_line_end = rai.Mark("center of line on left side")
        right_line_end = rai.Mark("center of line on left side")
    
    def _make(self,
              line_width: float =10,
              width: float = 200,
              height: float = 50,
             ):

        ### Define components
        coupler_line = rai.RectLW(width, line_width).proxy()
        
        left_line = rai.RectLW(line_width, height-2*line_width).proxy().move(-width/2+line_width/2,-height/2+line_width/2)
        right_line = left_line.proxy().vflip()

        ### Assemble subcomponents
        self.subcompos.coupler_line = coupler_line.proxy()
        self.subcompos.left_line = left_line.proxy()
        self.subcompos.right_line = right_line.proxy()

        ### Markers
        self.marks.left_line_end = self.subcompos.left_line.bbox.bot_mid
        self.marks.right_line_end = self.subcompos.right_line.bbox.bot_mid

class PPCKID_Meander(rai.Compo):
    """
    A rudimentary ruler shape
    """

    class Options:
        line_width = rai.Option.Geometric(
            "linewidth of inductor",
            browser_default=10
            )
        width_meander = rai.Option.Geometric(
            "maximum widht of the meander",
            browser_default=100
            )
        meander_gap = rai.Option.Geometric(
            "gap distance between the meandering lines",
            browser_default = 10
            )
        amount = rai.Option.Geometric(
            "number of meanders (both to left and right)",
            browser_default=3
            )
    class Marks:
        enter = rai.Mark("inter point of meander")
        exit = rai.Mark("exit point of meander")
    
    def _make(self,
              line_width: float =10,
              width_meander: float = 100,
              meander_gap: float = 5,
              amount: float = 3,
             ):

        ### Define components
        horizontal_line = rai.RectLW(width_meander, line_width).proxy()
        vertical_line = rai.RectLW(line_width, meander_gap).proxy()
        end_line = rai.RectLW((width_meander+line_width)/2,line_width)


        ### Assemble the meander components
        for n in range(1,2*amount):
            self.subcompos[f"horizontal_line_{n}"] = horizontal_line.proxy().move(0,-n*(line_width+meander_gap))
            self.subcompos[f"vertical_line_{n}"] = vertical_line.proxy().move(-2*(n%2-0.5)*(width_meander-line_width)/2, (line_width+meander_gap)/2-n*(line_width+meander_gap))

        ### Assemble the start and end lines
        self.subcompos.start_line = end_line.proxy().move(-(width_meander-line_width)/4,0)
        self.subcompos[f"vertical_line_{n+1}"] = vertical_line.proxy().move(-2*((n+1)%2-0.5)*(width_meander-line_width)/2,(line_width+meander_gap)/2-(n+1)*(line_width+meander_gap))
        self.subcompos.end_line = end_line.proxy().move((width_meander-line_width)/4,-2*amount*(line_width+meander_gap))
        
        ### Markers
        self.marks.enter = self.bbox.top_mid
        self.marks.exit = self.bbox.bot_mid

class PPCKID_Connector(rai.Compo):
    """
    A rudimentary ruler shape
    """

    class Options:
        line_width = rai.Option.Geometric(
            "linewidth of inductor",
            browser_default=10
            )
        height = rai.Option.Geometric(
            "maximum widht of the meander",
            browser_default=100
            )
        width = rai.Option.Geometric(
            "gap distance between the meandering lines",
            browser_default = 10
            )

    class Marks:
        connect_top = rai.Mark("inter point of meander")
        connect_side = rai.Mark("exit point of meander")
    
    def _make(self,
              line_width: float =10,
              height: float = 50,
              width: float = 50,
             ):

        ### Define components
        vertical_line = rai.RectLW(line_width, height-line_width).proxy()
        horizontal_line = rai.RectLW(width, line_width).proxy()


        ## Assemble the start and end lines
        self.subcompos.vertical_line = vertical_line
        self.subcompos.horizontal_line = horizontal_line.move((width-line_width)/2,-height/2)
        
        ### Markers
        self.marks.connect_top = self.subcompos.vertical_line.bbox.top_mid
        self.marks.connect_side = self.subcompos.horizontal_line.bbox.mid_right

class PPCKID(rai.Compo):
    """
    A rudimentary ruler shape
    """
    class Options:
       meander_width = rai.Option.Geometric(
            "height of the inductor stucture",
            browser_default=10
            )

    
    class Marks:
        coupler_center = rai.Mark('Center of the coupler structure')
    
    def _make(self,
             meander_width: float = 10
             ):

        inductor_linewidth = 1
        coupler_width = 40
        
        ### Variables capacitor
        plate_height = 10
        plate_width= 10
        gap= 1
        top_overlap = 1
        de_overlap = 2

        capacitor_width = gap+2*plate_width


        ### Meander variables
        line_width = inductor_linewidth
        meander_width = meander_width
        meander_gap = line_width
        amount = 3

        meander_height = 2*amount*(line_width+gap)+2*line_width

        ### Coupler variables
        line_width = inductor_linewidth
        coupler_width = coupler_width
        coupler_height = 10

        ### Connector variables
        line_width = inductor_linewidth
        connector_height = plate_height/2+top_overlap+de_overlap+line_width
        connector_width = (coupler_width-capacitor_width)/2

        ### Proper dimensions check
        # - the width of the top plate and dielectric should be smaller then the connector with (to prevent overlap with verticle)
        # - the distance to the meander should be sufficient such that the 
        
        
        ### Define components
        coupler = PPCKID_Inductor_Coupler(
            line_width = line_width,
            width = coupler_width,
            height = coupler_height,
        ).proxy().map('conductor')

        meander = PPCKID_Meander(
            line_width = line_width,
            width_meander = meander_width,
            meander_gap = meander_gap,
            amount = amount,
        ).proxy().map('conductor')

        connector = PPCKID_Connector(
            line_width = line_width,
            height = connector_height,
            width = connector_width,
        ).proxy().map('conductor')
        
        capacitor = PPCKID_Capacitor(
            length = plate_height,
            width = plate_width,
            gap = gap,
            top_overlap = top_overlap,
            de_overlap = de_overlap,
        ).proxy().map({'bottom':'conductor','top':'top', 'dielectric':'dielectric'})

        
        ### Coupler marks
        left_coupler_end = coupler.marks.left_line_end
        right_coupler_end = coupler.marks.right_line_end
        
        ### Assemble subcomponents
        self.subcompos.coupler = coupler.proxy()
        
        self.subcompos.meander_L = meander.proxy().marks.enter.to(left_coupler_end)
        left_meander_exit = self.subcompos.meander_L.marks.exit
        self.subcompos.connector_L = connector.proxy().marks.connect_top.to(left_meander_exit)
        left_connector_exit = self.subcompos.connector_L.marks.connect_side
        
        self.subcompos.meander_R = meander.proxy().vflip().marks.enter.to(right_coupler_end)
        right_meander_exit = self.subcompos.meander_R.marks.exit
        self.subcompos.connector_R = connector.proxy().vflip().marks.connect_top.to(right_meander_exit)

        self.subcompos.capacitor = capacitor.proxy().marks.line_L.to(left_connector_exit)

        ### Markers
        self.marks.snap_point = self.bbox.top_mid

        # test = self.marks.snap_point 
        # self.subcompos.test = rai.Circle(1).proxy().bbox.mid.to(test)

