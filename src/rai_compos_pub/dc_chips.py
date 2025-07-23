import raimad as rai
import numpy as np
import math

from rai_compos_pub import RAIText
from rai_compos_pub import Invert_Layer
from rai_compos_pub import Layer_merge

## DC_chip without a bridge
# ------------------------------------

class DC_chip_side_no_bridge(rai.Compo):
    """
    A basic component for the DC chip structures - used to build DC_chip_no_bridge
    """
    
    class Options:
        width = rai.Option.Geometric(
            "total width of one side of the DC structure",
            browser_default = 200,
        )
        bridge_length = rai.Option.Geometric(
            "length of the freestanding bridge arm of one side of the DC structure",
            browser_default = 50
        )
        bridge_width = rai.Option.Geometric(
            "width of the bridge line",
            browser_default = 10
        )

    class Marks:
        connect = rai.Mark("connection point at the center of the end of the bridge structure")
    
    def _make(self,
              width = 200,
              bridge_length: float = 50,
              bridge_width: float = 10,
             ):
        
        ## create pads
        contact_pad = rai.RectLW(52,77).proxy()
        arm_up = rai.RectLW(3.8, 67.8).proxy()
        arm_up_tip = rai.RectLW(1,6).proxy()
        
        bottom_arm = rai.RectLW(width-bridge_length+arm_up.bbox.length/2,5).proxy()
        

        top_arm = rai.RectLW(width-bridge_length-3.8/2-1/2, 11.2).proxy()
        
        bridge = rai.RectLW(width,bridge_width).proxy()

        ## create pads
        self.subcompos.pad_TL = contact_pad.proxy()
        self.subcompos.pad_BL = contact_pad.proxy().snap_below(self.subcompos.pad_TL).movey(-3)
        self.subcompos.arm_T = top_arm.proxy().bbox.top_left.to(self.subcompos.pad_TL.bbox.top_left)
        self.subcompos.arm_B1 = bottom_arm.proxy().bbox.top_left.to(self.subcompos.pad_BL.bbox.top_left)
        self.subcompos.arm_B2 = arm_up.proxy().bbox.bot_right.to(self.subcompos.arm_B1.bbox.bot_right)
        self.subcompos.arm_B3 = arm_up_tip.proxy().bbox.bot_mid.to(self.subcompos.arm_B2.bbox.top_mid)

        self.subcompos.bridge = bridge.proxy().bbox.bot_left.to(self.subcompos.arm_T.bbox.bot_left)

        ## Marks
        self.marks.connect = self.subcompos.bridge.bbox.mid_right

class DC_chip_no_bridge(rai.Compo):
    """
    DC chip structure used to probe the resistance of a 'wide' line with relatively large length.
    Allows for an inverted "pads" layer by changing the 'inverse_pads' variable.
    """

    class Options:
        total_width = rai.Option.Geometric(
            "total width of the DC structure",
            browser_default = 400,
        )
        bridge_length = rai.Option.Geometric(
            "length of the freestanding bridge arm of the DC structure",
            browser_default = 100
        )
        bridge_width = rai.Option.Geometric(
            "width of the bridge line",
            browser_default = 10
        )
        inverse_pads = rai.Option.Geometric(
            "States whether to invert the layer containing the pads (changing polarity)",
            browser_default = False
        )
        bridge_layer = rai.Option.Geometric(
            "Uses the given string to use in the DC structure label",
            browser_default = "bridge"
        )
        
    def _make(self,
              inverse_pads: bool = False,
              bridge_length: float = 200,
              bridge_width: float = 10,
              bridge_layer: str = 'bridge',
              total_width: float = 400
             ):
        ## Contact pads
        left_pads = DC_chip_side_no_bridge(total_width/2, bridge_length/2, bridge_width).proxy()
        right_pads = (left_pads.proxy()
                      .vflip()
                      .marks.connect.to(left_pads.marks.connect)
                     )
        pads = Layer_merge(left_pads,right_pads)
        
        label = f'{bridge_layer} - {bridge_width*10:.0f} x {bridge_length*10:.0f} um'
        label_compo = (RAIText(label).proxy().scale(2e-1)
                       .bbox.mid.to(left_pads.bbox.bot_right)
                       .movey(20)
                      )

        if inverse_pads == False:
            self.subcompos.pads = pads.proxy()
            self.subcompos.label = label_compo.proxy()
        elif inverse_pads == True:
            merge = Layer_merge(pads,label_compo)
            outer_box = (rai.RectLW(merge.bbox.length+5,merge.bbox.width+5).proxy()
                         .bbox.mid.to(merge.bbox.mid)
                        )
            invert_merge = Invert_Layer(outer_box,merge,rev_inner=False).proxy().map("pads")
            self.subcompos.inverse_merge = invert_merge.proxy()

## DC_chip with Bridge
#--------------------------------------

class DC_chip_side(rai.Compo):
    """
    A basic component for the DC chip structures - used to build DC_chip_no_bridge
    """
    class Marks:
        connect_H = rai.Mark("connection point on the center of the end of the horizontal arm")
        connect_V = rai.Mark("connection point on the center of the end of the vertical arm")
    
    def _make(self,
              size_pad: tuple = (52,77),
              size_top_arm: tuple = (184, 11.2),
              size_bottom_arm: tuple = (187.6, 5),
              size_arm_up: tuple = (3.8,72.8),
              pad_gap: bool = 3
             ):
        ## create pads
        contact_pad = rai.RectLW(size_pad[0],size_pad[1]).proxy()
        top_arm = rai.RectLW(size_top_arm[0],size_top_arm[1]).proxy()
        bottom_arm = rai.RectLW(size_bottom_arm[0],size_bottom_arm[1]).proxy()
        arm_up = rai.RectLW(size_arm_up[0], size_arm_up[1]).proxy()

        ## create pads
        self.subcompos.pad_TL = contact_pad.proxy()
        self.subcompos.pad_BL = contact_pad.proxy().snap_below(self.subcompos.pad_TL).movey(-pad_gap)
        self.subcompos.arm_T = top_arm.proxy().bbox.top_left.to(self.subcompos.pad_TL.bbox.top_left)
        self.subcompos.arm_B1 = bottom_arm.proxy().bbox.top_left.to(self.subcompos.pad_BL.bbox.top_left)
        self.subcompos.arm_B2 = arm_up.proxy().bbox.bot_right.to(self.subcompos.arm_B1.bbox.bot_right)

        ## Marks
        self.marks.connect_H = self.subcompos.arm_T.bbox.mid_right
        self.marks.connect_V = self.subcompos.arm_B2.bbox.top_mid

class DC_chip_center_region(rai.Compo):
    """
    A basic component for the DC chip structures - used to build DC structures that require narrow lines for their measurements.
    """
    class Options:
        bridge_length = rai.Option.Geometric(
            "length of the freestanding bridge line",
            browser_default = 8
        )
        bridge_width = rai.Option.Geometric(
            "width of the bridge line",
            browser_default = 0.1
        )
        step_length = rai.Option.Geometric(
            "the length of the steps connecting the pads with the central bridge",
            browser_default = 8.5,
        )
        step_width = rai.Option.Geometric(
            "the width of the steps connecting the pads with the central bridge",
            browser_default = 1,
        )
        slab = rai.Option.Geometric(
            "states whether to generate a slab underneath the bridge of an intermediate layer",
            browser_default = True,
        )
        slab_length = rai.Option.Geometric(
            "states the length of the slab",
            browser_default = 20,
        )
        slab_width = rai.Option.Geometric(
            "states the width of the slab",
            browser_default = 13,
        )
        margin = rai.Option.Geometric(
            "states how far the steps are positioned w.r.t. each other. A larger margin is a larger spacing",
            browser_default = 0.75,
        )

    class Marks:
        connect_L = rai.Mark("connection point on the left side of the center of the horizontal step structure")
        connect_L = rai.Mark("connection point on the right side of the center of the horizontal step structure")
    
    def _make(self,
              bridge_length: float = 8,
              bridge_width: float = 0.1,
              step_length: float = 8.5,
              step_width: float = 1,
              slab: bool = True,
              slab_length: float = 20,
              slab_width: float = 13,
              margin = .75,
             ):
        
        ## Bridge region
        bridge_hor = rai.RectLW(bridge_length+2*(step_length+margin),bridge_width).proxy()
        bridge_step = rai.RectLW(step_length,step_width).proxy()
        ## Step gap

        bridge_ver = rai.RectLW(bridge_width,margin-bridge_width/2)
        
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
        self.subcompos.bridge_ver_L = (bridge_ver.proxy()
                                       .bbox.top_mid.to(self.subcompos.bridge_hor_step_L.bbox.mid_right)
                                       .move(margin,-bridge_width/2)
                                       .map('bridge')
                                      )
        self.subcompos.bridge_ver_step_L = (bridge_step.proxy().rotate(math.radians(90))
                                            .bbox.top_mid.to(self.subcompos.bridge_ver_L.bbox.bot_mid)
                                            .map('bridge')
                                           )
        self.subcompos.bridge_ver_R = (bridge_ver.proxy()
                                       .bbox.top_mid.to(self.subcompos.bridge_hor_step_R.bbox.mid_left)
                                       .move(-margin,-bridge_width/2)
                                       .map('bridge')
                                      )
        self.subcompos.bridge_ver_step_R = (bridge_step.proxy().rotate(math.radians(90))
                                            .bbox.top_mid.to(self.subcompos.bridge_ver_R.bbox.bot_mid)
                                            .map('bridge')
                                           )

        ## Slab
        if slab == True:
            slab = rai.RectLW(step_length+2*margin+bridge_length,step_length+2*margin).proxy()
            self.subcompos.slab = slab.proxy().map('slab')

        ## Marks
        self.marks.connect_L = self.subcompos.bridge_hor_step_L.bbox.mid_left
        self.marks.connect_R = self.subcompos.bridge_hor_step_R.bbox.mid_right

class DC_chip(rai.Compo):
    """
    DC chip structure used to probe the resistance of a 'narrow' line with relatively small length on top of a slab of non-conductive material."
    Allows for an inverted "pads" layer by changing the 'inverse_pads' variable.
    """
    class Options:
        inverse_pads = rai.Option.Geometric(
            "States whether to invert the layer containing the pads (changing polarity)",
            browser_default = False
        )
        bridge_layer = rai.Option.Geometric(
            "Uses the given string to use in the DC structure label",
            browser_default = "bridge"
        )
        bridge_length = rai.Option.Geometric(
            "length of the freestanding bridge line",
            browser_default = 8
        )
        bridge_width = rai.Option.Geometric(
            "width of the bridge line",
            browser_default = 0.1
        )
        total_width = rai.Option.Geometric(
            "total width of one side of the DC structure",
            browser_default = 400,
        )
        step_length = rai.Option.Geometric(
            "the length of the steps connecting the pads with the central bridge",
            browser_default = 8.5,
        )
        step_width = rai.Option.Geometric(
            "the width of the steps connecting the pads with the central bridge",
            browser_default = 1,
        )
        slab = rai.Option.Geometric(
            "states whether to generate a slab underneath the bridge of an intermediate layer",
            browser_default = True,
        )
        slab_length = rai.Option.Geometric(
            "states the length of the slab",
            browser_default = 20,
        )
        slab_width = rai.Option.Geometric(
            "states the width of the slab",
            browser_default = 13,
        )
        margin = rai.Option.Geometric(
            "states how far the steps are positioned w.r.t. each other. A larger margin is a larger spacing",
            browser_default = 0.75,
        )


    def _make(self,
              inverse_pads: bool = False,
              bridge_layer: str = 'bridge',
              bridge_length: float = 8,
              bridge_width: float = 0.1,
              total_width: float = 400,
              step_length: float = 8.5,
              step_width: float = 1,
              slab: bool = True,
              slab_length: float = 20,
              slab_width: float = 13,
              margin: float = 0.75,
             ):
        
        ### Build center
        center = (DC_chip_center_region(bridge_length,
                                        bridge_width,
                                        step_length,
                                        step_width,
                                        slab,
                                        slab_length,
                                        slab_width,
                                        margin
                                       ).proxy()
                 )

        ### Build pads
        overlap = step_length/4
        size_top_arm = (total_width/2 - center.bbox.length/2 + overlap, 11.2)
        size_arm_up = (3.8,
                       3+5+77-size_top_arm[1]/2-step_width/2-(margin-bridge_width/2) - step_length + overlap #set values correspond to standard arm size
                      )
        size_bottom_arm = (size_top_arm[0]+step_length-overlap+margin+size_arm_up[0]/2, 5)
        
        
        left_pads = (DC_chip_side(size_top_arm = size_top_arm, size_bottom_arm =size_bottom_arm, size_arm_up = size_arm_up).proxy()
                     .marks.connect_H.to(center.marks.connect_L)
                     .movex(overlap)
                    )
        right_pads = (left_pads.proxy()
                      .vflip()
                      .marks.connect_H.to(center.marks.connect_R)
                      .movex(-overlap)
                     )

        pads = Layer_merge(left_pads,right_pads)

        ### Build label
        label = f'{bridge_layer} - {bridge_width*10:.0f} x {bridge_length*10:.0f} um'
        label_compos = (RAIText(label).proxy()
                        .scale(2e-1)
                        .bbox.mid.to(left_pads.bbox.bot_right)
                        .movey(20)
                        .map('bridge')
                       )

        ### Build subcompos
        if inverse_pads == True:
            outer_box = (rai.RectLW(pads.bbox.length+5,pads.bbox.width+5).proxy()
                         .bbox.mid.to(pads.bbox.mid)
                        )
            inverse_pads = Invert_Layer(outer_box,pads,rev_inner=False).proxy()
            self.subcompos.pads = inverse_pads.proxy().map("pads")
        elif inverse_pads == False:
            self.subcompos.pads = pads.proxy().map("pads")
        else:
            print("ERROR: could not interpret 'inverse_pads'")
            
        self.subcompos.center = center.proxy()
        self.subcompos.label = label_compos.proxy()

class DC_chip_monolayer_bridge(rai.Compo):
    """
    DC chip structure used to probe the resistance of a 'narrow' line with relatively small length.
    Allows for an inverted "pads" layer by changing the 'inverse_pads' variable.
    """
    class Options:
        inverse_pads = rai.Option.Geometric(
            "States whether to invert the layer containing the pads (changing polarity)",
            browser_default = False
        )
        bridge_layer = rai.Option.Geometric(
            "Uses the given string to use in the DC structure label",
            browser_default = "bridge"
        )
        bridge_length = rai.Option.Geometric(
            "length of the freestanding bridge line",
            browser_default = 8
        )
        bridge_width = rai.Option.Geometric(
            "width of the bridge line",
            browser_default = 0.1
        )
        total_width = rai.Option.Geometric(
            "total width of one side of the DC structure",
            browser_default = 400,
        )
        step_length = rai.Option.Geometric(
            "the length of the steps connecting the pads with the central bridge",
            browser_default = 8.5,
        )
        step_width = rai.Option.Geometric(
            "the width of the steps connecting the pads with the central bridge",
            browser_default = 1,
        )
        margin = rai.Option.Geometric(
            "states how far the steps are positioned w.r.t. each other. A larger margin is a larger spacing",
            browser_default = 0.75,
        )
        
    def _make(self,
              inverse_pads: bool = False,
              bridge_layer: str = 'bridge',
              bridge_length: float = 8,
              bridge_width: float = 0.1,
              total_width: float = 400,
              step_length: float = 8.5,
              step_width: float = 1,
              margin: float = 0.75,
             ):
        
        ### Build center
        center = (DC_chip_center_region(bridge_length,
                                        bridge_width,
                                        step_length,
                                        step_width,
                                       ).proxy()
                 )

        ### Build pads
        overlap = step_length/4
        size_top_arm = (total_width/2 - center.bbox.length/2 + overlap, 11.2)
        size_arm_up = (3.8,
                       3+5+77-size_top_arm[1]/2-step_width/2-(margin-bridge_width/2) - step_length + overlap #set values correspond to standard arm size
                      )
        size_bottom_arm = (size_top_arm[0]+step_length-overlap+margin+size_arm_up[0]/2, 5)
        
        left_pads = (DC_chip_side(size_top_arm = size_top_arm, size_bottom_arm =size_bottom_arm, size_arm_up = size_arm_up).proxy()
                     .marks.connect_H.to(center.marks.connect_L)
                     .movex(overlap)
                    )
        right_pads = (left_pads.proxy()
                      .vflip()
                      .marks.connect_H.to(center.marks.connect_R)
                      .movex(-overlap)
                     )

        pads = Layer_merge(left_pads,right_pads)
        merge = Layer_merge(pads, center, 'root', 'bridge')

        ### Build label
        label = f'{bridge_layer} - {bridge_width*10:.0f} x {bridge_length*10:.0f} um'
        label_compos = (RAIText(label).proxy()
                        .scale(2e-1)
                        .bbox.mid.to(left_pads.bbox.bot_right)
                        .movey(20)
                       )
        merge_w_label = Layer_merge(merge,label_compos)

        ### Build subcompos
        if inverse_pads == False:
            self.subcompos.merge = merge.proxy()
            self.subcompos.label = label_compos.proxy()
        elif inverse_pads == True:
            merge_w_label = Layer_merge(merge,label_compos)
            outer_box = (rai.RectLW(merge_w_label.bbox.length+5,merge_w_label.bbox.width+5).proxy()
                         .bbox.mid.to(merge_w_label.bbox.mid)
                        )
            inverse_pads = Invert_Layer(outer_box,merge_w_label,rev_inner=False).proxy().map("pads")
            self.subcompos.pads = inverse_pads.proxy()
        else:
            print("ERROR: could not interpret 'inverse_pads'")
