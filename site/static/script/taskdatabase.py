#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
taskdatabase.py
V1.4 二次元配列への対応と初期値の条件追加、変数格納順の変更
熊谷 直也
2021.07.01
C7 課題情報管理部 M1&M2 (データベース関連)
M1: 課題をデータベースに格納&更新する。
M2: ユーザ名に対応した課題データを返す。
"""


import sqlite3
import numpy as np
import os  # ファイル存在確認
import datetime
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

        task_array = np.array(task_array)  # numpyの機能を使用するため、念の為ndarray化
        nagasa = task_array.shape[1]  # taskの個数を取得

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
            cur.execute(
                "SELECT * FROM taskdata WHERE task_id=?", [task_array[0, i]])  # SELECT文でデータベースにすでに入ってるタスクと、処理を行うタスクを比較

            task_fetch = cur.fetchone()  # fetchoneでSELECT文の結果を取得(リストになっている)
            # SELECT結果がNoneであればINSERT、重複していたらREPLACE
            if task_fetch == None:
                # task_array[8,i]→estimated_time(課題の推定時間)と、task_array[9,i]→progress(課題の完成度)は値が-1で生成されてしまうので、それぞれ初期値として60、0を代入。
                if task_array[8, i] == -1 and task_array[9, i] == -1:
                    task_array[8, i] = 60
                    task_array[9, i] = 0
                cur.execute("INSERT INTO taskdata VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                    task_array[0, i], task_array[1, i], task_array[2, i], task_array[3, i], task_array[4, i], task_array[5, i], task_array[6, i], task_array[7, i], task_array[8, i], task_array[9, i], task_array[10, i]])
                # print("inserted")
            elif task_array[0, i] == task_fetch[0]:
                # Scombからの抽出時、task_array[8,i]→estimated_time(課題の推定時間)と、task_array[9,i]→progress(課題の完成度)は値が-1であるので、その2つの変数は更新しない
                if task_array[8, i] == -1 and task_array[9, i] == -1:
                    # print("ちゅうしゅちゅ")
                    task_array[8, i] = task_fetch[8]  # すでにデータベースに入っていたデータで置き換え
                    task_array[9, i] = task_fetch[9]
                """
                else:
                    print("replaced")
                """
                # task_arrayの[*,i]にある変数すべてが置き換えられる
                cur.execute("REPLACE INTO taskdata VALUES(?,?,?,?,?,?,?,?,?,?,?)", [
                    task_array[0, i], task_array[1, i], task_array[2, i], task_array[3, i], task_array[4, i], task_array[5, i], task_array[6, i], task_array[7, i], task_array[8, i], task_array[9, i], task_array[10, i]])

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


"""
# 単体テスト
date0 = datetime.datetime.now()
date1 = datetime.datetime.now()
date2 = datetime.datetime.now()
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
task_array = np.array(task_array)

taskdata_gate(task_array)  # m1
# taskdata_ask(user_id_ask)  # m2
"""
