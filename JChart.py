from PIL import Image, ImageFont, ImageDraw
from os import path
from collections import OrderedDict


_colorWhite = (255, 255, 255)
_colorBlack = (0, 0, 0)
_titleHeight = 50
if path.isfile('msyh.ttc'):
    _fontname = 'msyh.ttc'
else:
    _fontname = None
_fontTitle = ImageFont.truetype(font=_fontname, size=20)
_fontKey = ImageFont.truetype(font=_fontname, size=16)
_fontNo = ImageFont.truetype(font=_fontname, size=12)
_fontValue = ImageFont.truetype(font=_fontname, size=10)
# for horizontal bar chart
_picWidth = 500
_barHeight = 15
_spacingForH = 30
_maxLineWidth = 300
# for vertical bar chart
_picHeight = 500
_barWidth = 15
_spacingForV = 30
_maxLineHeight = 300


class JChart:
    def __init__(self, data, options=None):
        """
        init
        :param data: dict or OrderedDict
        :param options: dict, barColor: 3-tuple
                               noColor: 3-tuple
                               keyColor: 3-tuple
                               valueColor: 3-tuple
                               backgroundColor: 3-tuple
        """
        if options == None:
            options = {}
        self._barColor = options.get('barColor') or (0, 153, 204)
        self._noColor = options.get('noColor') or (51, 255, 255)
        self._keyColor = options.get('keyColor') or (51, 255, 51)
        self._valueColor = options.get('valueColor') or (51, 255, 255)
        self._backgroundColor = options.get('backgroundColor') or _colorBlack
        self._data = data
        self._maxVal = max(data.values())
        self._number = len(data)

    def _createBackground(self, width, height):
        return Image.new("RGB", (width, height), self._backgroundColor)

    def _getHeight(self):
        """
        calculate and return the height for horizontal bar chart
        :return: int, height of pic
        """
        return (_barHeight + _spacingForH) * (self._number + 1) + _titleHeight

    def _makeHBar(self, saveName, data):
        """
        make picture of horizontal bar chart
        :param saveName: str
        :return: None
        """
        picHeight = self._getHeight()
        whole = self._createBackground(_picWidth, picHeight)
        startWidth = 150
        startHeight = 70
        draw = ImageDraw.Draw(whole)
        index = 1
        for key, value in data.items():
            itemWidth = int(_maxLineWidth * value / self._maxVal) or 1
            startPos = (startWidth, startHeight)
            endPos = (startWidth+itemWidth, startHeight+_barHeight)
            draw.rectangle([startPos, endPos], fill=self._barColor, outline=_colorWhite)
            draw.text((20, startHeight-5), str(index), font=_fontNo, fill=self._noColor)
            draw.text((50, startHeight-10), str(key), font=_fontKey, fill=self._keyColor)
            draw.text((50, startHeight+10), str(value), font=_fontValue, fill=self._valueColor)
            startHeight += _barHeight + _spacingForH
            index += 1
        del draw
        whole.save(saveName)

    def makeHBar(self, saveName, orderBy='none', reverse=False):
        """
        make picture of horizontal bar chart
        :param saveName: str
        :param orderBy: str, 'k' or 'v'
        :param reverse: bool
        :return: None
        """
        if orderBy != 'k' and orderBy != 'v':
            data = self._data
        else:
            orderIndex = 0 if orderBy == 'k' else 1
            data = OrderedDict(sorted(self._data.items(), key=lambda t: t[orderIndex], reverse=reverse))

        if path.splitext(saveName)[1] == '':
            saveName += '.jpg'

        self._makeHBar(saveName, data)
        print('picture saved as %s' % saveName)
