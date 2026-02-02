import raimad as rai
from rai_compos_pub import Invert_Layer
from rai_compos_pub.invert_layer import union, close_ring, connect_outer_and_inner

class PPCKID_Capacitor_v3(rai.Compo):
    """
    PPC capacitor component (without dielectric)
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

    
    def _make(self,
              length: float =13,
              width: float = 13,
              gap: float = 3.3,
              top_overlap: float = 1,
             ):


        ### Define components
        plate_bot = rai.RectLW(width, length).proxy()
        plate_top = rai.RectLW(2*width+gap+2*top_overlap, length+2*top_overlap).proxy()

        test_marker = rai.Circle(3).proxy()


        ### Assemble subcomponents
        self.subcompos.plate_bot_L = plate_bot.proxy().move(-width/2- gap/2,0).map('bottom')
        self.subcompos.plate_bot_R = plate_bot.proxy().move(width/2 + gap/2,0).map('bottom')

        self.subcompos.plate_top = plate_top.proxy().map('top')
        
        ### Markers
        self.marks.line_L = self.subcompos.plate_bot_L.bbox.mid_left
        self.marks.line_R = self.subcompos.plate_bot_R.bbox.mid_right

class PPCKID_Inductor_Coupler_v2(rai.Compo):
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

class PPCKID_Inductor_Meander_v2(rai.Compo):
    """
    A rudimentary ruler shape
    """

    class Options:
        line_width = rai.Option.Geometric(
            "linewidth of inductor",
            browser_default=0.5
            )
        width_meander = rai.Option.Geometric(
            "maximum widht of the meander",
            browser_default=60
            )
        meander_gap = rai.Option.Geometric(
            "gap distance between the meandering lines",
            browser_default = 0.5
            )
        amount = rai.Option.Geometric(
            "number of meanders (both to left and right)",
            browser_default=3
            )
        
    class Marks:
        enter = rai.Mark("inter point of meander")
        exit = rai.Mark("exit point of meander")
    
    def _make(self,
              line_width: float = 0.5,
              width_meander: float = 10,
              meander_gap: float = 0.5,
              amount: float = 3,
             ):

        ### Define components
        horizontal_line = rai.RectLW(width_meander, line_width).proxy()
        vertical_line = rai.RectLW(line_width, meander_gap).proxy()
        end_line = rai.RectLW((width_meander+line_width)/2,line_width)


        ### Assemble the meander components
        for n in range(0,2*amount):
            self.subcompos[f"horizontal_line_{n}"] = horizontal_line.proxy().move(0,-n*(line_width+meander_gap))
            self.subcompos[f"vertical_line_{n}"] = vertical_line.proxy().move(-2*(n%2-0.5)*(width_meander-line_width)/2, (line_width+meander_gap)/2-n*(line_width+meander_gap))
            if n == 0:
                self.marks.enter = self.subcompos[f"vertical_line_{n}"].bbox.top_mid
            if n == range(0,2*amount)[-1]:
                self.marks.exit = self.subcompos[f"horizontal_line_{n}"].bbox.mid_right

class PPCKID_Assembly_v3(rai.Compo):
    """
    Parralel Place Capacitor KID used for measurement of dielectric materials
    """
    class Options:
       meander_width = rai.Option.Geometric(
            "height of the inductor stucture",
            browser_default=10
            )

    
    class Marks:
        coupler_center = rai.Mark('Center of the coupler structure')
    
    def _make(self,
              meander_width: float = 10,
             ):

        junk_layer = 'z_junk'

        ### Input parameters
        
        # Variables capacitor
        plate_height = 13
        plate_width= 13
        gap= 3.3
        top_overlap = 0.5

        capacitor_width = gap+2*plate_width
        
        # variables connector
        line_width = 0.5
        connector_width = 2

        # Coupler variables
        line_width = line_width
        coupler_width = gap+2*plate_width + 2*connector_width + 2*line_width
        coupler_height = 1
        
        # Meander variables
        line_width = line_width
        meander_width = meander_width
        meander_gap = line_width
        amount = 3

        meander_height = 2*amount*(line_width+meander_gap)

        # Coupler variables
        line_width = line_width
        coupler_width = coupler_width
        coupler_height = 2

        # Dielectric variables
        de_gap = 1
        
        # Capacitor Plates
        capacitor = PPCKID_Capacitor_v3(
            length = plate_height,
            width = plate_width,
            gap = gap,
            top_overlap = top_overlap,
         ).proxy().map({'bottom':junk_layer,'top':'top'})
        
        self.subcompos.capacitor = capacitor.proxy()

        # junk_layer = None
            
        # Connectors
        connector = rai.RectLW(connector_width,line_width).proxy().map(junk_layer)
        yshift = 2
        self.subcompos.connector_L = connector.proxy().bbox.mid_right.to(self.subcompos.capacitor.marks.line_L).movey(yshift)
        self.subcompos.connector_R = connector.proxy().bbox.mid_left.to(self.subcompos.capacitor.marks.line_R).movey(yshift)

        # Meanders
        meander = PPCKID_Inductor_Meander_v2(
            line_width = line_width,
            width_meander = meander_width,
            meander_gap = meander_gap,
            amount = amount,
        ).proxy().map(junk_layer)
        self.subcompos.meander_L = meander.proxy().marks.exit.to(self.subcompos.connector_L.bbox.mid_left)
        self.subcompos.meander_R = meander.proxy().vflip().marks.exit.to(self.subcompos.connector_R.bbox.mid_right)

        # Coupler
        coupler = PPCKID_Inductor_Coupler_v2(
            line_width = line_width,
            width = coupler_width,
            height = coupler_height
        ).proxy().map(junk_layer)
        self.subcompos.coupler = coupler.proxy().marks.left_line_end.to(self.subcompos.meander_L.marks.enter)
        
        ### GND layer
        coup_gap = 2
        GND_gap_bot = 3
        GND = rai.RectLW(coupler_width+2*(meander_width+3),coup_gap+coupler_height-line_width+meander_height+plate_height/2+yshift-line_width/2+GND_gap_bot).proxy()
        self.subcompos.GND = GND.bbox.top_mid.to(self.subcompos.coupler.bbox.top_mid).movey(coup_gap).map(junk_layer)


        ### Dielectric Layer
        Dielectric = rai.RectLW(GND.bbox.length - 2*de_gap, GND.bbox.width - 2*de_gap).proxy()
        self.subcompos.Dielectric = Dielectric.bbox.mid.to(GND.bbox.mid).map('dielectric')
        
        ### Inverse GND
        flat_junk_subcompo = [self.subcompos.coupler.steamroll()[junk_layer]
                              +self.subcompos.meander_L.steamroll()[junk_layer]
                              +self.subcompos.meander_R.steamroll()[junk_layer]
                              +self.subcompos.connector_L.steamroll()[junk_layer]
                              +self.subcompos.connector_R.steamroll()[junk_layer]
                              +self.subcompos.capacitor.steamroll()[junk_layer]
                             ]
        
        inner_compo_poly = union(flat_junk_subcompo[0])
        # for i,shape in enumerate(inner_compo_poly):
        #     self.subcompos[f"test{i}"] = rai.CustomPoly(shape).proxy()

        outer_compo_poly = union(self.subcompos.GND.steamroll()[junk_layer])
        
        path = connect_outer_and_inner(outer_compo_poly[0], inner_compo_poly[0], rev_inner=False)

        self.subcompos.test = rai.CustomPoly(path).proxy().map('conductor')
