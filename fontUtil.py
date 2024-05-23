from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
import matplotlib.pyplot as plt

fullPoints = []

class SamplePen(BasePen):
    def __init__(self, glyphSet, sample_rate=10):
        super().__init__(glyphSet)
        self.points = []
        self.sample_rate = sample_rate

    def _moveTo(self, p0):
        self.points.append(p0)

    def _lineTo(self, p1):
        self.points.append(p1)

    def _curveToOne(self, p1, p2, p3):
        self._sample_cubic_bezier(self._getCurrentPoint(), p1, p2, p3)

    def _qCurveToOne(self, p1, p2):
        self._sample_quadratic_bezier(self._getCurrentPoint(), p1, p2)

    def _closePath(self):
        fullPoints.append(self.points[::])
        self.points.clear()

    def _sample_cubic_bezier(self, p0, p1, p2, p3):
        num_samples = self.sample_rate
        for i in range(1, num_samples):
            t = i / num_samples
            x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
            self.points.append((x, y))
        self.points.append(p3)

    def _sample_quadratic_bezier(self, p0, p1, p2):
        num_samples = self.sample_rate
        for i in range(1, num_samples):
            t = i / num_samples
            x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
            y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
            self.points.append((x, y))
        self.points.append(p2)

def get_glyph_name_for_character(font, character):
    cmap = font.getBestCmap()
    return cmap.get(ord(character))

def get_glyph_points(glyph_name, sample_rate=10):
    global font
    glyph_set = font.getGlyphSet()
    
    glyph = glyph_set[glyph_name]
    pen = SamplePen(glyph_set, sample_rate)
    glyph.draw(pen)

def get_glyph_metrics(glyph_name):
    return font['hmtx'][glyph_name]

font_path = 'Roboto-Bold.ttf'
font = TTFont(font_path)
sample_rate = 5

glyph_name = "Ğ"
glyph_name = get_glyph_name_for_character(font, glyph_name)
get_glyph_points(glyph_name, sample_rate)

advance_width, left_side_bearing = get_glyph_metrics(glyph_name)
print(f"Glyph: {glyph_name}, Advance Width: {advance_width}, Left Side Bearing: {left_side_bearing}")

# glyph_name = "C"
# glyph_name = get_glyph_name_for_character(font, glyph_name)
# glyph_points.extend(get_glyph_points(glyph_name, sample_rate))

# advance_width, left_side_bearing = get_glyph_metrics(glyph_name)
# print(f"Glyph: {glyph_name}, Advance Width: {advance_width}, Left Side Bearing: {left_side_bearing}")

colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "black", "gray"]

# i = 0
# for points in fullPoints:
#     for point in points:
#         plt.plot(point[0], point[1], ".", color=colors[i])
    
#     i += 1

# plt.show()