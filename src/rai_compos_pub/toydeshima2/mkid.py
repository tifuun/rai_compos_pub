"""filter.py: contains MKID compo for toydeshima2"""

import raimad as rai
from rai_compos_pub import CPWTaperMetal

class MKIDCPWCoup(rai.Compo):
    def _make(self):
        pass

class MKIDCoup(rai.Compo):
    def _make(self):
        pass

class MKIDFingers(rai.Compo):
    def _make(self):
        pass

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
        Straight1 = 
        tl = tl.TL((
            tl.StartAT((0, 0), straight=Straight1).
            tl.StraightTo((0, l1)).
            tl.StraightTo((0, l1 + ltaper), straight=Taper).
            tl.StraightTo((0, l2 + l1 + ltaper), straight=Straight2).
            ))

class MKID(rai.Compo):
    r"""
    Microwave Kinetic Inductance Detector for toydeshima2

          wp1 wp2  wp3                  
         |---|----|----|                
          ___      ____  ___            
         |   |    |    |  |             
         |___|____|____|  | lpatch      
           __|____|      _|_            
          |  |____||      |             
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
        pass
