from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re, jieba
from opencc import OpenCC

def importText():
    # text = "从前，有1只蜘蛛，在寺庙的廊庑下静静地结web。由于她经常听到讲经诵法，所以1000年过去了，她变得有些懂得佛理了。有一天，佛从这间寺庙路过，看到了这只有佛缘的蜘蛛，于是问她：“你说，什么是最珍贵的？”蜘蛛想了想说：“是得不到和已失去。”佛笑笑，然后走了。就这样，一千年过去了，蜘蛛一直被香火熏陶着，变得更深沉更知佛法。有一天，佛又路过这个寺庙，于是又问她：“现在你修行加深了，你认为什么是最珍贵的呢？”蜘蛛不假思索地说：“还是得不到和已失去。”佛又微笑着走了。又是一个漫长的一千年，蜘蛛变得更加悟道，她每天都坐在网上深深地思索。在这个千年结束的某一天，一阵大风吹过，一颗露珠落在了蛛网上，蜘蛛看见那晶莹剔透的露珠，心内禁不住欢悦起来，呵，那露珠是多么美好而又纯净，反射着太阳的光华，蜘蛛入迷地看着这滴露珠，充满了爱的欢欣。可是，就在她欣赏愉悦的时候，又是一阵大风吹来，露珠瞬间就被刮走了，消失得无影无踪。"
    # text = "各位友邦的元首與貴賓、各國駐台使節及代表、現場的好朋友，全體國人同胞，大家好感謝與承擔就在剛剛，我和陳建仁已經在總統府裡面，正式宣誓就任中華民國第十四任總統與副總統。我們要感謝這塊土地對我們的栽培，感謝人民對我們的信任，以及，最重要的，感謝這個國家的民主機制，讓我們透過和平的選舉過程，實現第三次政黨輪替，並且克服種種不確定因素，順利渡過長達四個月的交接期，完成政權和平移轉。台灣，再一次用行動告訴世界，作為一群民主人與自由人，我們有堅定的信念，去捍衛民主自由的生活方式。這段旅程，我們每一個人都參與其中。親愛的台灣人民，我們做到了。我要告訴大家，對於一月十六日的選舉結果，我從來沒有其他的解讀方式。人民選擇了新總統、新政府，所期待的就是四個字：解決問題。此時此刻，台灣的處境很困難，迫切需要執政者義無反顧的承擔。這一點，我不會忘記。我也要告訴大家，眼前的種種難關，需要我們誠實面對，需要我們共同承擔。所以，這個演說是一個邀請，我要邀請全體國人同胞一起來，扛起這個國家的未來。國家不會因為領導人而偉大；全體國民的共同奮鬥，才讓這個國家偉大。總統該團結的不只是支持者，總統該團結的是整個國家。團結是為了改變，這是我對這個國家最深切的期待。在這裡，我要誠懇地呼籲，請給這個國家一個機會，讓我們拋下成見，拋下過去的對立，我們一起來完成新時代交給我們的使命。在我們共同奮鬥的過程中，身為總統，我要向全國人民宣示，未來我和新政府，將領導這個國家的改革，展現決心，絕不退縮。"
    # text = "~1231321adsf子説：～勢如弩，箭如發機。"
    # text = "這是一個簡單的句子。『今天真好玩。昨天不知道在幹嘛』。『您好, 世界!』"
    file = open('/home/hal468a/DjangoWorkspace/EnterpriseAI/書籍全文連接版本.txt', 'r', encoding='utf-8')
    text = ''
    for line in file.readlines():
        text += line
    file.close()
    return text

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


def process_text(request):
    text = importText()
    text = simplifiedToTraditionalChineseOpenCC(text)
    text = removeCustomCharactersRE(text)
    text = cutSentenceRE(text)

    data = {}
    count_line = 1
    
    for line in text:
        data.update({f"{count_line}": line + "\n"})
        count_line += 1

    return JsonResponse(data,
                        json_dumps_params={'ensure_ascii':False})