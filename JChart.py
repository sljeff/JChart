from PIL import Image, ImageFont, ImageDraw
from os import path
from collections import OrderedDict


_colorWhite = (255, 255, 255)
_colorBlack = (0, 0, 0)
_barColor = (0, 153, 204)
_noColor = (51, 255, 255)
_textColor = (51, 255, 51)
_numColor = (51, 255, 255)
_titleHeight = 50
if path.isfile('msyh.ttc'):
    _fontName = 'msyh.ttc'
else:
    _fontName = None
_fontTitle = ImageFont.truetype(font=_fontName, size=20)
_fontText = ImageFont.truetype(font=_fontName, size=16)
_fontNo = ImageFont.truetype(font=_fontName, size=12)
_fontNum = ImageFont.truetype(font=_fontName, size=10)
# for horizontal bar chart
_picWidth = 500
_barHeight = 15
_spacing4H = 30
_maxLineWidth = 300
# for vertical bar chart
_picHeight = 500
_barWidth = 15
_spacing4V = 30
_maxLineHeight = 300


class JChart:
    def __init__(self, data):
        """
        init
        :param data: dict or OrderedDict
        """
        self._data = data
        self._maxVal = max(data.values())
        self._number = len(data)

    def _createBackground(self, width, height, backgroundColor=_colorBlack):
        return Image.new("RGB", (width, height), backgroundColor)

    def _getHeight(self):
        """
        calculate and return the height for horizontal bar chart
        :return: int, height of pic
        """
        return (_barHeight+_spacing4H) * (self._number+1) + _titleHeight

    def _makeHBar(self, saveName, data):
        """
        make picture of horizontal bar chart
        :param saveName: str
        :return: None
        """
        if path.splitext(saveName)[1] == '':
            saveName += '.jpg'
        picHeight = self._getHeight()
        whole = self._createBackground(_picWidth, picHeight)
        startWidth = 150
        startHeight = 50
        draw = ImageDraw.Draw(whole)
        index = 1
        for key, value in data.items():
            itemWidth = int(_maxLineWidth * value / self._maxVal) or 1
            startPos = (startWidth, startHeight)
            endPos = (startWidth+itemWidth, startHeight+_barHeight)
            draw.rectangle([startPos, endPos], fill=_barColor, outline=_colorWhite)
            draw.text((20, startHeight-5), str(index), font=_fontNo, fill=_noColor)
            draw.text((50, startHeight-10), str(key), font=_fontText, fill=_textColor)
            draw.text((50, startHeight+10), str(value), font=_fontNum, fill=_numColor)
            startHeight += _barHeight + _spacing4H
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
            orderIndex = 0 if orderBy=='k' else 1
            data = OrderedDict(sorted(self._data.items(), key=lambda t: t[orderIndex], reverse=reverse))
        self._makeHBar(saveName, data)
        print('picture saved as %s' % saveName)
