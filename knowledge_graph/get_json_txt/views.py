from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, re, jieba
from opencc import OpenCC


def simplifiedToTraditionalChineseOpenCC(text):
    converter = OpenCC('s2twp')
    return converter.convert(text)

def chineseQuoteReplaceRE(text):

    textList = list(text)

    flag = 0
    for i in range(len(textList)):
        temp = textList[i]
        if temp == '『':
            if flag == 0 and temp == '『':
                continue
            flag = 1
        elif temp == '』':
            if flag == 1 and temp == '』':
                continue
            flag = 0 
        
        if flag == 0:
            continue
        elif flag == 1:
            if temp == "。":
                textList[i] = u"\uFF0C"

    text = ''.join(textList)
    return text

def removeCustomCharactersRE(text):
    text = re.sub('[\u0040-\u007E\uFF20-\uFF60]', r'', text)
    text = re.sub('~#$%&()<=>`\uFF5E\uFF03-\uFF06\uFF08\uFF09\uFF1C-\uFF1E', r'', text) 
    return text

def stopWord(text):
    # stopwords = {}.fromkeys([ line.rstrip() for line in open('stopWords.txt', encoding='utf8') ])
    stopwords = [word.strip('\n') for word in open('customStopWords.txt', encoding='utf8')]
    # i = 0
    testList = []
    for line in text:
        # if i == 1:
        #     break;
        # print(line)
        segmentation = jieba.cut(line, cut_all=False)
        str = ''
        for s in segmentation:
            if s not in stopwords:
                str += s
        # i += 1
        testList.append(str)
    return testList

def cutSentenceRE(text):
    # for 中文全形
    text = re.sub('([.。！？\?])([^’”\"\'])',r'\1\n\2', text)
    text = re.sub('(\.{6})([^’”\"\'])',r'\1\n\2', text)
    text = re.sub('(\…{2})([^’”\"\'])',r'\1\n\2', text)
    # text = re.sub('([.。！？\?\.{6}\…{2}][’”])([^’”])',r'\1\n\2', text) 
    # text = re.sub('~',r'', text)

    text = text.rstrip()
    return text.split("\n")

@csrf_exempt
def receive_json(request):
    if request.method == 'POST':
        try:
            text = json.loads(request.body)
            # print(text['text'], type(text['text']))

            text = simplifiedToTraditionalChineseOpenCC(text['text'])
            text = removeCustomCharactersRE(text)
            text = cutSentenceRE(text)

            data = {}
            count_line = 1
            
            for line in text:
                data.update({f"{count_line}": line + "\n"})
                count_line += 1

            print(data)
            return JsonResponse(data,
                                json_dumps_params={'ensure_ascii':False})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Failed"}, status=400)
    else:
        return JsonResponse({'message': 'Only accpet POST reqiest'}, status=405)