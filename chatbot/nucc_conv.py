#!/usr/bin/env python3
"""
名大会話コーパスをcorpusenactor用に変換

名大会話コーパスは以下のように記述されている。

```
＠データ２（６０分）
＠収集年月日：２００１年１０月１６日
＠参加者F023：女性４０代後半、岐阜県出身、愛知県幡豆郡在住
＠参加者F128：女性２０代前半、愛知県西尾市出身、同市在住
％ｃｏｍ：F023は出身地に２６歳まで居住。
F107：今度はーイギリスにもアメリカと同様のテロが起こるだろうって言ったんだってよ。
F128：へえー。
F023：ほんとお。
F107：うん。
きのうのテレビで声明を出したとか言って、ビンラディン氏がイギリスにもアメリカと同様のことが起こるだろうって言ったじゃんね。
F128：うそー。
F107：へーとか思ってさ。
```

これを以下のようなルールで変換する。
・行頭が'＠'または'%'だった場合は先頭に'# 'を足してコメント行にする
・入力ファイルの会話本体はコロン区切りテキストで一列目は発言者名、二列目は発言内容とみなす。これを
タブ区切りテキストに変換して出力する。
行の先頭に発言者名がない場合は、直前の発言者名で補う。
"""

import sys
import os
import codecs
import glob

if len(sys.argv) == 1:
    print (
        f"{__file__} - 名大会話コーパスをtsv形式に変換\n"
        f"{__file__} <input file> 入力ファイルを指定\n"
        )
    quit()

path = sys.argv[1]

with codecs.open(path,"r",encoding="utf-8") as f:
    lines = f.readlines()

lines = [x.rstrip() for x in lines]

fruits = []
name = "noname"
for line in lines:

    if line.startswith('＠') or line.startswith('％') or line.startswith('<'):
        fruits.append(f"# {line}")
        continue

    nodes = line.split('：',1)
    if len(nodes) == 1:
        fruits.append(f"{name}\t{nodes[0]}")
    else:
        fruits.append("\t".join(nodes))
        name = nodes[0]


with codecs.open(f"{path}.tsv","w",encoding="utf-8") as f:
    f.write("\n".join(fruits))
