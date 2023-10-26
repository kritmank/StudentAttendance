from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os, json, requests

# Database Import
from student.models import User


# ------ Line Bot ------
# Channel Access Token
access_token = "YOUR_CHANNEL_ACCESS_TOKEN"  # Change this
line_bot_api = LineBotApi(access_token)

# Channel secret
handler = WebhookHandler("YOUR_CHANNEL_SECRET")  # Change this

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        if "HTTP_X_LINE_SIGNATURE" in request.META:
            signature = request.META["HTTP_X_LINE_SIGNATURE"]
        else:
            return HttpResponse(status=400)

        # get request body as text
        body = request.body.decode("utf-8")

        try:
            # handle webhook body
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def reply(event):
    query = event.message.text
    userID = event.source.user_id
    student = User.objects.filter(userID=userID).first()

    if student is None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="You have not registered yet!\nSelect 'Register' on menu 📌"
            ),
        )
    
    elif query == "Profile":
        student = student.student
        dorm = f"{student.dorm_building}-xxx" if student.dorm_room == "None" else f"{student.dorm_building}-{student.dorm_room}"

        headers = {
            "Authorization" : f"Bearer {access_token}",
        }
        req = requests.get(f"https://api.line.me/v2/bot/profile/{userID}", headers=headers)
        profile = req.json()

        # ------ Flex Message ------
        with open(os.path.join("bot_webhook","flex_message","reply_flex.json"), encoding="utf-8") as f:
            flex_dict = json.load(f)

        flex_dict["body"]["contents"][0]["contents"][0]["contents"][0]["url"]   = profile["pictureUrl"]
        flex_dict["body"]["contents"][0]["contents"][1]["contents"][0]["text"]  = profile["displayName"]
        flex_dict["body"]["contents"][0]["contents"][1]["contents"][1]["text"]  = student.studentID
        flex_dict["body"]["contents"][1]["contents"][1]["contents"][1]["text"]  = student.name
        flex_dict["body"]["contents"][1]["contents"][2]["contents"][1]["text"]  = student.class_name
        flex_dict["body"]["contents"][1]["contents"][3]["contents"][1]["text"]  = dorm

        qrcode_url = f"https://checky-pbl1.vercel.app/student/qrcode/{student.studentID}.png"
        flex_dict["body"]["contents"][2]["contents"][0]["contents"][0]["url"]   = qrcode_url
        messages = FlexSendMessage(alt_text="Profile", contents=flex_dict)
        line_bot_api.reply_message(event.reply_token, messages=messages)
        
    else:
        line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(text="Please select\nfunction on menu 📌"))

    return True

def reply_nonMesage(event):
    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(text="Message not supported. 🚫"))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply(event)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    reply_nonMesage(event)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply_nonMesage(event)


@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    reply_nonMesage(event)


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    reply_nonMesage(event)


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    reply_nonMesage(event)
