from flask import Flask
app = Flask(__name__)

from flask import request, abort, render_template
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import( MessageEvent, TextMessage, TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction,CarouselTemplate,
    CarouselColumn,ImageCarouselTemplate, ImageCarouselColumn, TemplateSendMessage, MessageTemplateAction,PostbackTemplateAction,ButtonsTemplate,PostbackEvent,URITemplateAction,ImageSendMessage)
from urllib.parse import parse_qsl
line_bot_api = LineBotApi('2qX6Ji2oFEDAnjQbN2BKLCMFngPITjntyfhWRhvkkeWrKytlHP0V64idlFIbLQ426ral6Yw+wVCIpRQKOYr/vcvkfspMiyMuNvF/03tuPR6txyz3yzpSBrVASpvXxBIiq1/ycSr7BlwqPEQP9XZcrgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2121839de708fe6c8a39aebe5ffdb7ae')
liffid = '2006619732-K4km2Me1'

#LIFF靜態頁面
@app.route('/page')
def page():
	return render_template('index.html', liffid = liffid)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    if mtext == '@樂園介紹':
        sendFlex(event)
    elif mtext == '@設施介紹':
        sendImgCarousel(event)
    elif mtext[:3] == '###' and len(mtext) > 3:
         manageForm(event, mtext)
    elif mtext == '@小幫手':
        sendButton(event)

def sendFlex(event):  #彈性配置
    try:
        bubble = BubbleContainer(
            direction='ltr',  #項目由左向右排列
            header=BoxComponent(  #標題
                layout='vertical',
                contents=[
                    TextComponent(text='兒童新樂園', weight='bold', size='xxl'),
                ]
            ),
            hero=ImageComponent(  #主圖片
                url='https://www.taiwan.net.tw/pic.ashx?qp=1/big_scenic_spots/pic_A12-00382.jpg&sizetype=3',
                size='full',
                aspect_ratio='792:555',  #長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  #主要內容
                layout='vertical',
                contents=[
                    
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text='台北市士林區承德路五段55號', color='#666666', size='sm', flex=5)
                                ],
                            ),
                            SeparatorComponent(color='#98fab2'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="星期一休息", color='#666666', size='sm', flex=5)
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="星期二至五 09:00-17:00", color='#666666', size='sm', flex=5)
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="星期六日 09:00-18:00", color='#666666', size='sm', flex=5)
                                ],
                            )
                            
                        ],
                    ),
                    BoxComponent(  
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='電話聯絡', uri='tel:0228333823'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='查看官網', uri="https://www.tcap.taipei/")
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  #底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@amusement park 2024', color='#888888', size='sm', align='center'),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendImgCarousel(event): #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://www-ws.gov.taipei/001/Upload/621/relpic/23906/128248/97efc0a2-11c8-4b84-a6c2-ff46dd09f754.jpg',
                        action=PostbackTemplateAction(
                            label='銀河號',
                            data='action=facility1'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://www-ws.gov.taipei/001/Upload/public/MMO/tcap/12.%E5%B9%B8%E7%A6%8F%E7%A2%B0%E7%A2%B0%E8%BB%8A.JPG',
                        action=PostbackTemplateAction(
                            label='幸福碰碰車',
                            data='action=facility2')
                        ),
                    ImageCarouselColumn(
                        image_url='https://www-ws.gov.taipei/Download.ashx?u=LzAwMS9VcGxvYWQvNjIxL2NrZmlsZS9mZTFjZTZmYS0yYzUzLTQwYzktOGQ2Ny0yYmZiMDliZGU4ZDAuanBn&n=5ZyW54mHMS5qcGc%3d&icon=.jpg',
                        action=PostbackTemplateAction(
                            label='海洋總動員',
                            data='action=facility3'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://www-ws.gov.taipei/001/Upload/public/MMO/tcap/5.%E5%AE%87%E5%AE%99%E8%BF%B4%E6%97%8B.JPG',
                        action=PostbackTemplateAction(
                            label='宇宙迴旋',
                            data='action=facility4'
                            )
                        ),
                    ImageCarouselColumn(
                        image_url='https://www-ws.gov.taipei/001/Upload/621/relpic/23906/128248/fe06b797-299c-4e89-8457-3401482f1382.jpg',
                        action=PostbackTemplateAction(
                            label='摩天輪',
                            data='action=facility5'
                            )
                        )
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名:'+flist[0]+'\n'
        text1 += '日期:' +flist[1]+'\n'
        text1 += '設施:' +flist[2]+'\n'
        text1 += '時段:'+flist[3]
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/YBOfQJ7.png',
                title='小幫手', #主標題
                text='請選擇:',
                actions=[
                    PostbackTemplateAction(#執行Postback功能,觸發Postback事件
                        label='門票價格', #按鈕文字
                        data='action=ticket' #Postback資料
                        ),
                    URITemplateAction( #開啟網頁
                        label='交通資訊',
                        uri='https://www.tcap.taipei/cp.aspx?n=1E39E09B4D64425C'
                        ),
                    PostbackTemplateAction(#執行Postback功能,觸發Postback事件
                        label='最新活動', #按鈕文字
                        data='action=news' #Postback資料
                        ),
                    PostbackTemplateAction(#執行Postback功能,觸發Postback事件
                        label='園區地圖', #按鈕文字
                        data='action=map' #Postback資料
                        )
                    
                    ]
                )
            )
        line_bot_api.reply_message(event.reply_token, message)
    except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
@handler.add(PostbackEvent)
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))
    action = backdata.get('action')

    if action == 'facility1':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="銀河號是環繞園區的單軌列車，行程中可一覽園區美景。")
        )
    elif action == 'facility2':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="幸福碰碰車以繽紛彩繪的跑車為主題，讓小朋友駕駛最酷、最炫的跑車，奔馳與追逐。")
        )
    elif action == 'facility3':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="海洋總動員是以海洋生物為載具造型的音樂馬車，上方有多樣臺灣海域之海洋生物彩繪圖案，以增加小朋友的教育認識。")
        )
    elif action == 'facility4':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="宇宙迴旋是以八大行星繞行太陽旋轉為主題的輻射飛椅，座椅以各行星彩繪為造型，旋轉時之離心力，如置身於銀河中神祕氛圍!")
        )
    elif action == 'facility5':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="摩天輪直徑40公尺並設有27個座艙，為園區主要地標，搭乘時可鳥瞰臺北盆地之美景。")
        )
    elif action == 'ticket':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="票價:\n銀河號:20元\n幸福碰碰車:30元\n海洋總動員:20元\n宇宙迴旋:20元\n摩天輪:30元")
        )
    elif action == 'news':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="【歡慶兒童新樂園10週年】\n兒童新樂園自103年12月16日開幕以來已經邁入10週年囉!從 2024年12月14日到2025年1月1日 特別準備了10週年感恩優惠、假日原住民市集與文化表演、零時差跨年無人機煙火大驚喜，歡迎大家到兒童新樂園一起迎接溫暖的聖誕節和歡樂的跨年夜。")
        )
    elif action == 'map':
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(  #地圖圖片
                        label='園區地圖',
                        original_content_url = "https://i.imgur.com/kDBy39A.png",
                        preview_image_url = "https://i.imgur.com/kDBy39A.png"
                        )
            )
    
    
if __name__ == '__main__':
    app.run(debug=False)


