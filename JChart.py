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
_picHeight = 600
_barWidth = 15
_spacingForV = 60
_maxLineHeight = 400


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

    def _makeBar(self, saveName, data, isHorizontal):
        """
        make bar chart picture
        :type saveName: str
        :type isHorizontal: bool
        :return: None
        """
        picWidth = _picWidth
        picHeight = _picHeight
        if isHorizontal:
            picHeight = (_barHeight + _spacingForH) * (self._number + 1)
            startWidth = 150
            startHeight = 40
            maxLength = _maxLineWidth
            getEndPos = lambda pos, length: (pos[0] + length, pos[1] + _barHeight)
            updateStartPos = lambda pos: (pos[0], pos[1] + _barHeight + _spacingForH)
            getNoPos = lambda w, h: (20, h - 5)
            getKeyPos = lambda w, h: (50, h - 10)
            getValuePos = lambda w, h:(50, h + 10)
        else:
            picWidth = (_barWidth + _spacingForV) * (self._number + 1)
            startWidth = 50
            startHeight = 470
            maxLength = _maxLineHeight
            getEndPos = lambda pos, length: (pos[0] + _barWidth, pos[1] - length)
            updateStartPos = lambda pos: (pos[0] + _barWidth + _spacingForV, pos[1])
            getNoPos = lambda w, h: (w + 5, 550)
            getKeyPos = lambda w, h: (w - 10, 500)
            getValuePos = lambda w, h: (w - 10, 520)
        whole = self._createBackground(picWidth, picHeight)
        draw = ImageDraw.Draw(whole)
        index = 1
        for key, value in data.items():
            itemLength = int(maxLength * value / self._maxVal) or 1
            startPos = (startWidth, startHeight)
            endPos = getEndPos(startPos, itemLength)
            draw.rectangle([startPos, endPos], fill=self._barColor, outline=_colorWhite)
            draw.text(getNoPos(startWidth, startHeight), str(index), font=_fontNo, fill=self._noColor)
            draw.text(getKeyPos(startWidth, startHeight), str(key), font=_fontKey, fill=self._keyColor)
            draw.text(getValuePos(startWidth, startHeight), str(value), font=_fontValue, fill=self._valueColor)
            startWidth, startHeight = updateStartPos(startPos)
            index += 1
        del draw
        whole.save(saveName)

    def makeBar(self, saveName, orderBy='none', reverse=False, isHorizontal=True):
        """
        make bar chart picture
        :type saveName: str
        :type reverse: bool
        :type isHorizontal: bool
        :param orderBy: str, 'k' or 'v'
        :return: None
        """
        if orderBy != 'k' and orderBy != 'v':
            data = self._data
        else:
            orderIndex = 0 if orderBy == 'k' else 1
            data = OrderedDict(sorted(self._data.items(), key=lambda t: t[orderIndex], reverse=reverse))

        if path.splitext(saveName)[1] == '':
            saveName += '.jpg'

        self._makeBar(saveName, data, isHorizontal)
        print('picture saved as %s' % saveName)
