#C4M2 課題情報追加

import unicodedata
import datetime



def kadai_regist(kamoku,kadai,date,note):
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


   task_id = 'test'
    submit_time = date
    user_id = 'test'
    task_name = 'test'
    subject_name = 'test'
    is_submit = '未提出'
    can_submit_overtime = '不可'
    estimated_time = 1
    progless = 0