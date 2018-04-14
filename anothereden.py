import os

IntentName = 'AnotherEdenIntent'
IntentCharName = 'AnotherEdenCharIntent'

#####ヘルプを起動する###################
def help_response():
    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "アナザーエデンVCをご利用いただきありがとうございます。"
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "アナザーエデンVCを開いて。と話しかけてください。"
                }
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVCのヘルプを起動しました",
                "type": "Simple"
            },
            'shouldEndSession': False
        }
    }
    return response
    

def launch_response():
########1回目の発話の応答##########
    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "誰のヴァリアブルチャントを知りたいですか"
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVC",
                "type": "Simple"
            },
            "shouldEndSession": False
        }
    }
    return response


def intent_response():
########1回目の発話の応答##########
    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "誰のヴァリアブルチャントを知りたいですか"
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVC",
                "type": "Simple"
            },
            "shouldEndSession": False
        }
    }
    return response

######VCを答える##########
def char_response(char_name,vc_name):
    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": char_name + 'のヴァリアブルチャントは' + vc_name + 'です'
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVC",
                "type": "Simple"
            },
            "shouldEndSession": True
        }
    }
    return response

######存在しないキャラクター##########
def char_error_response(char_name):
    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "存在しないキャラクターです"
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVC",
                "type": "Simple"
            },
            "shouldEndSession": True
        }
    }
    return response

#####cancelとストップはスキルを終了する###################
def cancel_response():

    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "アナザーエデンVCをキャンセルしました。"
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVCをキャンセルしました。",
                "type": "Simple"
            },
            'shouldEndSession': True
        }
    }
    return response

########対応していないインテントはスキルを終了する##########
def cannot_request_response(offset):

    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": "すみません。アナザーエデンVCは対応していません。"
            },
            "card": {
                "title": "アナザーエデンVC",
                "content": "アナザーエデンVC",
                "type": "Simple"
            },
            "shouldEndSession": True
        }
    }
    return response


########何もしない#############
def session_end_response(event):
    print('デバック：' + event['request']['type'] + 'を受信しました')
    print(event['request'])


########LaunchRequestの処理######
def send_launch_response(event, context):
    print('アナザーエデンVCを起動しました')
    return launch_response()

#######IntentRequestの処理#######
def send_intent_response(event, context):
    if event['request']['intent']['name'] == IntentName:
        print('アナザーエデンVCを起動しました')
        return intent_response()
        
    elif event['request']['intent']['name'] == IntentCharName:
        print('キャラクター名を受信しました')
        char_text = open('anaden_char.txt', 'r')
        list_charname = char_text.readlines()
        char_text.close()
        list = []
        char_name = event['request']['intent']['slots']['char']['value']
        char_check = 0
        for line in list_charname:
            ch = line.rstrip('\n')
            list.append(ch)
            if line.find(char_name) >= 0:
                char_check = 1
        
        if char_check == 1:
            vc_dict = dict(zip(list[0::2], list[1::2]))
            vc_name = vc_dict[char_name]
            return char_response(char_name,vc_name)
        else:
            return char_error_response(char_name)
        
    elif event['request']['intent']['name'] == 'AMAZON.HelpIntent':
        print('ヘルプを起動しました。')
        return help_response()
        
    elif event['request']['intent']['name'] == 'AMAZON.CancelIntent':
        print('スキルを停止します')
        return cancel_response()

    elif event['request']['intent']['name'] == 'AMAZON.StopIntent':
        print('スキルを停止します')
        return cancel_response()
        
    else:
        print('対応する必要のないリクエスト')
        offset = event['context']['AudioPlayer']['offsetInMilliseconds']
        return cannot_request_response(offset)

#######SessionEndRequestの処理#######
def send_end_response(event, context):
    print('ユーザからの応答がありませんでした')
    return session_end_response(event)

########mainの処理###########
def lambda_handler(event, context):
    if event['request']['type'] == 'LaunchRequest':
        return send_launch_response(event, context)
    elif event['request']['type'] == 'IntentRequest':
        return send_intent_response(event, context)
    elif event['request']['type'] == 'SessionEndedRequest':
        return send_end_response(event, context)
