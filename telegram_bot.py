from re import S
import crawler
import motor
import ReadWebcam
import json
import time
import LED
import detectcolor
from datetime import datetime
from telegram.ext import Updater # 更新者
from telegram.ext import CommandHandler, CallbackQueryHandler # 註冊處理 一般用 回答用
from telegram.ext import MessageHandler, Filters # Filters過濾訊息
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # 互動式按鈕
class telbot:
    def read_token(self):
        try:
            f=open('LSA1101_bot_api.txt','r', encoding="utf-8")
        except:
            print("can't find token file")
        self.token=f.read()
        self.token=self.token.strip()
        print(self.token)
        f.close()
    def __init__(self):
        
        self.colordic={'紅':[255,0,0],
          '綠':[0,255,0],
          '藍':[0,0,255],
          '黃':[255,255,51],
          '灰':[160,160,160],
          '白':[255,255,255],
          '紫':[178,120,160],
          '黑':[0,0,0]
          }
        self.read_token()
        self.water=5
    def startbot(self):
        # 初始化bot
        self.updater = Updater(token=self.token, use_context=False)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('hi', self.hi))
        self.dispatcher.add_handler(CommandHandler('luckycolor', self.luckycolor))
        self.dispatcher.add_handler(CommandHandler('off', self.off))
        self.dispatcher.add_handler(CommandHandler('spray', self.spray))
        self.dispatcher.add_handler(CommandHandler('whatcolor', self.whatcolor))
        self.dispatcher.add_handler(CommandHandler('set_waterpw', self.set_waterpw))
        self.dispatcher.add_handler(CommandHandler('blink', self.blink))
        self.dispatcher.add_handler(CommandHandler('hategreen', self.hategreen))
    def spray(self,bot,update):
        update.message.reply_text(text='吃我噴水水')
        mymotor=motor.motor()
        mymotor.blink(self.water)
    def set_waterpw(self,bot,update): 
        waterpw=update.message
        waterpw=int(waterpw['text'][12:])
        if waterpw:
            update.message.reply_text(text="The waterpower is now set as "+str(waterpw))
    def whatcolor(self,bot,update):
        mycam=ReadWebcam.color()
        out=mycam.run()
        mydetector=detectcolor.detector(out[0],out[1],out[2])
        color=mydetector.test()
        update.message.reply_text(text=color)
    def yourluckyday(self,update,searchcolor):
        mycam=ReadWebcam.color()
        out=mycam.run()
        mydetector=detectcolor.detector(out[0],out[1],out[2])
        color=mydetector.test()
        myled=LED.LED()
        myled.start(5,out[0],out[1],out[2])
        if(color==searchcolor):
            update.message.reply_text(text="你今天很幸運喔")
        else:
            update.message.reply_text(text="今天不是你的幸運日喔")
            #self.spray()
        
    def hi(self,bot, update): # 新增指令/start
        message = update.message
        chat = message['chat']
        update.message.reply_text(text='HI  ' + str(chat['first_name'])+' '+str(chat['last_name']))
    def blink(self,bot,update):
        mycam=ReadWebcam.color()
        out=mycam.run()
        mydetector=detectcolor.detector(out[0],out[1],out[2])
        color=mydetector.test()
        message = update.message
        myled=LED.LED()
        myled.start(5,out[0],out[1],out[2])
        update.message.reply_text(text='亮'+str(color)+'色燈')
    def hategreen(self,bot,update):
        mycam=ReadWebcam.color()
        out=mycam.run()
        mydetector=detectcolor.detector(out[0],out[1],out[2])
        color=mydetector.test()
        self.myled.start(5,out[0],out[1],out[2])
        update.message.reply_text(text="答案是紫色，因為外星人不戴帽子，所以綠色好討厭")
        if(color=='綠'):
            update.message.reply_text(text="就說我討厭綠色了!!!!!!")
           
            self.myled.start(1,0,255,255)
            mymotor=motor.motor()
            mymotor.blink(self.water)
        
    def luckycolor(self,bot,update):
        message=update.message
        starsign=list(message['text'])
        starsign=starsign[12:]
        starsign=''.join(starsign)
        print(starsign)
        if starsign=="":
            update.message.reply_text(text='請在指令後方加入星座')
            return
        mysearch=crawler.Fetch()
        if mysearch.isin(starsign):
            update.message.reply_text(text='稍等一下，正在查詢....')
            with open("data.json", "r") as f:
                data=json.load(f)
            f.close()
            update.message.reply_text(text='今天'+starsign+'的幸運顏色是: '+str(data['starsign'][starsign]))
            mysearch.end()
        else:
            update.message.reply_text(text='沒有'+starsign+'這個星座')
        #self.yourluckyday(str(data['starsign'][starsign]))
        searchcolor=str(data['starsign'][starsign])
        if searchcolor=='橙':
            searchcolor='黃'
        #detectcolor.detector()
        mycam=ReadWebcam.color()
        out=mycam.run()
        mydetector=detectcolor.detector(out[0],out[1],out[2])
        color=mydetector.test()
        
        #self.myled.start(5,out[0],out[1],out[2])
        if(color==searchcolor):
            update.message.reply_text(text="你今天很幸運喔")
        else:
            update.message.reply_text(text="今天不是你的幸運日喔")
            mymotor=motor.motor()
            mymotor.blink(self.water)
           # myled1=LED.LED()
           
            update.message.reply_text(text="這才是你的幸運色，快把濕衣服換掉")
        myled=LED.LED()
        myled.start(5,self.colordic[searchcolor][0],self.colordic[searchcolor][1],self.colordic[searchcolor][2])

    def off(self,bot,update):
        print("turn off")
        self.updater.stop()
if __name__=='__main__':
    mybot=telbot()
    mybot.startbot()
    mybot.updater.start_polling()
    while True:
        text = input()
        # Gracefully stop the event handler
        if text == 'stop':
            mybot.updater.stop()
            break

        # else, put the text into the update queue to be handled by our handlers
        elif len(text) > 0:
            mybot.update_queue.put(text)
