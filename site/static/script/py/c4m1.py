#C4M1 課題情報更新

import unicodedata
import datetime

def c4m1(kamoku,kadai,date,note):
    print("あああ")

    #kamokuのバイト数を数える
    count = 0
    for c in kamoku:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    #バイト数が255以下かどうか
    if count > 255:
        print("バイト数エラーです")


    #kadaiのバイト数を数える
    count = 0
    for c in kadai:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    #バイト数が255以下かどうか
    if count > 255:
        print("バイト数エラーです")


    #dateがDATETIME型かどうか
    if type(date) is datetime.datetime:
        print("dateはdatetime型です")
    else :
        print("dateはdatetime型ではありません")


    #kamokuが全角半角32文字以内か
    count = len(kamoku)
    if 32 < count:
        print("科目名は32文字以内で入力してください")
    else:
        print("科目名は32文字以内です")


    #kadaiが全角半角32文字以内か
    count = len(kadai)
    if 32 < count:
        print("科目名は32文字以内で入力してください")
    else:
        print("科目名は32文字以内です")


    #noteが全角半角128文字以内か
    count = len(note)
    if 128 < count:
        print("備考は128文字以内で入力してください")
    else:
        print("備考は128文字以内です")    
    
    







uiha = "あいばういは"
aumau = "ausaumau"
mayuzumi = "黛kai"

name = [uiha,aumau,mayuzumi]

print(name)

for liver in name:
    count = 0
    for c in liver:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    print(count)

print()
print()
print()

for liver in name:
    print(len(liver))

a = 112
b = 12.3
c = "うつつｔ"

print(type(a) is int)
print(type(b) is int)
print(type(c) is str)

test = datetime.datetime.now()
print(type(test) is datetime.datetime)
if type(test) is datetime.datetime:
    print("おけ")