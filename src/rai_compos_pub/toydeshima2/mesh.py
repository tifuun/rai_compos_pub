"""mesh.py: contains Mesh compo for toydeshima2"""

import raimad as rai

class Mesh(rai.Compo):
    """
    Mesh for toydeshima2

                    length                   
             |---------------------------|     
          ___                                  
           |    | |      | |       | |         
           | ___|_|______|_|_______|_|____ ___ 
           | ___|_|______|_|_______|_|____ _|_ wwire
           |    | |      | |       | |         
           |    | |      | |       | |         
           |    | |      | |       | |         
     width | ___|_|______|_|_______|_|____     
           | ___|_|______|_|_______|_|____  -  
           |    | |      | |       | |      |  
           |    | |      | |       | |      | wcell
           |    | |      | |       | |      |  
           | ___|_|______|_|_______|_|____  |  
           | ___|_|______|_|_______|_|____  -  
           |    | |      | |       | |         
           |    | |      | |       | |         
          _|_   | |      | |       | |         

    """
    def _make(
            self,
            length: float = 1000,
            width: float = 1000,
            wcell: float = 50,
            wwire: float = 10,
            ):
        for x in range(0, length // wcell):
            self.subcompos.append(
                    rai.RectLW(wwire, width)
                    .proxy()
                    .bbox.bot_left.to((x * wcell, 0))
                )
        for y in range(0, width // wcell):
            self.subcompos.append(
                    rai.RectLW(length, wwire)
                    .proxy()
                    .bbox.top_left.to((0, y * wcell))
                )

