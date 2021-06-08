# C6 M1 課題情報管理部主処理に接続し、ユーザIDの登録有無とパスワードを取得する。
# 6/8現在の内部仕様書通りに書きましたが、返す値こんなに必要なかったかもしれないです。
# 別の場所から受け取る値は内部設計書に書かれている順番どおりに受け取っています。
import userdata_gate
import userdata_register


def search_userdata(user_id):  # ログイン用
    truth, user_id, pwd = userdata_gate.user_gate(
        user_id)  # truth==0:失敗 それ以外:成功, C6側の関数名は仮です。
    return truth, user_id, pwd


def check_userdata(user_id, pwd, mail):  # 新規登録用
    truth, user_id, mail, pwd = userdata_register.user_check(
        user_id, mail, pwd)
    return truth, user_id, pwd, mail
