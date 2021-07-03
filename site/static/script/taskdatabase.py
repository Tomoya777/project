#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
taskdatabase.py
V1.2 (変数の追加、初期値処理の追加)
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
dbname = "task.db"

# C7M1 課題情報管理部主処理
# 上位の層から上位の層から来た課題データを確認し、変更点をデータベースに格納する。
# 一部データが欠けている際には必要なら書き入れる。


def taskdata_gate(task_array):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        # テーブルがなければテーブル作成(task_arrayにデータがなければ作成されません)
        cur.execute("CREATE TABLE IF NOT EXISTS taskdata(task_id STRING PRIMARY KEY, \
                                     submit_time datetime,\
                                     user_id STRING,\
                                     task_name STRING,\
                                     is_submit INT,\
                                     can_submit INT,\
                                     submit_url STRING,\
                                     estimated_time INT,\
                                     progress INT,\
                                     remarks STRING )")

        # task_array[8]→estimated_time(課題の推定時間)は値が-1で生成されるので、初期値として60を代入。
        if task_array[7] == -1:
            task_array[7] = 60
            # task_array[8]→progress(課題の完成度)は値が-1で生成されるので、初期値として0を代入。
        if task_array[8] == -1:
            task_array[8] = 0

        # 一致するPRIMARY KEY(task_id)が無ければ挿入、重複していたら更新
        cur.execute('INSERT OR REPLACE INTO taskdata VALUES(?,?,?,?,?,?,?,?,?,?)', [
            task_array[0], task_array[1], task_array[2], task_array[3], task_array[4], task_array[5], task_array[6], task_array[7], task_array[8], task_array[9]])
        conn.commit()  # データベース更新
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 0  # 返り値が0で処理正常

    except sqlite3.Error as e:  # 例外処理
        print(e)

# C7M2 課題情報問い合わせ所


def taskdata_ask(user_id):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('SELECT * FROM taskdata WHERE user_id = ?', [user_id])
    result = cur.fetchall()
    if len(result) == 0:  # fetchallでfetchしてきたデータの数が0であればエラー
        print("error")
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 1, result  # 返り値が0以外は失敗
    else:  # 正常
        cur.close()  # カーソルクローズ
        conn.close()  # データベース接続終了
        return 0, result  # 返り値が0で処理正常


"""
# 単体テスト
date = datetime.datetime.now()
task_id = "test2"
submit_time = date
user_id = "testes2"
task_name = "test"
subject_name = "test"
is_submit = "nosubmit"
can_submit_overtime = "cannot"
estimated_time = -1
progless = -1
remarks = "hello,world!"

task_array = np.zeros(0, dtype=task_datatype)
task_array = [task_id, submit_time, user_id, task_name, subject_name,
              is_submit, can_submit_overtime, estimated_time, progless, remarks]


taskdata_gate(task_array)  # m1
# taskdata_ask(user_id)  # m2
"""
