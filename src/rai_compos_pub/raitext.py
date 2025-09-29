#!/usr/bin/env python
# coding: utf-8

# In[11]:


"""
raitext.py: Home to the RAItext component with its symbol library
"""


import raimad as rai

class RAIText(rai.Compo):
    """ 
    Generate 2D polygons of symbols.
    
    Contains
    Letters: A-Z (small letters are capitalized)
    Numbers: 0-9
    And a selection op special symbols

    Inspired by the KLayout font
    
    """
    class Options:
        string = rai.Option.Functional(
            "Text displayed by the function", 
            browser_default = "RAIText"
        )
        scale = rai.Option.Geometric(
            "Size scaling of the text",
            browser_default = 1
        )
    
    def _make(self, 
              string: str = "RAIText",
              scale: float = 1):
        symbols_dict= {}

        """ Capitalized letters as Polygons """
        symbols_dict["A"] = rai.CustomPoly([(0,0),(0,55),(15,70),(35,70),(45,60),(20,60),(10,50),(10,35),(40,35),(40,50),(30,60),(45,60),(50,55),(50,0),(40,0),(40,25),(10,25),(10,0)
                                             ])
        symbols_dict["B"] = rai.CustomPoly([(0,0),(0,70),(40,70),(50,60),(10,60),(10,40),(35,40),(40,45),(40,55),(35,60),(50,60),(50,40),(45,35),(50,30),(10,30),(10,10),(35,10),(40,15),(40,25),(35,30),(50,30),(50,10),(40,0)
                                             ])
        symbols_dict["C"] = rai.CustomPoly([(10,0),(0,10),(0,60),(10,70),(40,70),(50,60),(50,50),(40,50),(40,55),(35,60),(15,60),(10,55),(10,15),(15,10),(35,10),(40,15),(40,20),(50,20),(50,10),(40,0)
                                             ])
        symbols_dict["D"] = rai.CustomPoly([(0,0),(0,70),(35,70),(45,60),(10,60),(10,10),(30,10),(40,20),(40,50),(30,60),(45,60),(50,55),(50,15),(35,0)
                                             ])
        symbols_dict["E"] = rai.CustomPoly([(0,0),(0,70),(50,70),(50,60),(10,60),(10,40),(30,40),(30,30),(10,30),(10,10),(50,10),(50,0)
                                             ])
        symbols_dict["F"] = rai.CustomPoly([(0,70),(50,70),(50,60),(10,60),(10,40),(30,40),(30,30),(10,30),(10,0),(0,0)
                                              ])
        symbols_dict["G"] = rai.CustomPoly([(0,10),(0,60),(10,70),(40,70),(50,60),(50,50),(40,50),(40,55),(35,60),(15,60),(10,55),(10,15),(15,10),(35,10),(40,15),(40,30),(25,30),(25,40),(50,40),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["H"] = rai.CustomPoly([(0,70),(10,70),(10,40),(40,40),(40,70),(50,70),(50,0),(40,0),(40,30),(10,30),(10,0),(0,0)
                                             ])
        symbols_dict["I"] = rai.CustomPoly([(0,10),(5,10),(5,60),(0,60),(0,70),(20,70),(20,60),(15,60),(15,10),(20,10),(20,0),(0,0)
                                             ])
        symbols_dict["J"] = rai.CustomPoly([(0,10),(0,20),(10,20),(10,15),(15,10),(35,10),(40,15),(40,60),(30,60),(30,70),(50,70),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["K"] = rai.CustomPoly([(0,70),(10,70),(10,40),(20,40),(40,60),(40,70),(50,70),(50,55),(30,35),(50,15),(50,0),(40,0),(40,10),(20,30),(10,30),(10,0),(0,0)
                                             ])
        symbols_dict["L"] = rai.CustomPoly([(0,70),(10,70),(10,10),(50,10),(50,0),(0,0)
                                             ])
        symbols_dict["M"] = rai.CustomPoly([(0,70),(10,70),(20,60),(30,60),(40,70),(50,70),(50,0),(40,0),(40,50),(35,50),(25,40),(15,50),(10,50),(10,0),(0,0)
                                             ])
        symbols_dict["N"] = rai.CustomPoly([(0,70),(10,70),(35,45),(40,45),(40,70),(50,70),(50,0),(40,0),(40,25),(15,50),(10,50),(10,0),(0,0)
                                             ])
        symbols_dict["O"] = rai.CustomPoly([(0,10),(0,60),(10,70),(40,70),(50,60),(50,35),(40,35),(40,55),(35,60),(15,60),(10,55),(10,15),(15,10),(35,10),(40,15),(40,35),(50,35),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["P"] = rai.CustomPoly([(0,70),(40,70),(50,60),(50,40),(40,30),(10,30),(10,40),(35,40),(40,45),(40,55),(35,60),(10,60),(10,0),(0,0)
                                             ])
        symbols_dict["Q"] = rai.CustomPoly([(0,10),(0,60),(10,70),(40,70),(50,60),(15,60),(10,55),(10,15),(15,10),(25,10),(25,15),(20,20),(30,30),(35,25),(40,25),(40,55),(35,60),(50,60),(50,20),(45,15),(50,10),(40,0),(35,5),(30,0),(10,0)
                                             ])
        symbols_dict["R"] = rai.CustomPoly([(0,70),(40,70),(50,60),(10,60),(10,40),(35,40),(40,45),(40,55),(35,60),(50,60),(50,40),(40,30),(40,25),(50,15),(50,0),(40,0),(40,10),(20,30),(10,30),(10,0),(0,0)
                                             ])
        symbols_dict["S"] = rai.CustomPoly([(0,10),(0,20),(10,20),(10,15),(15,10),(35,10),(40,15),(40,25),(35,30),(10,30),(0,40),(0,60),(10,70),(40,70),(50,60),(50,50),(40,50),(40,55),(35,60),(15,60),(10,55),(10,45),(15,40),(40,40),(50,30),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["T"] = rai.CustomPoly([(20,60),(0,60),(0,70),(50,70),(50,60),(30,60),(30,0),(20,0)
                                             ])
        symbols_dict["U"] = rai.CustomPoly([(0,10),(0,70),(10,70),(10,15),(15,10),(35,10),(40,15),(40,70),(50,70),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["V"] = rai.CustomPoly([(0,20),(0,70),(10,70),(10,25),(25,10),(40,25),(40,70),(50,70),(50,20),(30,0),(20,0)
                                             ])
        symbols_dict["W"] = rai.CustomPoly([(0,70),(10,70),(10,15),(15,15),(25,25),(35,15),(40,15),(40,70),(50,70),(50,0),(35,0),(25,10),(15,0),(0,0)
                                             ])
        symbols_dict["X"] = rai.CustomPoly([(0,15),(15,30),(15,40),(0,55),(0,70),(10,70),(10,60),(25,45),(40,60),(40,70),(50,70),(50,55),(35,40),(35,30),(50,15),(50,0),(40,0),(40,10),(25,25),(10,10),(10,0),(0,0)
                                             ])
        symbols_dict["Y"] = rai.CustomPoly([(20,35),(0,55),(0,70),(10,70),(10,60),(25,45),(40,60),(40,70),(50,70),(50,55),(30,35),(30,0),(20,0)
                                             ])
        symbols_dict["Z"] = rai.CustomPoly([(0,20),(20,40),(25,40),(40,55),(40,60),(0,60),(0,70),(50,70),(50,50),(30,30),(25,30),(10,15),(10,10),(50,10),(50,0),(0,0)
                                             ])

        
        """ Lower case letters as copies of capitalized """
        symbols_dict["a"] = symbols_dict["A"]
        symbols_dict["b"] = symbols_dict["B"]
        symbols_dict["c"] = symbols_dict["C"]
        symbols_dict["d"] = symbols_dict["D"]
        symbols_dict["e"] = symbols_dict["E"]
        symbols_dict["f"] = symbols_dict["F"]
        symbols_dict["g"] = symbols_dict["G"]
        symbols_dict["h"] = symbols_dict["H"]
        symbols_dict["i"] = symbols_dict["I"]
        symbols_dict["j"] = symbols_dict["J"]
        symbols_dict["k"] = symbols_dict["K"]
        symbols_dict["l"] = symbols_dict["L"]
        symbols_dict["m"] = symbols_dict["M"]
        symbols_dict["n"] = symbols_dict["N"]
        symbols_dict["o"] = symbols_dict["O"]
        symbols_dict["p"] = symbols_dict["P"]
        symbols_dict["q"] = symbols_dict["Q"]
        symbols_dict["r"] = symbols_dict["R"]
        symbols_dict["s"] = symbols_dict["S"]
        symbols_dict["t"] = symbols_dict["T"]
        symbols_dict["u"] = symbols_dict["U"]
        symbols_dict["v"] = symbols_dict["V"]
        symbols_dict["w"] = symbols_dict["W"]
        symbols_dict["x"] = symbols_dict["X"]
        symbols_dict["y"] = symbols_dict["Y"]
        symbols_dict["z"] = symbols_dict["Z"]


        """ Numbers as Polygons """
        symbols_dict["0"] = rai.CustomPoly([(0,10),(0,60),(10,70),(40,70),(50,60),(15,60),(10,55),(10,15),(15,10),(35,10),(40,15), (40,25),(30,25),(30,45),(20,45),(20,25),(40,25) ,(40,55),(35,60),(50,60),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["1"] = rai.CustomPoly([(0,0),(0,10),(20,10),(20,50),(15,50),(5,40),(0,40),(0,50),(20,70),(30,70),(30,10),(50,10),(50,0)
                                             ])
        symbols_dict["2"] = rai.CustomPoly([(0,0),(0,25),(10,35),(35,35),(40,40),(40,55),(35,60),(15,60),(10,55),(10,50),(0,50),(0,60),(10,70),(40,70),(50,60),(50,35),(40,25),(15,25),(10,20),(10,10),(50,10),(50,0)
                                             ])
        symbols_dict["3"] = rai.CustomPoly([(0,10),(0,20),(10,20),(10,15),(15,10),(35,10),(40,15),(40,25),(35,30),(20,30),(20,40),(35,40),(40,45),(40,55),(35,60),(15,60),(10,55),(10,50),(0,50),(0,60),(10,70),(40,70),(50,60),(50,40),(45,35),(50,30),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["4"] = rai.CustomPoly([(30,15),(0,15),(0,25),(30,25),(30,50),(25,50),(10,35),(10,25),(0,25),(0,40),(30,70),(40,70),(40,25),(50,25),(50,15),(40,15),(40,0),(30,0)
                                             ])
        symbols_dict["5"] = rai.CustomPoly([(0,10),(0,20),(10,20),(10,15),(15,10),(35,10),(40,15),(40,30),(35,35),(0,35),(0,70),(50,70),(50,60),(10,60),(10,45),(40,45),(50,35),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["6"] = rai.CustomPoly([(0,10),(0,50),(20,70),(40,70),(40,60),(25,60),(15,50),(15,45),(40,45),(50,35),(15,35),(10,30),(10,15),(15,10),(35,10),(40,15),(40,30),(35,35),(50,35),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["7"] = rai.CustomPoly([(20,35),(40,55),(40,60),(0,60),(0,70),(50,70),(50,50),(30,30),(30,0),(20,0)
                                             ])
        symbols_dict["8"] = rai.CustomPoly([(0,10),(0,30),(5,35),(0,40),(0,60),(10,70),(40,70),(50,60),(15,60),(10,55),(10,45),(15,40),(35,40),(40,45),(40,55),(35,60),(50,60),(50,40),(45,35),(50,30),(15,30),(10,25),(10,15),(15,10),(35,10),(40,15),(40,25),(35,30),(50,30),(50,10),(40,0),(10,0)
                                             ])
        symbols_dict["9"] = rai.CustomPoly([(10,10),(25,10),(35,20),(35,25),(10,25),(0,35),(35,35),(40,40),(40,55),(35,60),(15,60),(10,55),(10,40),(15,35),(0,35),(0,60),(10,70),(40,70),(50,60),(50,20),(30,0),(10,0)
                                             ])


        """ Other symbols (To be Continued) """
        symbols_dict["~"] = rai.CustomPoly([(0,60),(10,70),(25,70),(32.5,62.5),(40,70),(50,70),(50,60),(40,50),(25,50),(17.5,57.5),(10,50),(0,50)
                                             ])
        symbols_dict["!"] = rai.CustomPoly([(0,10),(10,10),(10,0),(0,0)
                                             ])
        symbols_dict["@"] = rai.CustomPoly([(0,10),(0,60),(10,70),(40,70),(50,60),(50,30),(40,30),(40,40),(30,40),(30,30),(50,30),(50,25),(45,20),(25,20),(20,25),(20,45),(25,50),(40,50),(40,55),(35,60),(15,60),(10,55),(10,15),(15,10),(50,10),(50,0),(10,0)
                                             ])
        symbols_dict["#"] = rai.CustomPoly([(10,20),(0,20),(0,30),(10,30),(10,40),(0,40),(0,50),(10,50),(10,70),(20,70),(20,50),(30,50),(30,70),(40,70),(40,50),(50,50),(50,40),(40,40),(40,30),(50,30),(50,20),(40,20),(40,0),(30,0),(30,40),(20,40),(20,30),(30,30),(30,20),(20,20),(20,0),(10,0)
                                             ])
        symbols_dict["$"] = rai.CustomPoly([(20,10),(0,10),(0,20),(20,20),(20,30),(5,30),(0,35),(0,55),(5,60),(20,60),(20,70),(30,70),(30,60),(50,60),(50,50),(10,50),(10,40),(20,40),(20,50),(30,50),(30,40),(45,40),(50,35),(50,30),(30,30),(30,20),(40,20),(40,30),(50,30),(50,15),(45,10),(30,10),(30,0),(20,0)
                                             ])
        symbols_dict["%"] = rai.CustomPoly([(0,15),(40,55),(40,65),(50,65),(50,50),(10,10),(10,0),(0,0)
                                             ])
        symbols_dict["^"] = rai.CustomPoly([(0,60),(10,70),(20,70),(30,60),(30,50),(20,50),(20,55),(15,60),(10,55),(10,50),(0,50)
                                             ])
        symbols_dict["&"] = rai.CustomPoly([(0,5),(0,30),(5,35),(0,40),(0,65),(5,70),(25,70),(30,65),(30,60),(10,60),(10,45),(20,45),(20,60),(30,60),(30,40),(25,35),(35,25),(40,30),(50,30),(50,25),(10,25),(10,10),(25,10),(25,20),(20,25),(50,25),(50,20),(45,15),(50,10),(50,0),(40,0),(35,5),(30,0),(5,0)
                                             ])
        symbols_dict["*"] = rai.CustomPoly([(5,20),(10,25),(10,30),(0,30),(0,40),(10,40),(10,45),(5,50),(5,60),(15,60),(15,55),(20,50),(20,40),(30,40),(30,50),(35,55),(35,60),(45,60),(45,50),(40,45),(40,40),(50,40),(50,30),(40,30),(40,25),(45,20),(45,10),(35,10),(35,15),(30,20),(30,30),(20,30),(20,20),(15,15),(15,10),(5,10)
                                             ])
        symbols_dict["("] = rai.CustomPoly([(0,10),(0,60),(10,70),(25,70),(25,60),(15,60),(10,55),(10,15),(15,10),(25,10),(25,0),(10,0)
                                             ])
        symbols_dict[")"] = rai.CustomPoly([(0,10),(10,10),(15,15),(15,55),(10,60),(0,60),(0,70),(15,70),(25,60),(25,10),(15,0),(0,0)
                                             ])
        symbols_dict["_"] = rai.CustomPoly([(0,10),(50,10),(50,0),(0,0)
                                             ])
        symbols_dict["+"] = rai.CustomPoly([(15,30),(0,30),(0,40),(15,40),(15,55),(25,55),(25,40),(40,40),(40,30),(25,30),(25,15),(15,15)
                                             ])
        symbols_dict["{"] = rai.CustomPoly([(10,10),(10,25),(0,35),(10,45),(10,60),(20,70),(35,70),(35,60),(25,60),(20,55),(20,40),(15,35),(20,30),(20,15),(25,10),(35,10),(35,0),(20,0)
                                            ])
        symbols_dict["}"] = rai.CustomPoly([(0,10),(10,10),(15,15),(15,30),(20,35),(15,40),(15,55),(10,60),(0,60),(0,70),(15,70),(25,60),(25,45),(35,35),(25,25),(25,10),(15,0),(0,0)
                                             ])
        symbols_dict["|"] = rai.CustomPoly([(0,70),(10,70),(10,40),(0,40)
                                             ])
        symbols_dict[":"] = rai.CustomPoly([(0,30),(10,30),(10,20),(0,20)
                                             ])
        symbols_dict['"'] = rai.CustomPoly([(0,70),(10,70),(10,50),(0,50)
                                             ])
        symbols_dict["<"] = rai.CustomPoly([(0,35),(25,60),(30,60),(30,50),(15,35),(30,20),(30,10),(25,10)
                                             ])
        symbols_dict[">"] = rai.CustomPoly([(0,20),(15,35),(0,50),(0,60),(5,60),(30,35),(5,10),(0,10)
                                             ])
        symbols_dict["?"] = rai.CustomPoly([(20,35),(30,45),(35,45),(40,50),(40,55),(35,60),(15,60),(10,55),(10,50),(0,50),(0,60),(10,70),(40,70),(50,60),(50,45),(40,35),(35,35),(30,30),(30,20),(20,20)
                                             ])
        symbols_dict["-"] = rai.CustomPoly([(0,40),(40,40),(40,30),(0,30)
                                             ])
        symbols_dict["="] = rai.CustomPoly([(0,30),(30,30),(30,20),(0,20)
                                             ])
        symbols_dict["["] = rai.CustomPoly([(0,70),(25,70),(25,60),(10,60),(10,10),(25,10),(25,0),(0,0)
                                             ])
        symbols_dict["]"] = rai.CustomPoly([(0,10),(15,10),(15,60),(0,60),(0,70),(25,70),(25,0),(0,0)
                                             ])
        symbols_dict[";"] = rai.CustomPoly([(0,10),(5,10),(10,15),(10,30),(20,30),(20,10),(10,0),(0,0)
                                             ])
        symbols_dict["'"] = rai.CustomPoly([(0,70),(10,70),(10,50),(0,50)
                                             ])
        symbols_dict[","] = rai.CustomPoly([(0,10),(5,10),(10,15),(10,20),(5,20),(5,30),(20,30),(20,10),(10,0),(0,0)
                                             ])
        symbols_dict["."] = rai.CustomPoly([(0,10),(10,10),(10,0),(0,0)
                                             ])
        symbols_dict["/"] = rai.CustomPoly([(0,15),(40,55),(40,65),(50,65),(50,50),(10,10),(10,0),(0,0)
                                             ])


        """ Reading input string and adding them as subpolygons """
        symbols_dict
        string_chars = list(string)
        translation = 0
        
        for i in range(len(string_chars)):
            if string_chars[i] == "," or string_chars[i] == "I" or string_chars[i] == "i":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                translation += 30*scale ##Fontwidht 30
            elif string_chars[i] == "(" or string_chars[i] == "<" or string_chars[i] == ">" or string_chars[i] == "^" or string_chars[i] == ")" or string_chars[i] == "{" or string_chars[i] == "}" or string_chars[i] == "["or string_chars[i] == "]":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                translation += 40*scale ##Fontwidht 40
            elif string_chars[i] == "." or string_chars[i] == "'":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                translation += 20*scale ##Fontwidht 20
            elif string_chars[i] == ":":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,50),(10,50),(10,40),(0,40)]).proxy().scale(scale).move((translation),0)
                translation += 20*scale
            elif string_chars[i] == ";":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(10,50),(20,50),(20,40),(10,40)]).proxy().scale(scale).move((translation),0)
                translation += 30*scale
            elif string_chars[i] == "?":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(20,10),(30,10),(30,0),(20,0)]).proxy().scale(scale).move((translation),0)
                translation += 60*scale
            elif string_chars[i] == "!":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,70),(10,70),(10,20),(0,20)]).proxy().scale(scale).move((translation),0)
                translation += 20*scale
            # elif string_chars[i] == "0":
            #     self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
            #     translation += 60*scale ##Fontwidht 60
            elif string_chars[i] == "|":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,30),(10,30),(10,0),(0,0)]).proxy().scale(scale).move((translation),0)
                translation += 20*scale
            elif string_chars[i] == "|":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,30),(10,30),(10,0),(0,0)]).proxy().scale(scale).move((translation),0)
                translation += 25*scale
            elif string_chars[i] == '"':
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] =rai.CustomPoly([(20,70),(30,70),(30,50),(20,50)]).proxy().scale(scale).move((translation),0)
                translation += 40*scale
            elif string_chars[i] == "%":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,65),(10,65),(10,55),(0,55)]).proxy().scale(scale).move((translation),0)
                self.subcompos[f"Object_{i}_3"] = rai.CustomPoly([(40,10),(50,10),(50,0),(40,0)]).proxy().scale(scale).move((translation),0)
                translation += 60*scale
            elif string_chars[i] == "=":
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                self.subcompos[f"Object_{i}_2"] = rai.CustomPoly([(0,50),(30,50),(30,40),(0,40)]).proxy().scale(scale).move((translation),0)
                translation += 50*scale
            elif string_chars[i] == " ":
                translation += 40*scale
            else:
                self.subcompos[f"Object_{i}"] = symbols_dict[string_chars[i]].proxy().scale(scale).move(translation,0)
                translation += 60*scale
        return

