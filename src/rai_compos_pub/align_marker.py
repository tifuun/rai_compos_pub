"""
align_marker.py: home to AlignMarker component
"""

import raimad as rai

class HalfAlignMarker(rai.Compo):
    def _make(
            self,
            num_rects: int,
            rect_width: float,
            rect_length: float,
            gap_width: float,
            ):
        for x in range(num_rects):
            self.subcompos[f'rect_{x}'] = (
                rai.RectLW(rect_length, rect_width)
                .proxy()
                .move(0, (rect_width + gap_width) * x)
                )


class AlignMarker(rai.Compo):
    class Layers:
        left = rai.Layer('Left side of marker')
        right = rai.Layer('Right side of marker')

    def _make(
            self,
            num_rects: int = 20,
            rect_width: float = 10,
            rect_length: float = 25,
            gap_width: float = 10,
            abberation: float = 1.5
            ):
        self.subcompos.left = HalfAlignMarker(
            num_rects,
            rect_width,
            rect_length,
            gap_width
            ).proxy()
        self.subcompos.right = (
            self.subcompos.left
            .proxy()
            .scale(abberation)
            .snap_right(
                self.subcompos.left
                )
            )

if __name__ == '__main__':
    rai.show(AlignMarker())

