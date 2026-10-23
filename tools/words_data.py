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

# ---------------- Year 2: units 11-22 (same textbook table) ----------------
L2=[("十一","一","同面拉师您助谢握人礼貌气","同面师助点人"),
("十一","二","买汽车问店存钱能算半年十再辆架吧","车存半年十再"),
("十二","一","几海马忙孩千什呢翅膀左右父节","马孩左右父节"),
("十二","二","蛙想捉荷别真没久它运第名","到几别久得名"),
("识字四","","养洁羽毛肚饿找食物饱坏","养羽毛红找物"),
("十三","一","屋娃影灯光比东墙兔西为拍","晚光比东西为"),
("十三","二","她伞怎顶盒遮净","出么着们干净"),
("十四","一","鞋穿耍国成力士","跳和玩成力士"),
("十四","二","清蝴蝶窗前弟喷报应该分童话认","前花弟分看话"),
("十五","一","球摇圆高远生答猜新当脸","球高生朋友脸"),
("十五","二","鹿病角变他窝被打站朵","变很窝朵美丽"),
("十六","一","厕所洗澡电哭肯床外狗指道升","电外狗道升"),
("十六","二","候火钟喊叫踢怪过关","火可笑最关做"),
("识字五","","加包抱宝足赛泡给杯茶奶","包足水食奶叫"),
("十七","一","云住哪追赶方法颜","云什都翅追方"),
("十七","二","兄题因休息等请呼","兄因海顺他呼"),
("十八","一","九八日旗次庆今举共视目表男女舞","九八日今目男女"),
("十八","二","农田稻米果护土","农田米果土共"),
("十九","一","桥便平背各种害让热彩虹","那桥平各害彩"),
("十九","二","排路叔阿姨班直立送","星灯姨立"),
("二十","一","邻伯活奇自己期浇二油尺已眉收割","自己二尺已眉收"),
("二十","二","鼻象耳尾巴猴牛正泥谈鸭办音狮","动鼻象牛正谈音"),
("二十一","一","常爷告诉昨鼠嘴难容易吞","常老爷办易吞耳"),
("二十一","二","尖肉转逃条蛇死咬","问吃肉条两气"),
("二十二","一","鸡啼醒骂午苹擦弄痛折断谁","没午采弄谁巴"),
("二十二","二","百齐皮垃圾破拾丢桶扫院周","百齐皮张等扫周")]
PY2={"几":"jǐ","什":"shén","呢":"ne","吧":"ba","为":"wèi","应":"yīng","该":"gāi","当":"dāng","角":"jiǎo","便":"biàn","背":"bèi","种":"zhǒng",
"巴":"bā","正":"zhèng","难":"nán","转":"zhuǎn","折":"zhé","弄":"nòng","扫":"sǎo","分":"fēn","和":"hé","谁":"shéi","打":"dǎ","给":"gěi","泡":"pào",
"哪":"nǎ","答":"dá","便":"biàn","伯":"bó","尺":"chǐ","奇":"qí","阿":"ā","干":"gān","空":"kōng","过":"guò","好":"hǎo","得":"dé","着":"zhe","么":"me","们":"men","的":"de","都":"dōu","只":"zhī"}
EN2={"同":"same, together","面":"face, side","拉":"pull","师":"teacher","您":"you (polite)","助":"help","谢":"thank","握":"hold, grip","人":"person","礼":"gift, manners","貌":"looks (礼貌 polite)","气":"air, breath",
"买":"buy","汽":"steam (汽车 car)","车":"car, vehicle","问":"ask","店":"shop","存":"save, keep","钱":"money","能":"can, able","算":"count, calculate","半":"half","年":"year","十":"ten","再":"again","辆":"(for vehicles)","架":"shelf, frame","吧":"(let's…)",
"几":"how many, a few","海":"sea","马":"horse","忙":"busy","孩":"child","千":"thousand","什":"what (什么)","呢":"(question word)","翅":"wing","膀":"wing (翅膀)","左":"left","右":"right","父":"father","节":"festival, section",
"蛙":"frog","想":"think, want","捉":"catch","荷":"lotus","别":"don't, other","真":"really, true","没":"not, haven't","久":"long time","它":"it","运":"carry, luck","第":"(ordinal: 第一 first)","名":"name",
"到":"arrive, to","得":"(得 — how well)",
"养":"raise, keep (pets)","洁":"clean","羽":"feather","毛":"fur, hair","肚":"tummy","饿":"hungry","找":"look for","食":"food, eat","物":"thing","饱":"full (after eating)","坏":"bad, broken","红":"red",
"屋":"house, room","娃":"baby, doll","影":"shadow","灯":"lamp, light","光":"light","比":"compare, than","东":"east","墙":"wall","兔":"rabbit","西":"west","为":"for (为什么 why)","拍":"pat, clap",
"晚":"evening, late","她":"she, her","伞":"umbrella","怎":"how (怎么)","顶":"top","盒":"box","遮":"cover, shade","净":"clean","出":"go out","么":"(什么/怎么)","着":"(-ing)","们":"(plural)","干":"dry (干净 clean)",
"鞋":"shoe","穿":"wear, put on","耍":"play (玩耍)","国":"country","成":"become","力":"strength","士":"soldier, person (力士 strongman)","跳":"jump","和":"and","玩":"play",
"清":"clear","蝴":"butterfly (蝴蝶)","蝶":"butterfly","窗":"window","前":"front, before","弟":"younger brother","喷":"spray","报":"report, newspaper","应":"should (应该)","该":"should","分":"divide, minute","童":"child","话":"words, speech","认":"recognise","花":"flower","看":"look",
"球":"ball","摇":"shake","圆":"round","高":"tall, high","远":"far","生":"be born, raw","答":"answer","猜":"guess","新":"new","当":"be, when","脸":"face","朋":"friend","友":"friend",
"鹿":"deer","病":"sick","角":"horn, corner","变":"change","他":"he, him","窝":"nest","被":"quilt, by","打":"hit","站":"stand","朵":"(for flowers, clouds)","很":"very","美":"beautiful","丽":"pretty",
"厕":"toilet","所":"place (厕所 toilet)","洗":"wash","澡":"bath","电":"electricity","哭":"cry","肯":"willing","床":"bed","外":"outside","狗":"dog","指":"finger, point","道":"road, way","升":"rise",
"候":"time (时候)","火":"fire","钟":"clock, bell","喊":"shout","叫":"call","踢":"kick","怪":"strange","过":"pass, cross","关":"close","可":"can","笑":"laugh","最":"most","做":"do, make",
"加":"add","包":"bag, wrap","抱":"hug","宝":"treasure","足":"foot","赛":"race, contest","泡":"bubble, soak","给":"give","杯":"cup","茶":"tea","奶":"milk","水":"water",
"云":"cloud","住":"live","哪":"which, where","追":"chase","赶":"hurry, catch up","方":"square, side","法":"way, method","颜":"colour (颜色)","都":"all",
"兄":"older brother","题":"question, topic","因":"because","休":"rest","息":"rest (休息)","等":"wait","请":"please, invite","呼":"breathe, call","顺":"smooth",
"九":"nine","八":"eight","日":"sun, day","旗":"flag","次":"time (once/twice)","庆":"celebrate","今":"now (今天 today)","举":"raise, lift","共":"together","视":"look (电视 TV)","目":"eye","表":"show, watch","男":"male, boy","女":"female, girl","舞":"dance",
"农":"farming","田":"field","稻":"rice plant","米":"rice","果":"fruit","护":"protect","土":"soil, earth",
"桥":"bridge","便":"convenient","平":"flat","背":"back, carry on back","各":"each","种":"kind, type","害":"harm","让":"let","热":"hot","彩":"colourful","虹":"rainbow","那":"that",
"排":"line up","路":"road","叔":"uncle","阿":"(阿姨 auntie)","姨":"auntie","班":"class","直":"straight","立":"stand","送":"send, give","星":"star",
"邻":"neighbour","伯":"uncle (伯伯)","活":"live, work","奇":"strange","自":"self","己":"self (自己)","期":"period, hope","浇":"water (plants)","二":"two","油":"oil","尺":"ruler","已":"already","眉":"eyebrow","收":"collect","割":"cut",
"鼻":"nose","象":"elephant","耳":"ear","尾":"tail","巴":"(尾巴 tail)","猴":"monkey","牛":"cow","正":"just, upright","泥":"mud","谈":"talk","鸭":"duck","办":"do, handle","音":"sound","狮":"lion","动":"move",
"常":"often","爷":"grandpa","告":"tell","诉":"tell (告诉)","昨":"yesterday (昨天)","鼠":"mouse","嘴":"mouth","难":"hard","容":"hold (容易 easy)","易":"easy","吞":"swallow","老":"old",
"尖":"sharp, pointy","肉":"meat","转":"turn","逃":"escape","条":"(for long things)","蛇":"snake","死":"die","咬":"bite","吃":"eat","两":"two",
"鸡":"chicken","啼":"crow (rooster)","醒":"wake up","骂":"scold","午":"noon","苹":"apple (苹果)","擦":"wipe","弄":"make, fiddle","痛":"hurt, pain","折":"fold, snap","断":"break","谁":"who","采":"pick",
"百":"hundred","齐":"neat, together","皮":"skin","垃":"rubbish (垃圾)","圾":"rubbish","破":"broken","拾":"pick up","丢":"throw away, lose","桶":"bucket, bin","扫":"sweep","院":"yard","周":"week, around","张":"(for flat things)"}
def py2(c): return PY2.get(c) or PY.get(c) or pinyin(c,style=Style.TONE)[0][0]
y1=set(order)
w2={}; order2=[]
for unit,lesson,r,w in L2:
    tag=unit if not lesson else f"{unit}-{lesson}"
    for c in r+w:
        if c not in w2:
            w2[c]={"char":c,"pinyin":(words[c]["pinyin"] if c in words else py2(c)),"en":(words[c]["en"] if c in words else EN2.get(c,"")),
                   "lesson":tag,"read":False,"write":False,"new":c not in y1}
            order2.append(c)
    for c in r: w2[c]["read"]=True
    for c in w: w2[c]["write"]=True
print('year2 chars',len(order2),'new',sum(w2[c]["new"] for c in order2),'missing meanings',[c for c in order2 if not w2[c]["en"]])
used2={}
for p in sorted(glob.glob(ROOT+'/ep*/index.html')):
    s=open(p).read(); text=''.join(re.findall(r'data-line="([^"]+)"',s))+''.join(re.findall(r'data-show="([^"]+)"',s))
    ep=int(re.search(r'ep(\d+)/',p).group(1))
    for c in set(text):
        if c in w2: used2.setdefault(c,[]).append(ep)
for c in order2: w2[c]["episodes"]=sorted(set(used2.get(c,[])))
lessons2=[{"unit":u,"lesson":l,"tag":(u if not l else f"{u}-{l}"),"read":list(r),"write":list(w)} for u,l,r,w in L2]
json.dump({"source":"华文 一年级 课本 — 认读生字与习写生字表 (Year 2: 第十一 to 第二十二单元)","lessons":lessons2,"chars":[w2[c] for c in order2]},
          open(ROOT+'/data/year2-words.json','w'),ensure_ascii=False,indent=1)
nw=[c for c in order2 if w2[c]["new"]]
print('year2 new covered',sum(1 for c in nw if w2[c]["episodes"]),'of',len(nw))
