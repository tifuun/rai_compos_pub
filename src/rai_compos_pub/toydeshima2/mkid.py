"""filter.py: contains MKID compo for toydeshima2"""


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
    def _make(self):
        pass

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
           | |  | |       |             
           | |  | |       |             
           | |  | |       |  l1         
           | |  | |       |             
           | |  | |      _|_            
           \ \ / /        |             
            | V |         |  ltaper     
            \   /        _|_            
             | |          |             
             | |          |             
             | |          |             
             | |          |  l2         
             | |          |             
             | |          |             
             |_|         _|_            




    """
    def _make(self):
        pass
