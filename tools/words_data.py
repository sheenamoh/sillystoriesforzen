import json, re, glob
import os; ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from pypinyin import pinyin, Style
L=[("识字一","",
 "蓝天太阳小鸟上学读书写字","天太阳上学"),
("一","一","了花跟我招手一起走到校门口","了一走门口"),
("一","二","得早跳来去在树枝做操朋友跑草地","小鸟早来去"),
("二","一","课识会儿歌故事习长知","书儿习长知"),
("二","二","笔画要好眼心也顺错不","写手心也不"),
("三","一","开爸妈笑着回哥姐全家的声","开回哥姐声"),
("三","二","星那么多这颗中间是三靠样近亲明","妈爸中三亲"),
("四","一","吃晚饭有瓜鱼还蛋桌菜可大都喜欢","饭有瓜鱼喜"),
("四","二","妹搭积木房子机场配说们城市和游乐","妹木校乐"),
("识字二","","双林片森绿羊美肥丽舌甘甜爱蜂蜜","双片羊大舌"),
("五","一","露珠照相张又月亮出红见","又月亮见家"),
("五","二","雨停更山青弯曲河胖啊","雨更山青曲"),
("六","一","个只老虎猫边少群鹅数瞧记牢","个只边多少群"),
("六","二","蚂蚁搬虫动两点重四五六七进洞","虫重四五六七"),
("七","一","睛脚爪腿短牙齿以睡觉","要画牙齿我以"),
("七","二","你就飞园嗅香味才吗采造时流汗水","你飞香才时"),
("八","一","蕉黄像滑梯玩爬下坐快","黄爬下坐机快"),
("八","二","唱里很每从棵响落风听座","唱在里爱从风"),
("识字三","","对睛伤吵闹安静怕空放情","对说闹安空放"),
("九","一","夜悄换黑色衣最把留","夜色衣的蓝森"),
("九","二","用铅发现慢白文图本","用发地白文本"),
("十","一","金沙滩银船工具呀简单板看身后串","金工单是身后"),
("十","二","公轻吹叶飘头带拿剪刀贴纸","公头带起刀子")]
PY={"了":"le","得":"dé","长":"cháng","着":"zhe","还":"hái","都":"dōu","乐":"lè","重":"zhòng","觉":"jué","只":"zhī","发":"fā","的":"de","么":"me","们":"men","子":"zi","吗":"ma","啊":"a","呀":"ya","数":"shǔ","相":"xiàng","更":"gèng","曲":"qū","空":"kōng","场":"chǎng","和":"hé","落":"luò","为":"wèi","几":"jǐ","正":"zhèng","会":"huì","种":"zhǒng","间":"jiān","好":"hǎo","要":"yào","便":"biàn","调":"diào","处":"chù","地":"dì","头":"tóu","看":"kàn","兴":"xìng","睡":"shuì","个":"gè","藏":"cáng","转":"zhuǎn","切":"qiē","中":"zhōng","奇":"qí","尽":"jìn","系":"xì","答":"dá","似":"sì"}
EN={"蓝":"blue","天":"sky, day","太":"too, very","阳":"sun","小":"small","鸟":"bird","上":"up, on","学":"learn, school","读":"read","书":"book","写":"write","字":"character, word",
"了":"(done)","花":"flower","跟":"with, follow","我":"I, me","招":"wave","手":"hand","一":"one","起":"rise, up","走":"walk","到":"arrive, to","校":"school","门":"door","口":"mouth, opening",
"得":"get","早":"early","跳":"jump","来":"come","去":"go","在":"at, in","树":"tree","枝":"branch","做":"do, make","操":"exercise","朋":"friend","友":"friend","跑":"run","草":"grass","地":"ground",
"课":"lesson","识":"know","会":"can","儿":"child, son","歌":"song","故":"story (故事)","事":"thing, matter","习":"practise","长":"long","知":"know",
"笔":"pen, pencil","画":"draw, picture","要":"want","好":"good","眼":"eye","心":"heart","也":"also","顺":"smooth","错":"wrong","不":"not",
"开":"open","爸":"dad","妈":"mum","笑":"laugh, smile","着":"(-ing)","回":"return","哥":"older brother","姐":"older sister","全":"whole","家":"home, family","的":"('s)","声":"sound, voice",
"星":"star","那":"that","么":"(那么/这么)","多":"many","这":"this","颗":"(for stars, beads)","中":"middle","间":"between","是":"is","三":"three","靠":"lean on, near","样":"kind, way","近":"near","亲":"close, kin","明":"bright",
"吃":"eat","晚":"evening, late","饭":"rice, meal","有":"have","瓜":"melon","鱼":"fish","还":"still, also","蛋":"egg","桌":"table","菜":"vegetable, dish","可":"can","大":"big","都":"all","喜":"like, happy","欢":"joyful",
"妹":"younger sister","搭":"build","积":"pile up (积木 blocks)","木":"wood","房":"house","子":"(noun ending)","机":"machine","场":"field, place","配":"match","说":"say","们":"(plural)","城":"city","市":"market, city","和":"and","游":"swim, play","乐":"happy",
"双":"pair","林":"woods","片":"slice, piece","森":"forest","绿":"green","羊":"sheep","美":"beautiful","肥":"fat","丽":"pretty","舌":"tongue","甘":"sweet","甜":"sweet","爱":"love","蜂":"bee","蜜":"honey",
"露":"dew","珠":"pearl, bead","照":"shine, photo","相":"photo (照相)","张":"(for flat things)","又":"again","月":"moon, month","亮":"bright","出":"go out","红":"red","见":"see",
"雨":"rain","停":"stop","更":"even more","山":"mountain","青":"blue-green","弯":"bend","曲":"curved","河":"river","胖":"chubby","啊":"ah!",
"个":"(general measure)","只":"(for animals)","老":"old","虎":"tiger","猫":"cat","边":"side","少":"few","群":"group, flock","鹅":"goose","数":"count","瞧":"look","记":"remember","牢":"firmly",
"蚂":"ant (蚂蚁)","蚁":"ant","搬":"carry, move","虫":"bug","动":"move","两":"two","点":"dot, bit","重":"heavy","四":"four","五":"five","六":"six","七":"seven","进":"enter","洞":"hole",
"睛":"eye (眼睛)","脚":"foot","爪":"claw","腿":"leg","短":"short","牙":"tooth","齿":"tooth","以":"(以后 later)","睡":"sleep","觉":"sleep (睡觉)",
"你":"you","就":"then, just","飞":"fly","园":"garden","嗅":"sniff","香":"fragrant","味":"taste, smell","才":"only then","吗":"(question)","采":"pick","造":"make","时":"time","流":"flow","汗":"sweat","水":"water",
"蕉":"banana (香蕉)","黄":"yellow","像":"like, resemble","滑":"slide, slippery","梯":"ladder (滑梯 slide)","玩":"play","爬":"climb","下":"down","坐":"sit","快":"fast, happy",
"唱":"sing","里":"inside","很":"very","每":"every","从":"from","棵":"(for trees)","响":"loud, ring","落":"fall","风":"wind","听":"listen","座":"seat",
"对":"right, to","伤":"hurt","吵":"noisy","闹":"noisy","安":"calm","静":"quiet","怕":"afraid","空":"sky, empty","放":"put, let go","情":"feeling",
"夜":"night","悄":"quietly","换":"change","黑":"black","色":"colour","衣":"clothes","最":"most","把":"(takes object)","留":"stay, keep",
"用":"use","铅":"lead (铅笔 pencil)","发":"send out","现":"now, appear","慢":"slow","白":"white","文":"writing","图":"picture","本":"book, notebook",
"金":"gold","沙":"sand","滩":"beach","银":"silver","船":"boat","工":"work","具":"tool","呀":"(oh!)","简":"simple","单":"single, simple","板":"board","看":"look","身":"body","后":"behind, after","串":"string of",
"公":"public, male","轻":"light","吹":"blow","叶":"leaf","飘":"float","头":"head","带":"bring, belt","拿":"take, hold","剪":"cut, scissors","刀":"knife","贴":"stick","纸":"paper"}
def py(c): return PY.get(c) or pinyin(c,style=Style.TONE)[0][0]
words={}; order=[]
for unit,lesson,r,w in L:
    tag=unit if not lesson else f"{unit}-{lesson}"
    for c in r+w:
        if c not in words:
            words[c]={"char":c,"pinyin":py(c),"en":EN.get(c,""),"lesson":tag,"read":False,"write":False}; order.append(c)
    for c in r: words[c]["read"]=True
    for c in w: words[c]["write"]=True
missing=[c for c in order if not words[c]["en"]]
print('chars',len(order),'missing meanings',missing)
# coverage from episodes
used={}
for i,p in enumerate(sorted(glob.glob(ROOT+'/ep*/index.html')),1):
    s=open(p).read()
    text=''.join(re.findall(r'data-line="([^"]+)"',s))+''.join(re.findall(r'data-show="([^"]+)"',s))
    ep=re.search(r'ep(\d+)/',p).group(1)
    for c in set(text):
        if c in words: used.setdefault(c,[]).append(int(ep))
for c in order: words[c]["episodes"]=sorted(set(used.get(c,[])))
lessons=[{"unit":u,"lesson":l,"tag":(u if not l else f"{u}-{l}"),"read":list(r),"write":list(w)} for u,l,r,w in L]
data={"source":"华文 一年级 课本 — 认读生字与习写生字表 (Year 1 target: 识字一 to 第十单元)","lessons":lessons,"chars":[words[c] for c in order]}
json.dump(data,open(ROOT+'/data/year1-words.json','w'),ensure_ascii=False,indent=1)
cov=sum(1 for c in order if words[c]["episodes"])
print('covered',cov,'of',len(order))
