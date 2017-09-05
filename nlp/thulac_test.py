import thulac

thu1 = thulac.thulac(seg_only=True)
txt = '分词和词性标注程序'
r = thu1.cut(txt,text=True)
print(r)
