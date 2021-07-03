'''
***  File Name: scomblogin.py
***  Version	: V2.0
***  Designer	: 加藤健太
***  Date     : 2021/07/03
***  Purpose  : scombへのログイン、課題抽出
***
***  Revision:
*** V1.0 : 加藤健太, 2021.07.03
'''
import time
import numpy as np
import urllib.parse
from os import times
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import chromedriver_binary
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.http import HttpResponse
from taskdatabase import * 
task_datatype = [
  ("task_id" , "U32"), #課題のid. scormからの読み取り時は"idnumber+固有id"とする.
  ("submit_time", "datetime64[s]"), #提出期限
  ("user_id", "U64"), #ユーザ識別番号
  ("subject_name", "U64"), #表示される科目名
  ("task_name", "U64"), #表示される課題名
  ("is_submit", "int"), #提出されているかどうか(1:提出済み,0:提出されていない)
  ("can_submit", "int"), #提出可能かどうか(1:可能,0:可能でない)
  ("submit_url", "U256"), #提出url
  ("estimated_time", "int"), #課題の推定時間(int). scorm抽出時は-1.
  ("progress", "int"), #課題の完成度. scorm抽出時は-1.
  ("remarks", "U256")] #備考,scorm抽出時はなし

# scombにloginし,ログイン済みのdriverを返す
def Scomblogin (USER, PASSW):
  TIME_OUT = 1.5 #タイムアウト時間

  options = webdriver.ChromeOptions() #optionの取得
  options.add_argument('--disable-extensions')  #拡張機能を無効化
  options.add_experimental_option( "prefs", {'profile.managed_default_content_settings.images': 2}) #軽量化のため画像を読み込ませない
  options.add_experimental_option("excludeSwitches", ["enable-logging"]) #不要なエラーの表示削除
  # options.add_argument('--headless') #ブラウザ画面の非表示

  driver = webdriver.Chrome(options=options) #chromeドライバの起動
  driver.get('https://al19063:sibaura_p00p@scomb.shibaura-it.ac.jp/portal/dologin?initialURI=') #scormへと接続

  # タイムアウト時間を設定
  wait = WebDriverWait(driver, TIME_OUT)
  time.sleep(0.5)

  low_url = driver.current_url #遷移後urlの取得
  login_url =  low_url[:8] +  USER + ":" + PASSW +"@" + low_url[8:] #パスワードを付与したurlを取得
  driver.get(login_url) #ログイン
  try :
    wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@type='submit']"))) #ログインボタンが押せるまで待機
  except TimeoutException:
    return driver , 0
  driver.find_element_by_xpath("//input[@type='submit']").click() #ログインボタンを押す。

  return driver , 1

#ログインしているセッションを引き継ぎ、課題を取り出します。
def Scombkadai (driver,siteuser):
  task_array = np.zeros(0, dtype = task_datatype)
  driver.get("https://scomb.shibaura-it.ac.jp/portal/contents/lms")
 
  # element = driver.find_element_by_xpath = '//*[@id="lmsStudentForm"]/div[1]/table/tbody/tr[1]/td/label[1]'
  html = driver.page_source.encode('utf-8') 
  soup = BeautifulSoup(html, 'lxml')  

  data_td = soup.find_all("td", class_="class", rel="tooltip")
  usedsubjectname = []
  for counter in data_td: #科目ごとに実行する
    data_a = counter.find("a") #"td"タグの中にある"a"タグの要素を抽出
    correntsubjectname = data_a.text #現在処理している科目名

    for tempolalysubjectname in usedsubjectname:
      if tempolalysubjectname == correntsubjectname: #すでにその科目名がチェックされていたならbreak
        break
    else: # 科目名が重複していないことを確認後
      subjectpage_url = (str(data_a))[9:88] #科目ページを取得
      driver.get(subjectpage_url) #科目ページに移行

      html = driver.page_source.encode('utf-8') #ページソースをエンコードした後 
      soup = BeautifulSoup(html, 'lxml') #soupオブジェクトに現在のソースコードを格納

      #課題抽出
      kadai_lowdata = soup.find("div", id ="report") #課題提出の欄を探索
      if kadai_lowdata is not None: #課題が存在すれば
        kadai_lowlist = kadai_lowdata.table.tbody.find_all("tr") #さらに深く探索し、課題を配列で格納する
        for count in kadai_lowlist[1:]: #最初の要素は項目欄のため除外
          task_temp = np.zeros(1, dtype = task_datatype) #今回の課題情報用の構造体を一時的に生成
          submit_url = count.a["href"] #課題の提出場所を保存
          task_temp["submit_url"] = submit_url #構造体に保存
          low_taskid = urllib.parse.parse_qsl(urllib.parse.urlparse(submit_url).query) #urlを分解し,含まれるパラメーターを抽出
          task_temp["task_id"] = siteuser + low_taskid[0][1] + low_taskid[1][1] #得られたパラメーターからidを生成し,保存
          task_temp["submit_time"] = count.find_all("td")[1].text[22:].replace("/","-").replace(" ","T") + ":00" #提出時間を読み取り保存
          task_temp["user_id"] = siteuser #user_idを保存
          task_temp["subject_name"] = correntsubjectname #科目名を保存
          task_temp["task_name"] = count.find("span", class_="instancename").text #課題名を保存
          if count.find_all("td", class_ ="last")[1].span != None: #提出ボタンが存在しなければ
            task_temp["can_submit"] = 1 #提出可能ではない
          if count.find("span", class_ ="unsubmitted") != None: #提出されていないことを確認したら
            task_temp["is_submit"] = 1 #値を代入
          task_temp["estimated_time"] = -1
          task_temp["progress"] = -1
          task_array = np.append(task_array, task_temp, axis=0) #配列の末尾にこのfor文の中で取得した課題を追加
      
      #テスト抽出
      kadai_lowdata = soup.find("div", id ="examination") #課題提出の欄を探索
      if kadai_lowdata is not None: #課題が存在すれば
        kadai_lowlist = kadai_lowdata.table.tbody.find_all("tr") #さらに深く探索し、課題を配列で格納する
        for count in kadai_lowlist[1:]: #最初の要素は項目欄のため除外
          task_temp = np.zeros(1, dtype = task_datatype) #今回の課題情報用の構造体を一時的に生成
          submit_url = count.a["href"] #課題の提出場所を保存
          task_temp["submit_url"] = submit_url #構造体に保存
          low_taskid = urllib.parse.parse_qsl(urllib.parse.urlparse(submit_url).query) #urlを分解し,含まれるパラメーターを抽出
          task_temp["task_id"] = siteuser + low_taskid[2][1] + low_taskid[1][1] #得られたパラメーターからidを生成し,保存
          task_temp["submit_time"] = count.find_all("td")[2].text.replace("/","-").replace(" ","T") + ":00" #提出時間を読み取り保存
          task_temp["user_id"] = siteuser #user_idを保存
          task_temp["subject_name"] = correntsubjectname #科目名を保存
          task_temp["task_name"] = count.find("span", class_="instancename").text #課題名を保存
          if count.find_all("td")[3].span != None: #提出ボタンが存在しなければ
            task_temp["can_submit"] = 1 #提出可能ではない
          if count.find("span", class_ ="unsubmitted") != None: #提出されていないことを確認したら
            task_temp["is_submit"] = 1 #値を代入
          task_temp["estimated_time"] = -1
          task_temp["progress"] = -1
          task_array = np.append(task_array, task_temp, axis=0) #配列の末尾にこのfor文の中で取得した課題を追加
      
      #アンケート抽出
      kadai_lowdata = soup.find("div", id ="questionnaire") #課題提出の欄を探索
      if kadai_lowdata is not None: #課題が存在すれば
        kadai_lowlist = kadai_lowdata.table.tbody.find_all("tr") #さらに深く探索し、課題を配列で格納する
        for count in kadai_lowlist[1:]: #最初の要素は項目欄のため除外
          task_temp = np.zeros(1, dtype = task_datatype) #今回の課題情報用の構造体を一時的に生成
          submit_url = count.a["href"] #課題の提出場所を保存
          task_temp["submit_url"] = submit_url #構造体に保存
          low_taskid = urllib.parse.parse_qsl(urllib.parse.urlparse(submit_url).query) #urlを分解し,含まれるパラメーターを抽出
          task_temp["task_id"] = siteuser + low_taskid[0][1] + low_taskid[3][1] #得られたパラメーターからidを生成し,保存
          task_temp["submit_time"] = count.find_all("td")[2].text.replace("/","-") + "T23:59:59" #提出時間を読み取り保存
          task_temp["user_id"] = siteuser #user_idを保存
          task_temp["subject_name"] = correntsubjectname #科目名を保存
          task_temp["task_name"] = count.find("span", class_="instancename").text #課題名を保存
          if count.find_all("td")[3].span != None: #提出ボタンが存在しなければ
            task_temp["can_submit"] = 1 #提出可能ではない
          if count.find("span", class_ ="unsubmitted") != None: #提出されていないことを確認したら
            task_temp["is_submit"] = 1 #値を代入
          task_temp["estimated_time"] = -1
          task_temp["progress"] = -1
          task_array = np.append(task_array, task_temp, axis=0) #配列の末尾にこのfor文の中で取得した課題を追加
      
      usedsubjectname.append(correntsubjectname) #配列の末尾に今回の科目の名前を追加
  driver.close() #ドライバーを停止 
  return task_array

class ScombLoginView(LoginView):
  def get(self, request, *args, **kwargs):
    context = {}
    return render(request, 'scomblogin.html', context)
    
def ajax(request):
  driver, code = Scomblogin(request.POST.get("scomb_username"),request.POST.get("scomb_password"))
  if (code == 0):
    driver.close() #ドライバーを停止 
    return HttpResponse("error")
  else:
      task_array = Scombkadai(driver, request.POST.get("username"))
      #taskdata_gate(task_array)
  print(task_array)
  return HttpResponse("ok")
