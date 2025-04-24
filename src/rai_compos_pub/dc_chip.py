import raimad as rai
import numpy as np
import math
from rai_compos_pub import Invert_Layer
from rai_compos_pub import RAIText

class DC_chip_side(rai.Compo):
    def _make(self):
        ## create pads
        contact_pad = rai.RectLW(52,77).proxy()
        top_arm = rai.RectLW(184, 11.2).proxy()
        bottom_arm = rai.RectLW(187.6, 5).proxy()
        arm_up = rai.RectLW(3.8, 72.8).proxy()

        ## create pads
        self.subcompos.pad_TL = contact_pad.proxy()
        self.subcompos.pad_BL = contact_pad.proxy().snap_below(self.subcompos.pad_TL).movey(-3)
        self.subcompos.arm_T = top_arm.proxy().bbox.top_left.to(self.subcompos.pad_TL.bbox.top_left)
        self.subcompos.arm_B1 = bottom_arm.proxy().bbox.top_left.to(self.subcompos.pad_BL.bbox.top_left)
        self.subcompos.arm_B2 = arm_up.proxy().bbox.bot_right.to(self.subcompos.arm_B1.bbox.bot_right)

        ## Marks
        self.marks.connect_h = np.array(list(self.subcompos.arm_T.bbox.bot_right)) + np.array([-7.25,2])
        self.marks.snap_side = self.bbox.mid_right


class Center_region_DC_chip(rai.Compo):
    def _make(self, 
              bridge_width: float = 0.1
             ):

        ## Bridge region
        bridge_hor = rai.RectLW(26.5,bridge_width).proxy()
        bridge_step = rai.RectLW(8.5,1).proxy()
        ## Step gap
        margin = .25
        vertical_connect = margin + (bridge_step.bbox.width+bridge_hor.bbox.width)/2

        bridge_ver = rai.RectLW(bridge_width,vertical_connect)

        ## Center regioin
        slab = rai.RectLW(20,13).proxy()
        
        ## Create subcompos
        # Horizontal parts
        self.subcompos.bridge_hor = bridge_hor.proxy().map('bridge')
        self.subcompos.bridge_hor_step_L = (bridge_step.proxy()
                                            .bbox.mid_left.to(self.subcompos.bridge_hor.bbox.mid_left)
                                            .map('bridge')
                                           )
        self.subcompos.bridge_hor_step_R = (bridge_step.proxy()
                                            .bbox.mid_right.to(self.subcompos.bridge_hor.bbox.mid_right)
                                            .map('bridge')
                                           )
        # Vertical parts
        self.subcompos.bridge_ver_step_L = (bridge_step.proxy().rotate(math.radians(90))
                                            .bbox.top_left.to(self.subcompos.bridge_hor_step_L.bbox.bot_right)
                                            .move(margin,-margin)
                                            .map('bridge')
                                           )
        self.subcompos.bridge_ver_step_R = (bridge_step.proxy().rotate(math.radians(90))
                                            .bbox.top_right.to(self.subcompos.bridge_hor_step_R.bbox.bot_left)
                                            .move(-margin,-margin)
                                            .map('bridge')
                                           )
        self.subcompos.bridge_ver_L = (bridge_ver.proxy()
                                       .bbox.bot_mid.to(self.subcompos.bridge_ver_step_L.bbox.top_mid)
                                       .map('bridge')
                                      )
        self.subcompos.bridge_ver_R = (bridge_ver.proxy()
                                        .bbox.bot_mid.to(self.subcompos.bridge_ver_step_R.bbox.top_mid)
                                        .map('bridge')
                                      )

        # Slab
        self.subcompos.slab = slab.proxy().map('slab')

        ## Marks
        self.marks.connect_L = self.subcompos.bridge_hor_step_L.bbox.mid_left

class DC_chip_pads_inverse(rai.Compo):
    def _make(self):
        split = DC_chip_side().proxy()
        Outer_square = rai.RectLW(split.bbox.length+5,split.bbox.width+5).proxy().bbox.mid.to(split.bbox.mid)
        GND = Invert_Layer(Outer_square,split, rev_inner= False)
        
        # self.subcompos.split = split
        self.subcompos.GND = GND.proxy()

        self.marks.connect_h = split.marks.connect_h
        self.marks.snap_side = split.marks.snap_side

class DC_chip_side_monolayer(rai.Compo):
    def _make(self,
              bridge_length: float = 200,
              bridge_width: float = 10,
             ):
        
        ## create pads
        contact_pad = rai.RectLW(52,77).proxy()
        top_arm = rai.RectLW(90, 11.2).proxy()
        bottom_arm = rai.RectLW(91.9, 5).proxy()
        arm_up = rai.RectLW(3.8, 67.8).proxy()
        arm_up_tip = rai.RectLW(1,6).proxy()
        
        bridge = rai.RectLW(bridge_length/2 + top_arm.bbox.length,bridge_width).proxy()

        ## create pads
        self.subcompos.pad_TL = contact_pad.proxy()
        self.subcompos.pad_BL = contact_pad.proxy().snap_below(self.subcompos.pad_TL).movey(-3)
        self.subcompos.arm_T = top_arm.proxy().bbox.top_left.to(self.subcompos.pad_TL.bbox.top_left)
        self.subcompos.arm_B1 = bottom_arm.proxy().bbox.top_left.to(self.subcompos.pad_BL.bbox.top_left)
        self.subcompos.arm_B2 = arm_up.proxy().bbox.bot_right.to(self.subcompos.arm_B1.bbox.bot_right)
        self.subcompos.arm_B3 = arm_up_tip.proxy().bbox.bot_mid.to(self.subcompos.arm_B2.bbox.top_mid)

        self.subcompos.bridge = bridge.proxy().bbox.bot_left.to(self.subcompos.arm_T.bbox.bot_left)

        ## Marks
        self.marks.snap_side = self.bbox.mid_right

class DC_chip_monolayer(rai.Compo):
    def _make(self,
              inverse_pads: bool = True,
              bridge_length: float = 200,
              bridge_width: float = 10,
              bridge_layer: str = 'bridge',
             ):
        ## Contact pads
        if inverse_pads == True:
            split = DC_chip_side_monolayer(bridge_length, bridge_width).proxy()
            Outer_square = rai.RectLW(split.bbox.length+2.5,split.bbox.width+5).proxy().bbox.mid.to(split.bbox.mid).movex(-1.25)
            Left_pads = Invert_Layer(Outer_square,split, rev_inner= False).proxy().map('pads')
        
        else:
            Left_pads = DC_chip_side_monolayer(bridge_length, bridge_width).proxy().map('pads')

        
        Right_pads = (Left_pads.proxy()
                      .vflip()
                      .movex(328)
                     )
        
        label = f'{bridge_layer} - {bridge_width*10:.0f} x {bridge_length*10:.0f} um'
        
        ## create subcompos
        self.subcompos.pads_L = Left_pads.proxy()
        self.subcompos.pads_R = Right_pads.proxy()

        self.subcompos.label = (RAIText(label).proxy().scale(2e-1)
                                .bbox.mid.to(self.subcompos.pads_L.bbox.bot_right)
                                .movey(20)
                                .map('pads')
                               )
class DC_chip(rai.Compo):
    def _make(self,
              inverse_pads: bool = True,
              bridge_width: float = .1,
              bridge_layer: str = 'bridge',
             ):
        
        ## Contact pads
        if inverse_pads == True:
            Left_pads = DC_chip_pads_inverse().proxy().map('pads')
        else:
            Left_pads = DC_chip_side().proxy().map('pads')
            
        Right_pads = (Left_pads.proxy()
                      .vflip()
                      .marks.snap_side.to(Left_pads.marks.snap_side)
                      .movex(4.8)
                      .map('pads')
                     )
        
        ## Center region
        center = (Center_region_DC_chip(bridge_width).proxy()
                  .snap_right(Left_pads)
                  .movex(4.8)
                  .map({'bridge':'bridge',"slab":"slab"})
                 )

        label = f'{bridge_layer} - {bridge_width*10:.0f} x 80 um'
        
        ## create subcompos
        self.subcompos.pads_L = Left_pads.proxy()
        self.subcompos.pads_R = Right_pads.proxy()
        self.subcompos.center = center.proxy().marks.connect_L.to(Left_pads.proxy().marks.connect_h)

        self.subcompos.label = (RAIText(label).proxy().scale(2e-1)
                                .bbox.mid.to(self.subcompos.pads_L.bbox.bot_right)
                                .movey(20)
                                .map('bridge')
                               )
