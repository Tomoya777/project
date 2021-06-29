#!/usr/bin/env python
# -*- coding: utf-8 -*-


# C7 課題情報管理部 M1&M2
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
    ("estimated_time", "int"),  # 課題の推定時間(int). scomb抽出時は0.
    ("progress", "int")]  # 課題の完成度. scomb抽出時は0.
dbname = "task.db"

# C7M1 課題情報管理部主処理
# 上位の層から上位の層から来た課題データを確認し、変更点をデータベースに格納する。一部データが欠けている際には必要なら書き入れる。


def taskdata_gate(task_array):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        # テーブルがなければテーブル作成
        cur.execute("CREATE TABLE IF NOT EXISTS taskdata(task_id STRING PRIMARY KEY, \
                                     submit_time datetime,\
                                     user_id STRING,\
                                     task_name STRING,\
                                     is_submit INT,\
                                     can_submit INT,\
                                     submit_url STRING,\
                                     estimated_time INT,\
                                     progress INT)")

        # 一致するPRIMARY KEY(task_id)が無ければ挿入、重複していたら更新
        cur.execute('INSERT OR REPLACE INTO taskdata VALUES(?,?,?,?,?,?,?,?,?)', [
            task_array[0], task_array[1], task_array[2], task_array[3], task_array[4], task_array[5], task_array[6], task_array[7], task_array[8]])
        conn.commit()  # データベース更新
        conn.close()  # データベース接続終了
        return 0  # 返り値が0で処理正常

    except sqlite3.Error as e:  # 例外処理
        print(e)

# C7M2 課題情報問い合わせ所


def taskdata_ask(user_id):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM taskdata WHERE user_id = ?', user_id)
        tmp = cur.fetchall()
        print(tmp)
        conn.commit()  # データベース更新
        conn.close()  # データベース接続終了
        return 0, tmp  # 返り値が0で処理正常
    except sqlite3.Error as e:  # 例外処理
        print(e)


date = datetime.datetime.now()
task_id = "test"
submit_time = date
user_id = "testes"
task_name = "test"
subject_name = "test"
is_submit = "nosubmit"
can_submit_overtime = "cannot"
estimated_time = 1
progless = 0

task_array = np.zeros(0, dtype=task_datatype)
task_array = [task_id, submit_time, user_id, task_name, subject_name,
              is_submit, can_submit_overtime, estimated_time, progless]

# 単体テスト
taskdata_ask(task_array)
