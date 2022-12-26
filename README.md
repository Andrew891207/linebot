# Line Fitness

## 構想
一個Linebot的密室逃脫遊戲，遊戲中以2D的方式呈現，透過想像力，創造出一個3D空間的密室，遊戲內容改編自https://t.co/UkHWBXXYQC
，並且優化了遊戲流程，添加成就系統。由於Line聊天紀錄會記錄下來，遊玩中獲得的線索可以輕易查看，獲得良好的遊戲體驗。

## QRcode以及Line id
![](https://i.imgur.com/HD0HHYt.png)

## 環境
- Anaconda
- python Python 3.6.13

## 使用教學
1. install requirements
```shell
pip install -r /path/to/requirements.txt
```
2. 若遇到pygraphviz安裝失敗，則嘗試下面這行
```shell
conda install -c alubbock pygraphviz
```
3. 從`.env.sample`產生出一個`.env`，並填入以下兩個資訊
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN

4. install `ngrok`

```shell
sudo snap install ngrok
```
5. run `ngrok` to deploy Line Chat Bot locally (Webhook URL 後面記得加"/webhook")
```shell
ngrok http 8000
```

6. execute app.py
```shell
python3 app.py
```

## 使用說明
- 基本操作
    - 一開始在Line隨便輸入一段文字即可開始
    - 在房間中，在Line輸入"L"、"R"、"B"，會轉到不同的方向
    - 點選按鈕可查看物品或返回
    - 輸入密碼時，直接在Line輸入密碼即可
    - 在Line輸入"restart"可以重新開始

## 使用示範
### 開始
![](https://i.imgur.com/r818XGN.png)

### 查看物品
![](https://i.imgur.com/4jNpIhd.png)

### 返回
![](https://i.imgur.com/MGgIgrb.png)

### 輸入密碼
![](https://i.imgur.com/nGAs7w0.png)

## FSM
![](https://i.imgur.com/twhvxkX.png)

### state說明
- start: 按下按鈕開始遊戲
- front: 顯示前方的牆壁，按下按鈕查看物品
- left: 顯示左方的牆壁，按下按鈕查看物品
- right: 顯示右方的牆壁，按下按鈕查看物品
- back: 顯示後方的牆壁，按下按鈕查看物品
- front_door: 顯示前方的門，若輸入的密碼正確即破關(去到clearance)，按下"返回"回到front
- front_window: 顯示前方的窗戶，按下"返回"回到front
- left_safe: 顯示左方的保險箱，若輸入的密碼正確即獲得線索，按下"返回"回到left
- left_wall: 顯示左方牆上的方塊，按下"返回"回到left
- right_bag: 顯示右方的黑色書包，若輸入的密碼正確即獲得線索，按下"返回"回到right
- right_box: 顯示右方的橘色箱子，若輸入的密碼正確即獲得線索，按下"返回"回到right
- back_picture: 顯示後方的畫，若輸入的密碼正確即獲得線索，按下"返回"回到back
- back_calendar: 顯示後方的月曆，按下"返回"回到back
- back_book: 顯示後方的書，按下"返回"回到back
- clearance: 顯示成就，按下"重新開始"回到start