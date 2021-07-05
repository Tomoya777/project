#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***  File Name		: taskdatabase.py
***  Version		: V1.5
***  Designer		: 熊谷 直也
***  Date			: 2021.07.05
***  Purpose       	: データベース関連
***
*** Revision :
*** V1.0 : 熊谷 直也, 2021.07.01
*** V1.3 : 熊谷 直也, 2021.07.05 M2 二次元配列への対応と初期値の条件追加、変数格納順の変更
*** V1.4 : 熊谷 直也, 2021.07.05 配列→構造体
*** V1.5 : 熊谷 直也, 2021.07.05 備考欄の初期値処理の追加

"""


import sqlite3
import numpy as np
import os  # ファイル存在確認
import datetime
import pandas as pd
import struct

task_datatype = [
    ("task_id", "U32"),  # 課題のid. scombからの読み取り時は"idnumber+固有id"とする.
    ("submit_time", "datetime64[s]"),  # 提出期限
    ("user_id", "U64"),  # ユーザ識別番号
    ("subject_name", "U64"),  # 表示される科目名
    ("task_name", "U64"),  # 表示される課題名
    ("is_submit", "int"),  # 提出されているかどうか(1:提出済み,0:提出されていない)
    ("can_submit", "int"),  # 提出可能かどうか(1:可能,0:可能でない)
    ("submit_url", "U256"),  # 提出url
    ("estimated_time", "int"),  # 課題の推定時間(int). scomb抽出時は-1.
    ("progress", "int"),  # 課題の完成度. scomb抽出時は-1.
    ("remarks", "U256")]  # 備考欄
dbname = "task.db"  # データベースのファイル名

# C7M1 課題情報管理部主処理
# 上位の層から上位の層から来た課題データを確認し、変更点をデータベースに格納する。
# 一部データが欠けている際には必要なら書き入れる。


def taskdata_gate(task_array):
    try:
        conn = sqlite3.connect(dbname)  # データベース接続
        cur = conn.cursor()

        sqlite3.register_adapter(np.int64, int)  # int32 or int64をintへ
        sqlite3.register_adapter(np.int32, int)

       # task_array = np.array(task_array)  # numpyの機能を使用するため、念の為ndarray化
        nagasa = len(task_array)  # taskの個数を取得
        # print(nagasa)
        # テーブルがなければテーブル作成(task_arrayにデータがなければ作成されません)
        cur.execute("CREATE TABLE IF NOT EXISTS taskdata(task_id STRING PRIMARY KEY, \
                                     submit_time datetime,\
                                     user_id STRING,\
                                     subject_name STRING,\
                                     task_name STRING,\
                                     is_submit INT,\
                                     can_submit INT,\
                                     submit_url STRING,\
                                     estimated_time INT,\
                                     progress INT,\
                                     remarks STRING )")

        for i in range(nagasa):  # taskごとにそれぞれ処理
            # print(task_array)
            # submit_timeはnumpyのdatetime64型であるから、ndarrayのメソッドastypeでdatetime.datetime型へ変換
            # 参考 https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html
            dt64 = task_array[i]['submit_time']
            # print(dt64)
            dt_dt = dt64.astype(datetime.datetime)
            # print(dt_dt)
            task_array[i]['submit_time'] = dt_dt

            cur.execute(
                "SELECT * FROM taskdata WHERE task_id=?", [task_array[i]['task_id']])  # SELECT文でデータベースにすでに入ってるタスクと、処理を行うタスクを比較
            task_fetch = cur.fetchone()  # fetchoneでSELECT文の結果を取得(リストになっている)
            """task_array[i]['datetime'] = struct.unpack(
                '<q', task_array[i]['datetime'])
            print(task_fetch[1])"""

            """task_array[i]['estimated_time'] = struct.unpack(
                '<q', task_array[i]['estimated_time'])"""

            # SELECT結果がNoneであればINSERT、重複していたらREPLACE
            if task_fetch == None:
                # estimated_time(課題の推定時間)と、progress(課題の完成度)、remarks()備考欄は値が-1で生成されてしまうので、それぞれ初期値として60、0、nullを代入。
                if task_array[i]['estimated_time'] == -1 and task_array[i]['progress'] == -1 and task_array[i]['remarks']:
                    task_array[i]['estimated_time'] = 60
                    task_array[i]['progress'] = 0
                    task_array[i]['remarks'] = "null"
                cur.execute("INSERT INTO taskdata VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                    task_array[i]['task_id'],
                    dt_dt,  # task_arrayに格納したdatetimeを挿入できなかったので直接出力
                    task_array[i]['user_id'],
                    task_array[i]['subject_name'],
                    task_array[i]['task_name'],
                    task_array[i]['is_submit'],
                    task_array[i]['can_submit'],
                    task_array[i]['submit_url'],
                    task_array[i]['estimated_time'],
                    task_array[i]['progress'],
                    task_array[i]['remarks']])
                # print("inserted")
            elif task_array[i]['task_id'] == task_fetch[0]:
                # Scombからの抽出時、estimated_time(課題の推定時間)と、progress(課題の完成度)は値が-1であるので、その2つの変数は更新しない
                if task_array[i]['estimated_time'] == -1 and task_array[i]['progress'] == -1:
                    # print("ちゅうしゅちゅ")
                    # すでにデータベースに入っていたデータで置き換え
                    task_array[i]['estimated_time'] = task_fetch[8]
                    task_array[i]['progress'] = task_fetch[9]

                """else:
                    print("replaced")"""

                # task_arrayの[i]にある変数すべてが置き換えられる
                cur.execute("REPLACE INTO taskdata VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                    task_array[i]['task_id'],
                    dt_dt,
                    task_array[i]['user_id'],
                    task_array[i]['subject_name'],
                    task_array[i]['task_name'],
                    task_array[i]['is_submit'],
                    task_array[i]['can_submit'],
                    task_array[i]['submit_url'],
                    task_array[i]['estimated_time'],
                    task_array[i]['progress'],
                    task_array[i]['remarks']])

        conn.commit()  # データベース更新
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 0  # 返り値が0で処理正常

    except sqlite3.Error as e:  # 例外処理
        print(e)

# C7M2 課題情報問い合わせ所
# 上位の層から来たユーザ名に対応する課題データを返す


def taskdata_ask(user_id_ask):  # user_idが配列になったことから競合を避けるためuser_id→user_id_askとしました。
    conn = sqlite3.connect(dbname)  # データベース接続
    cur = conn.cursor()  # cursorで一件ずつ取得
    cur.execute("SELECT * FROM taskdata WHERE user_id = ?",
                [user_id_ask])  # user_id_askと一致するuser_idの課題データを取得
    result = cur.fetchall()  # SELECT文の結果をすべて取得
    if result == None:  # fetchallでfetchしてきたデータがなければエラー
        # print("error")
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 1, result  # 返り値が0以外は失敗 resultはリスト型
    else:  # 正常
        # print(result)
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 0, result  # 返り値が0で処理正常 resultはリスト型


# 単体テスト

"""# 上位層ではnumpyのdatetime64型で時刻が生成されるため、datetime64型で生成
dt_now = datetime.datetime.now()
date0 = np.datetime64(dt_now.strftime('%Y-%m-%dT%H:%M:%S'))
date1 = np.datetime64(dt_now.strftime('%Y-%m-%dT%H:%M:%S'))
date2 = np.datetime64(dt_now.strftime('%Y-%m-%dT%H:%M:%S'))
task_id = ["task_id1", "task_id3", "task_id4"]
submit_time = [date0, date1, date2]
user_id = ["user_id", "user_id1", "user_id2"]
subject_name = ["subject_nameあ", "subject_name1い", "subject_name2う"]
task_name = ["task_name", "task_name1", "task_name2"]
is_submit = [1, 1, 1]
can_submit = [1, 1, 1]
submit_url = ["https://scomb.shibaura-it.ac.jp/portal/index",
              "https://scomb.shibaura-it.ac.jp/portal/index", "https://scomb.shibaura-it.ac.jp/portal/index"]
estimated_time = [-1, 30, 120]
progless = [-1, 0, 40]
remarks = ["hello,world!", "hello,world!_1", "hello,world!_2"]

user_id_ask = "user_id"

# task_array = np.zeros(0, dtype=task_datatype) #0を要素とする配列をtask_datatypeの型で生成
task_array = [task_id, submit_time, user_id,  subject_name, task_name,
              is_submit, can_submit, submit_url, estimated_time, progless, remarks]
task_array = np.array(task_array)"""

"""# 配列の中に構造体を入れてやり直し
task_array = np.zeros(1, dtype=task_datatype)  # 1を要素とする配列をtask_datatypeの型で生成
dt_now = datetime.datetime.now()
date0 = np.datetime64(dt_now.strftime('%Y-%m-%dT%H:%M:%S'))
task_array["task_id"] = "admin8202101SU003133100132861"
task_array["submit_time"] = date0
task_array["user_id"] = "admin8"
task_array["subject_name"] = "人工知能"
task_array["task_name"] = "課題1"
task_array["is_submit"] = 0
task_array["can_submit"] = 0
task_array["submit_url"] = "https://scomb.shibaura-it.ac.jp/portal/contents/lms/report_submission?idnumber=202101SU0031331001&reportId=32861"
task_array["estimated_time"] = -1
task_array["progress"] = -1
task_array["remarks"] = "hello"

user_id_ask = "admin8"


# taskdata_gate(task_array)  # m1
taskdata_ask(user_id_ask)  # m2"""
