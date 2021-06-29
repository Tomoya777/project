# -*- coding: utf-8 -*-

# C6 M1 顧客情報管理部主処理 熊谷
# C2 M2の層から来たユーザIDをdjangoフレームワークを利用して確認し、登録されてあるパスワードを返す
# import user_search
# 6/22 djangoのフレームワークを使って書き換えてみました
# 参考https://docs.djangoproject.com/ja/3.2/topics/auth/default/
# from django.contrib.auth import authenticate
# django SQL実行 参考 https://docs.djangoproject.com/ja/2.0/topics/db/sql/

import sqlite3
"""
from django.db import connection
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# ベースディレクトリからのパスを通す
BASE_DIR = Path(__file__).resolve().parent.parent
"""

"""
# ログイン時　django.authをつかう
def userdata_gate(user_id, pwd):

    user = authenticate(username=user_id, password=pwd)
    if user is not None:
        # A backend authenticated the credentials(認証成功時)
        print("おけ")
        return 1, user_id, pwd

    else:
        return 0, user_id, pwd

"""

"""
# django.dbをつかう
def userdata_gate(user_id, pwd):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT username FROM auth_user WHERE username = %s", [user_id])
        row = cursor.fetchone()
        print(row)
"""


def userdata_gate(user_id):  # 単独実行

    dbname = '../../../db.sqlite3'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute(
        'SELECT username FROM auth_user WHERE username = ?', user_id)
    if cur.fetchone == None:
        cur.close()
        conn.close()
        return 1  # 入力されたユーザIDが登録されていない場合、エラーとして1を返す

    else:
        cur.close()
        conn.close()
    return 0


"""
# test_kを抽出
user_id = ('admin8',)
print(userdata_gate(user_id))
"""
