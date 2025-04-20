"""filter.py: contains MKID compo for toydeshima2"""

import raimad as rai
from rai_compos_pub import tl
from rai_compos_pub import BetterPartial
from rai_compos_pub import CPWTaperMetal

class MKIDPatch(rai.Compo):
    r"""
      wp1 wp2  wp3                  
     |---|----|----|                
      ___      ____  ___            
     |   |    |    |  |             
     |___|____|____|  | lpatch      
         |    |       |            
         |____|      _|_           
    """
    def _make(
            self,
            wp1: float = 20,
            wp2: float = 20,
            wp3: float = 30,
            lpatch: float = 40,
            ):
        p1 = rai.RectLW(wp1, lpatch / 2).proxy()
        p2 = rai.RectLW(wp2, lpatch / 2).proxy()
        p3 = rai.RectLW(wp3, lpatch / 2).proxy()

        p2.bbox.top_left.to(p1.bbox.bot_right)
        p3.bbox.bot_left.to(p2.bbox.top_right)

        self.subcompos.p1 = p1
        self.subcompos.p2 = p2
        self.subcompos.p3 = p3

class MKIDCoup(rai.Compo):
    r"""
       ________   ___            
      |        |   | width       
      |  ____  |  _|_      ___   
      |_|    |_|           _|_ wstub
                                 
      |--------| length
      |-| lstub
    """

    def _make(
            self,
            length: float = 40,
            width: float = 20,
            lstub: float = 10,
            wstub: float = 10,
            ):
        stub_l = rai.RectLW(lstub, wstub).proxy()
        stub_r = rai.RectLW(lstub, wstub).proxy()
        base = rai.RectLW(length, width).proxy()

        stub_l.bbox.top_left.to(base.bbox.bot_left)
        stub_r.bbox.top_right.to(base.bbox.bot_right)

        self.subcompos.stub_l = stub_l
        self.subcompos.stub_r = stub_r
        self.subcompos.base = base

class MKIDFingers(rai.Compo):
    r"""
         __     ___            
      __ || __   |         ___ 
      || || ||   |          |  
      || || ||   |          |  
      || || ||   | lfinger1 | lfinger2
      ||_||_||   |          |  
      |______|  _|_        _|_ 

      || wfinger
      |------| width

    """
    def _make(
            self,
            lfinger1: float = 50,
            lfinger2: float = 40,
            wfinger: float = 10,
            width: float = 40,
            ):

        finger_l = rai.RectLW(wfinger, lfinger2).proxy()
        finger_r = rai.RectLW(wfinger, lfinger2).proxy()
        finger_mid = rai.RectLW(wfinger, lfinger1).proxy()
        base = rai.RectLW(width, wfinger).proxy()

        finger_l.bbox.bot_left.to(base.bbox.top_left)
        finger_r.bbox.bot_right.to(base.bbox.top_right)
        finger_mid.bbox.bot_mid.to(base.bbox.top_mid)

        self.subcompos.finger_l = finger_l
        self.subcompos.finger_r = finger_r
        self.subcompos.finger_mid = finger_mid
        self.subcompos.base = base


class MKIDLeek(rai.Compo):
    r"""
    "Leek" part of MKID
                                        
                                        
            _   _        ___            
           | | | |        |             
           | | | |        |             
           | | | |        |  l2         
           | | | |        |             
           | | | |       _|_            
           \ \ / /        |             
            | V |         |  ltaper     
            \   /        _|_            
             | |          |             
             | |          |             
             | |          |             
             | |          |  l1         
             | |          |             
             | |          |             
             |_|         _|_            
                                        
           |-|-|-| wl1, wl2, wl3       

    """
    def _make(
            self,
            l1: float = 100,
            l2: float = 100,
            ltaper: float = 40,
            wl1: float = 10,
            wl2: float = 10,
            wl3: float = 10,
            ):
        #Straight1 = rai.RectLW.partial(width=wl2)
        # TODO Partial add marks??
        Straight1 = BetterPartial(
            CPWTaperMetal,
            l=BetterPartial.Mapped('length'),
            sl=wl2,
            sr=wl2,
            wl1=0,
            gl1=0,
            wr1=0,
            gr1=0,
            wl2=0,
            gl2=0,
            wr2=0,
            gr2=0,
            )
        Taper = BetterPartial(
            CPWTaperMetal,
            l=BetterPartial.Mapped('length'),
            sl=0,
            sr=0,

            wl1=-wl2/2,
            wr1=wl1,
            wl2=-wl2/2,
            wr2=wl1,

            gl1=wl1,
            gr1=wl1,
            gl2=wl3,
            gr2=wl3,
            )
        Straight2 = BetterPartial(
            CPWTaperMetal,
            l=BetterPartial.Mapped('length'),
            sl=0,
            sr=0,
            wl1=wl1,
            gl1=wl2,
            wr1=wl2,
            gr1=wl1,
            wl2=wl1,
            gl2=wl2,
            wr2=wl2,
            gr2=wl3,
            )
        leek = tl.TL((
            tl.StartAt((0, 0), straight=Straight1, radius=0),
            tl.StraightTo((0, l1), straight=Taper),
            tl.StraightTo((0, l1 + ltaper), straight=Straight2),
            tl.StraightTo((0, l2 + l1 + ltaper)),
            ))

        leek.make_specs()

        leek.make_straights()
        #leek.make_bends()

        self.subcompos.extend(leek.straights_)
        #self.subcompos.extend(leek.bends_)

class MKID(rai.Compo):
    r"""
    Microwave Kinetic Inductance Detector for toydeshima2

          wp1 wp2  wp3                  
         |---|----|----|                
          ___      ____  ___            
         |   |    |    |  |             
         |___|____|____|  | lpatch      
           __|____|       |             
          |  |____||     _|_            
          |  ____  |      | lcoup       
          |_| __ |_|     _|_            
           __ || __       |         ___ 
           || || ||       |          |  
           || || ||       |          |  
           || || ||       | lfinger1 | lfinger2
           ||_||_||       |          |  
           |______|      _|_        _|_ 
           | | | |        |             
           | | | |        |             
           | | | |        |  l2         
           | | | |        |             
           | | | |       _|_            
           \ \ / /        |             
            | V |         |  ltaper     
            \   /        _|_            
             | |          |             
             | |          |             
             | |          |             
             | |          |  l1         
             | |          |             
             | |          |             
             |_|         _|_            
                                        
           |-|-|-| wl1, wl2, wl3       

    """
    def _make(self):
        leek = MKIDLeek().proxy()
        fingers = MKIDFingers().proxy()
        coup = MKIDCoup().proxy()
        patch = MKIDPatch().proxy()

        fingers.snap_above(leek)
        coup.snap_above(fingers)
        patch.snap_above(coup)

        self.subcompos.leek = leek
        self.subcompos.fingers = fingers
        self.subcompos.coup = coup
        self.subcompos.patch = patch
