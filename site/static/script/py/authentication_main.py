# C2 M1 サイト認証主処理 熊谷
import sys
import user_search


def login(user_id, pwd):
    truth, search_id, search_pwd = user_search.search_userdata(user_id, pwd)
    # truth==0で失敗

    # 戻り値 0:エラー, 1:成功
    if truth == 0:
        print("だめぇ")  # 単体テスト
        return 0  # エラー処理
    elif pwd == search_pwd:
        print("おｋ")  # 単体テスト
        return 1  # 成功
    else:
        pass  # その他例外処理(未完成)


def signup(user_id, pwd, mail):
    truth, check_id, check_pwd, check_mail = user_search.check_userdata(
        user_id, pwd, mail)

    if truth == 0:
        return 0  # エラー処理
    else:
        return 1


def authentication_main(user_id, pwd, select, mail):  # 認証,

    if select == 0:  # select==0でログイン
        login(user_id, pwd)
    else:  # select == 1 で新規登録
        signup(user_id, pwd, mail)

        # 戻り値1で成功


# 単体テスト用
args = sys.argv
user_id = args[0]
pwd = args[1]

login(user_id, pwd)
# 単体テストここまで
