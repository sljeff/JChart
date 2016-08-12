# JChart
一个简单的图表制作工具
## 准备
需要Pillow  
`pip install Pillow`  

PS：如果你的系统里没有simhei.ttf字体的话，请在JChart.py同目录里放置一个simhei.ttf文件或者把`_fontname`改为已有的字体
## 使用
### 例子
```
import JChart

data={
  '陆婷': 71639.6, '李艺彤': 169971.4, '冯薪朵': 88598.8, '黄婷婷': 130258.3,
  '鞠婧祎': 230752.7, '曾艳芬': 88656.8, '莫寒': 73362.6, '张语格': 66867.5
}
jc = JChart.JChart(data)
jc.makeBar('result/Hbar', orderBy='v', reverse=True)

jc.makeBar('result/Vbar', orderBy='v', reverse=False, isHorizontal=False)

options = {
  'backgroundColor': (0, 152, 102),
  'barColor': (0, 0, 0)
}
jc2 = JChart.JChart(data, options)
jc2.makeBar('result/Hbar2', orderBy='v', reverse=True)
```

结果  
result/Hbar.jpg  
![](http://o8qs2v45f.bkt.clouddn.com/JChart/Hbar.jpg)  
result/Vbar.jpg  
![](http://o8qs2v45f.bkt.clouddn.com/JChart/Vbar.jpg)  
result/Hbar2.jpg  
![](http://o8qs2v45f.bkt.clouddn.com/JChart/Hbar2.jpg)  
## 说明
### `JChart.JChart`  
#### `JChart.JChart(data, options=None)`  
**data**: dict或OrderedDict  
*因为dict是没有顺序的，所以如果希望你的输出是按照特定顺序的就要使用OrderedDict。如果只需要按照data的key或者value排序可以直接使用makeBar的`orderBy`参数*  
  
**options**: 一个dict，它的value都应该是三个元素(分别代表RGB)的tuple，可以放置  
*条形颜色barColor  
序号颜色noColor  
key文字颜色keyColor  
value文字颜色valueColor  
背景色backgroundColor*  

#### `JChart.makeBar(saveName, orderBy='none', reverse=False, isHorizontal=True)`
**saveName**: str  
*保存的图片文件的名字，后缀可以为Pillow文档的image-file-formats页面列出的图片格式。如果不带后缀默认为jpg。*  
  
**orderBy**: str  
*柱状图的显示按照什么值来排序，可以为'k'或'v'，分别代表key和value。（为了排序请确保key或者value的类型一致）*  
  
**reverse**: bool  
*在OrderBy为'k'或'v'的情况下，如果reverse为False则柱状图会从低到高排序，如果为True则从高到低*  
  
**isHorizontal**: bool  
*如果为True则输出柱子为横向的条形图，如果为False则输出柱子为纵向的柱状图*  
