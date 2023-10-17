import numpy as np
from scipy.interpolate import make_interp_spline
import argparse as ap
import os


class Stealer:
    def __init__(self):
        self.eq = [20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000,
                   2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]

        params = self.parse()
        steal = self.read_eq(params.steal, params.peace)
        apply = self.read_eq(params.apply, params.peace)

        self.create_eq(steal, apply)

    def parse(self):
        parser = ap.ArgumentParser(
            prog="soundstage-stealer"
        )

        parser.add_argument('-s', '--steal', help='Input Graphic EQ file from which you want to "steal" the soundstage',
                            required=True)
        parser.add_argument('-a', '--apply',
                            help='Input Graphic EQ file to which you want to apply the "stolen" soundstage',
                            required=True)
        parser.add_argument('--peace', action='store_true', required=False, help="If you exported "
                                                                                            "GraphicEQ from"
                                                                                            "Peace"
                                                                                            "add this option to the "
                                                                                            "commandline")

        return parser.parse_args()

    def read_eq(self, file, apo):
        freq = []
        deci = []

        if apo:
            eq_p = open(file, 'r', encoding='utf-8').readline()[10:].split(" ")

            for i in eq_p:
                if "f" in i:
                    freq.append(int(i.split('"')[1]))
                elif 'v' in i:
                    deci.append(float(i.split('"')[1]))

        else:
            eq = open(file, 'r', encoding='utf-8').readline()[11:].split("; ")

            for i in eq:
                freq.append(int(i.split(' ')[0]))
                deci.append(float(i.split(' ')[1]))

        spline = make_interp_spline(np.array(freq), np.array(deci))
        freq_ = np.linspace(1, 22050, 22050)
        deci_ = spline(freq_)

        return [freq_.tolist(), deci_.tolist()]

    def create_eq(self, eq1, eq2):
        total_deci = [(x * -1) + y for x, y in zip(eq1[1], eq2[1])]
        final = {}

        for freq, deci in zip(eq1[0], total_deci):
            if round(freq) in self.eq:
                final[round(freq)] = round(deci, 1)

        # AutoEQ GraphicEQ file for Wavelet
        file = open(os.path.join(os.getcwd(), "GraphicEQ.txt_AutoEQ"), 'w', encoding='utf-8')
        file.write("GraphicEQ:")
        for x, y in final.items():
            if x == 20000:
                file.write(f" {x} {y}")
            else:
                file.write(f" {x} {y};")
        file.close()

        # Peace GraphicEQ file
        file = open(os.path.join(os.getcwd(), "GraphicEQ_Peace.txt"), 'w', encoding='utf-8')
        file.write("GraphicEQ:")
        f = 0
        d = 0
        for x in final.keys():
            file.write(f'f{f}="{x}" ')
            f += 1
        file.write('FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" ')
        for y in final.values():
            file.write(f'v{d}="{y}"')
            d += 1
        file.close()


if __name__ == '__main__':
    Stealer()
