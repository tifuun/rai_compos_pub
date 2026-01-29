import raimad as rai

class DektakModule(rai.Compo):
    def _make(
        self,
        kvlayer1,
        kvlayer2,
        kvlayer3,
    ):
        num_layer1, layer1 = kvlayer1
        num_layer2, layer2 = kvlayer2
        num_layer3, layer3 = kvlayer3

        top_square_1 = rai.RectLW(320, 80).proxy().map(layer1)
        square_2 = rai.RectLW(290, 120).proxy().map(layer2)
        square_3 = rai.RectLW(290, 120).proxy().map(layer3)
        bot_square_1 = rai.RectLW(320, 80).proxy().map(layer1)

        top_square_1.bbox.top_mid.to((0, 140))
        bot_square_1.bbox.bot_mid.to((0, -140))
        square_2.bbox.top_left.to(rai.add(top_square_1.bbox.top_left, (-80, -40)))
        square_3.bbox.bot_right.to(rai.add(bot_square_1.bbox.bot_right, (80, 40)))

        self.subcompos.top_square_1 = top_square_1
        self.subcompos.text_top_square_1 = (
            RAIText(num_layer1).proxy().map(layer1).bbox.mid_left.to(rai.add(top_square_1.bbox.mid_right, (135, 0)))
        )
        self.subcompos.bot_square_1 = bot_square_1
        self.subcompos.text_bot_square_1 = (
            RAIText(num_layer1).proxy().map(layer1).bbox.mid_right.to(rai.add(bot_square_1.bbox.mid_left, (-135, 0)))
        )
        self.subcompos.square_2 = square_2
        self.subcompos.text_square_2 = (
            RAIText(num_layer2)
            .proxy()
            .map(layer2)
            .bbox.mid_right.to((self.subcompos.text_bot_square_1.bbox.mid_right[0], square_2.bbox.mid_left[1]))
        )
        self.subcompos.square_3 = square_3
        self.subcompos.text_square_3 = (
            RAIText(num_layer3)
            .proxy()
            .map(layer3)
            .bbox.mid_left.to((self.subcompos.text_top_square_1.bbox.mid_left[0], square_3.bbox.mid_right[1]))
        )

class DektakAssembly(rai.Compo):
    def _make(self, *args):
        sep = 400

        self.subcompos.dektak1 = DektakModule(
            ("1", "_NbTiN"),
            ("3", "_Polyimide"),
            ("4", "_Aluminium_COARSE"),
        ).proxy()
        self.subcompos.dektak2 = (
            DektakModule(
                ("1", "_NbTiN"),
                ("3", "_Polyimide"),
                ("4", "_Aluminium_COARSE"),
            )
            .proxy()
            .movey(sep)
        )
        self.subcompos.dektak3 = (
            DektakModule(
                ("1", "_NbTiN"),
                ("3", "_Polyimide"),
                ("4", "_Aluminium_COARSE"),
            )
            .proxy()
            .movey(2 * sep)
        )
        self.subcompos.dektak4 = (
            DektakModule(
                ("1", "_NbTiN"),
                ("2", "_NbTiN_EB_COARSE"),
                ("4", "_Aluminium_COARSE"),
            )
            .proxy()
            .movey(3 * sep)
        )
        self.subcompos.dektak5 = (
            DektakModule(
                ("1", "_NbTiN"),
                ("2", "_NbTiN_EB_COARSE"),
                ("4", "_Aluminium_COARSE"),
            )
            .proxy()
            .movey(4 * sep)
        )

        self.subcompos.polyimide_dektak = rai.RectLW(200, 200).proxy().map("_Polyimide").movey(-sep)
        self.subcompos.perminex_dektak = rai.RectLW(200, 200).proxy().map("_Perminex").movey(5 * sep)
        self.subcompos.nbtin_remove_dektak = rai.RectLW(250, 250).proxy().map("_NbTiN").movey(5 * sep)
