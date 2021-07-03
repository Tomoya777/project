#C4M1 課題情報更新
'''
***  File Name: kadaiAdd.py
***  Version	: V1.1
***  Designer	: 笠松悠太
***  Date     : 2021/07/03
***  Purpose  : 課題データベースに更新するデータを受け渡す
***
***  Revision:
*** V1.0 : 笠松悠太, 2021.07.03
*** V1.1 : 笠松悠太, 2021.07.04 
    途中です このファイルはたぶん完成？？
'''
import unicodedata
import datetime
from taskdatabase import *

#1つ1つの課題は以下の要素を持っている？
task_datatype = [
    ("task_id" , "U32"), #課題のid. scormからの読み取り時は"idnumber+固有id"とする.
    ("submit_time", "datetime64[s]"), #提出期限
    ("user_id", "U64"), #ユーザ識別番号
    ("subject_name", "U64"), #表示される科目名
    ("task_name", "U64"), #表示される課題名
    ("is_submit", "int"), #提出されているかどうか(1:提出済み,0:提出されていない)
    ("can_submit", "int"), #提出可能かどうか(1:可能,0:可能でない)
    ("submit_url", "U256"), #提出url
    ("estimated_time", "int"), #課題の推定時間(分)(int). scorm抽出時は-1.
    ("progress", "int"), #課題の完成度. scorm抽出時は-1.
    ("remarks", "U256")] #備考,scorm抽出時はなし

def kadaiAdd(task_id, submit_time, user_id, subject_name, task_name, 
             is_submit, can_submit, submit_url, estimated_time, progless, remarks):
    #urlは空
    #入力にエラーがあった場合はerror_arrayにエラー内容を格納
    #この関数の終わりにerror_arrayが空なら次の処理に渡す
    #空じゃなかったらそのエラーをウィンドウに表示する(？)
    error_array = ""

    #この配列を課題情報データベースに送る
    #引数として渡されたデータを上のtask_datetypeに合うように配列に格納していく
    #入れるときにデータが正しいか
    task_array = np.zeros(1, dtype = task_datatype)




    #task_idがあるかどうか
    #task_idがないなら一意に生成する
    if not task_id:
        user_id = "testtest"
        dt_now = datetime.datetime.now()
        dt_now_string =  dt_now.strftime("%Y%m%d%H%M%S")

        task_id = user_id + dt_now_string

    task_array["task_id"] = task_id


    #submit_timeあとまわし
    task_array["submit_time"] = ''
    

    #user_idはそのまま
    task_array["user_id"] = user_id


    #subject_nameがあるかどうか
    if not subject_name:
        subject_name = "科目名未入力"
        error_array += "科目名が未入力です\n"
    #subject_nameが全角半角32文字以内じゃないならエラー文追加
    count = len(subject_name)
    if 32 < count:
        error_array += "科目名は全角半角32文字以内で入力してください\n"
    #subject_nameのバイト数が超えていたらエラー文追加
    count = 0
    for c in subject_name:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    #バイト数が255以下かどうか
    if 255 < count:
        error_array += "科目名は255byte以下になるように入力してください\n"
    task_array["subject_name"] = subject_name

    print(task_name)
    #task_nameがあるかどうか
    if not task_name:
        task_name = "課題名未入力"
        error_array += "課題名が未入力です\n"
    #task_nameが全角半角32文字以内じゃないならエラー文追加
    count = len(task_name)
    if 32 < count:
        error_array += "課題名は全角半角32文字以内で入力してください\n"
    #task_nameのバイト数が超えていたらエラー文追加
    count = 0
    for c in task_name:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1
    #バイト数が255以下かどうか
    if 255 < count:
        error_array += "課題名は255byte以下になるように入力してください\n"
    task_array["task_name"] = task_name


    
    print(task_name)
    is_submit = int(is_submit)
    if is_submit != 0 and is_submit != 1:
        error_array += "提出されているか不明(is_submitが0か1ではない)"
    print("is_submitの値は" + str(is_submit))
    print(type(is_submit))
    task_array["is_submit"] = is_submit


    if can_submit != 0 and can_submit != 1:
        error_array += "提出されているか不明(can_submitが0か1ではない)"
    task_array["can_submit"] = can_submit


    #URLはとりま空
    task_array["submit_url"] = ""


    if estimated_time == 0:
        error_array += "課題にかかる推定時間(分)を1以上で入力してください"
    task_array["estimated_time"] = estimated_time


    task_array["progress"] = progress

    #noteが全角半角128文字以内か
    count = len(remarks)
    if 128 < count:
        error_array += "備考は128文字以内で入力してください"
    task_array["remarks"] = remarks


    #エラー文が無いなら次の関数taskdata_gate()にtask_arrayを渡す
    if len(error_array) == 0:
        #simau()
        taskdata_gate(task_array)
        #しまりがいいから0を返す
        return 0,error_array
    else:
        #エラー文があるなら1とエラー文を返す
        return 1,error_array


def kadaiAddAjax(request):
    print(request.POST.get)
    code,error_array = kadaiAdd(request.POST.get("task_id"), request.POST.get("submit_time"), request.POST.get("user_id"), 
                                request.POST.get("subject_name"), request.POST.get("task_name"), request.POST.get("is_submit"), 
                                request.POST.get("can_submit"), request.POST.get("submit_url"), request.POST.get("estimated_time"), 
                                request.POST.get("progless"), request.POST.get("remarks"))
    if code == 0 :
        return HttpResponse("ok")
    else:
        return HttpResponse(error_array)



"""
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

"""
