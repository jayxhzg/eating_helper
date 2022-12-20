# 吃貨小幫手
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/icon.png width="200">
</p>

## 前言
吃飯的時候常常很難決定要吃哪間店，因此設計此line bot來幫忙決定，節省思考的時間。
## 環境
* Windows 11
* Python 3.10.7
## 額外套件
* Google Maps API  
用來搜尋並取得google maps上的資料(免費試用有額度限制，用完就沒了QQ)
## 特色
* 會過濾掉目前尚未營業的店家
* 只搜尋使用者選擇地點的周圍店家
* 會顯示店家當天的營業時間及評價
## 使用說明
* 有用到的英文指令大小寫皆可
* **加入好友後，要先輸入`menu`或`主選單`才能進入主選單**
* 在任何一個狀態都能輸入`menu`或`主選單`回到主選單，重新搜尋
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(1).png width="350">
</p>

### 1. 顯示使用說明
* 點選"使用說明"或是輸入`description`後可顯示使用說明，按下"返回主選單"即可回到主選單
<p align="center">  
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(2).png width="300"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(3).png width="300">
</p>

### 2. 選擇餐點
* 點選畫面上的按鈕選擇餐點的種類
* 可不點選按鈕，自行輸入餐點的種類
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(4).png width="350">
</p>

### 3. 輸入位置
* 點選左下角的"+"號，並點選"位置資訊"
* 選擇好地點後，點選"分享"回傳位置資訊
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(5).png width="250"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(6).png width="250"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(7).png width="250">
</p>

### 4. 顯示結果
* 搜尋完成後會將結果(店名)列出(最多顯示20筆資料;搜尋半徑3公里)
* 輸入店家的編號可查看該店家的詳細資料(⭐:評價；🕛:當天的營業時間)
* 點選"吃這間"可在google maps開啟
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(8).png width="300"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(9).png width="300">
</p>

* 若想查看其他店家，直接輸入其他店家的編號
* 點選"返回主選單"可回到主選單
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(10).png width="350">
</p>

### 5. 其他功能
* 若想不到想吃的東西，在主選單點選"可以吃就好"，就可不限定食物的種類搜尋餐廳
* 後續的操作和3、4相同
<p align="center">
    <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(11).png width="250"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(12).png width="250"> <img src=https://github.com/jayxhzg/eating_helper/blob/master/img/description%20(13).png width="250">
</p>

## FSM
![image](https://github.com/jayxhzg/eating_helper/blob/master/img/fsm.png)
state說明:
* menu : 主選單
* description : 顯示使用說明
* select_type : 選擇食物類型
* select_location : 選擇地點(位置資訊)
* show_result : 顯示結果列表
* select_detail : 顯示店家詳細資料