import raimad as rai

class RLTaper(rai.Compo):
    r"""
    Taper component.

    Takes in two compos `left` and `right`,
    and constructs self to connect the bbox of `left`
    to the bbox of `right`,
    like this:
     ___________ 
    |           |\
    |           | \
    |           |  \ ___________
    |  `left`   |   |  `right`  |
    |           |   |___________|
    |           |  /
    |           | /
    |___________|/

    This is a purely geometric component,
    i.e. geometry defined directly, without subcompos.
    """
    def _make(self, left: rai.Compo, right: rai.Compo):
        self.geoms.update({
            'root': [
                [
                    tuple(left.bbox.top_right),
                    tuple(right.bbox.top_left),
                    tuple(right.bbox.bot_left),
                    tuple(left.bbox.bot_right),
                    ]
                ]
            })


class MSLHalf(rai.Compo):
    def _make(self):
        """Left half of the MSL structure."""
        step1 = rai.RectLW(20, 20).proxy()
        step2 = rai.RectLW(10, 12).proxy()
        step3 = rai.RectLW(12, 5).proxy()

        # Will not be added to design,
        # just a placeholder to create final taper
        step4 = rai.RectLW(6, 2).proxy()

        # Position the step
        step2.snap_right(step1).movex(10)
        step3.snap_right(step2).movex(10)
        step4.snap_right(step3).movex(10)

        # create the tapers
        taper1 = RLTaper(step1, step2).proxy()
        taper2 = RLTaper(step2, step3).proxy()
        taper3 = RLTaper(step3, step4).proxy()

        # register the subcompos
        self.subcompos.step1 = step1
        self.subcompos.step2 = step2
        self.subcompos.step3 = step3
        self.subcompos.taper1 = taper1
        self.subcompos.taper2 = taper2
        self.subcompos.taper3 = taper3

        # Declare marks
        self.marks.tip = step4.bbox.mid_left
        self.marks.step1_mid = step1.bbox.mid

class MSLHalves(rai.Compo):
    """Two halves of the MSL structure joined together with a signal line"""
    def _make(self):
        line = rai.RectLW(20, 2).proxy()
        left = MSLHalf().proxy()
        right = MSLHalf().proxy()

        left_resist = MSLHalf().proxy()
        right_resist = MSLHalf().proxy()

        right.vflip()
        right_resist.vflip()

        left_resist.scale(1.2)
        right_resist.scale(1.2)

        # could also use regular bbox snapping here,
        # but I think it's better to align based on mark.
        # What if MSLHalf is changed to have geometry
        # that pokes out above the right side?
        left.marks.tip.to(line.bbox.mid_left)
        right.marks.tip.to(line.bbox.mid_right)

        left_resist.marks.step1_mid.to(left.marks.step1_mid)
        right_resist.marks.step1_mid.to(right.marks.step1_mid)

        # Map layers
        # (could use shorthand here, e.g.
        # left.map('conductor')),
        # but I wanna be explicit
        line.map({'root': 'conductor'})
        left.map({'root': 'conductor'})
        right.map({'root': 'conductor'})
        left_resist.map({'root': 'resist'})
        right_resist.map({'root': 'resist'})

        # Register subcompos
        self.subcompos.line = line
        self.subcompos.left = left
        self.subcompos.right = right
        self.subcompos.left_resist = left_resist
        self.subcompos.right_resist = right_resist

class Headphones(rai.Compo):
    def _make(self):
        band = rai.RectLW(5, 1).proxy()
        stem_l = rai.RectLW(1, 5).proxy()
        stem_r = rai.RectLW(1, 5).proxy()
        cup_l = rai.RectLW(2, 2).proxy()
        cup_r = rai.RectLW(2, 2).proxy()

        stem_l.bbox.top_right.to(band.bbox.top_left)
        stem_r.bbox.top_left.to(band.bbox.top_right)

        cup_l.snap_below(stem_l)
        cup_r.snap_below(stem_r)

        self.subcompos.band = band
        self.subcompos.cup_l = cup_l
        self.subcompos.cup_r = cup_r
        self.subcompos.stem_l = stem_l
        self.subcompos.stem_r = stem_r

class Snake(rai.Compo):
    """
    Meander at the top middle of the VialessMSL chip.

    Once raimad.path / raimad.tl get reimplemented,
    we will be able to construct transmission lines
    just by passing points and parameters.
    But for now we just build it by hand like a toy railroad.
    """
    def _make(self):
        straight1 = rai.RectLW(2, 1).proxy()
        straight2 = straight1.shallow_copy()
        straight3 = straight1.shallow_copy()
        straight4 = straight1.shallow_copy()

        bend1 = rai.AnSec.from_auto(
            rmid=2,
            dr=1,
            thetamid=0,
            dtheta=rai.semicircle,
            ).proxy()
        bend2 = bend1.shallow_copy().vflip()
        bend3 = bend1.shallow_copy()

        bend1.bbox.bot_left.to(straight1.bbox.bot_right)
        straight2.bbox.top_right.to(bend1.bbox.top_left)
        bend2.bbox.bot_right.to(straight2.bbox.bot_left)
        straight3.bbox.top_left.to(bend2.bbox.top_right)
        bend3.bbox.bot_left.to(straight3.bbox.bot_right)
        straight4.bbox.top_right.to(bend3.bbox.top_left)

        self.subcompos.bend1 = bend1
        self.subcompos.bend2 = bend2
        self.subcompos.bend3 = bend3
        self.subcompos.straight1 = straight1
        self.subcompos.straight2 = straight2
        self.subcompos.straight3 = straight3
        self.subcompos.straight4 = straight4

        # There will be a small gap between the bends and straight segments.
        # RAIMAD bug, will fix!!


class VialessMSL(rai.Compo):
    """via-less MSL test chip draft."""
    def _make(self):
        halves = MSLHalves().proxy()
        headphones = Headphones().proxy()
        resist_valley = rai.RectLW(20, 40).proxy()
        snake = Snake().proxy()

        # Subcompos introspection is generally discourages,
        # but since this is quick draft,
        # and since `halves` is defined in the same file,
        # it should be fine.
        headphones.snap_below(halves.subcompos.line).movey(-2)
        snake.snap_above(halves.subcompos.line).movey(2)

        resist_valley.bbox.mid.to(halves.bbox.mid)

        halves.map({
            'resist': 'nbtin_hole',
            'conductor': 'al',
            })
        headphones.map({
            'root': 'al',
            })
        resist_valley.map({
            'root': 'nbtin_hole',
            })
        snake.map({
            'root': 'al',
            })

        self.subcompos.snake = snake
        self.subcompos.halves = halves
        self.subcompos.headphones = headphones
        self.subcompos.resist_valley = resist_valley
        

