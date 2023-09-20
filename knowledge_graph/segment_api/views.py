from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest
from translate import Translator
import json, re, jieba, time
from opencc import OpenCC

def removeURL(text):
    # 刪除URL網址
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def simplifiedToTraditionalChineseOpenCC(text):
    # 將簡體中文轉成繁體中文
    converter = OpenCC('s2twp')
    return converter.convert(text)

def removeCustomCharactersRE(text):
    # 刪除英文字母與全形英文字母
    text = re.sub('[\u0040-\u007E\uFF20-\uFF60]', r'', text) 
    # 刪除符號與全形符號
    text = re.sub('[\uFF5E\uFF03-\uFF06\uFF08\uFF09\uFF1C-\uFF1E]', r'', text) 
    # 刪除數字與全形數字
    text = re.sub('[\u0030-\u0039\uFF10-\uFF19]', r'', text) 
    # 刪除特定符號
    text = re.sub('[~#$%&()<=>\"]', r'', text)
    return text

def cutSentenceRE(text):
    # 為了中文全形的分句，根據句號驚嘆號問號做換行
    text = re.sub('([.。！？\?])([^’”\"\'])',r'\1\n\2', text) 
    # 為了中文全形的分句，根據全形刪節號做換行
    text = re.sub('(\.{6})([^’”\"\'])',r'\1\n\2', text) 
    # 為了中文半形的分句，根據半形刪節號做換行
    text = re.sub('(\…{2})([^’”\"\'])',r'\1\n\2', text) 

    # 删除 string 字串末尾的指定符號並做分句
    text = text.rstrip()
    return text.split("\n")

@csrf_exempt
def process_text(request:WSGIRequest):
    if request.method == 'POST':
        try:
            start = time.time()
            text = json.loads(request.body)
            # print(text['text'], type(text['text']))

            text = simplifiedToTraditionalChineseOpenCC(text["text"])
            text = removeURL(text)
            text = removeCustomCharactersRE(text)
            text = cutSentenceRE(text)

            data = {"text":{}}
            count_line = 1
            
            for line in text:
                data["text"].update({f"{count_line}": line + "\n"})
                count_line += 1
            
            end = time.time()
            print(data)
            print(f"Time: {round(end - start, 5)}/sec")
            return JsonResponse(data,
                                json_dumps_params={'ensure_ascii':False})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Failed"}, status=400)
    else:
        return JsonResponse({'message': 'Only accpet POST reqiest'}, status=405)