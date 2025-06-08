from flask import Flask, render_template, jsonify
from collections import OrderedDict
import random

app = Flask(__name__)

# Dictionary of letter pairs and their corresponding Chinese characters
letter_pairs_a = {
    "ab": "盘", "ac": "调", "ad": "告", "ae": "爱因斯坦", "af": "非",
    "ag": "使", "ah": "灰", "ai": "爱", "aj": "汁", "ak": "枪",
    "al": "外", "am": "盾", "an": "妮", "ao": "均", "ap": "猿",
    "aq": "液", "ar": "箭", "as": "屁", "at": "原", "au": "金",
    "av": "片", "aw": "奖", "az": "典"
}

letter_pairs_b = {
    "ba": "爸", "bc": "培", "bd": "床", "be": "蜂", "bf": "牛",
    "bg": "包", "bh": "洗", "bi": "鼻", "bj": "口", "bk": "书",
    "bl": "铃", "bm": "炸", "bn": "豆", "bo": "船", "bp": "闪",
    "bq": "烤", "br": "吧", "bs": "板", "bt": "瓶", "bu": "不",
    "bv": "狸", "bw": "碗", "bz": "忙"
}

letter_pairs_c = {
    "ca": "擦", "cb": "方", "cd": "码", "ce": "厕", "cf": "咖",
    "cg": "笼", "ch": "椅", "ci": "词", "cj": "绩", "ck": "糕",
    "cl": "胞", "cm": "摄", "cn": "厅", "co": "椰", "cp": "杯",
    "cq": "支", "cr": "车", "cs": "案", "ct": "城", "cu": "醋",
    "cv": "洞", "cw": "爬", "cz": "疯"
}

letter_pairs_d = {
    "da": "大", "db": "哑", "dc": "骰", "de": "德", "df": "聋",
    "dg": "狗", "dh": "盘", "di": "帝", "dj": "DJ", "dk": "桌",
    "dl": "钻", "dm": "鼓", "dn": "丹", "do": "干", "dp": "深",
    "dq": "队", "dr": "门", "ds": "盘", "dt": "点", "du": "毒",
    "dv": "魔", "dw": "矮", "dz": "晕"
}

letter_pairs_e = {
    "ea": "鹰", "eb": "肘", "ec": "蚀", "ed": "教", "ee": "灵elf",
    "ef": "蛋", "eg": "地", "eh": "诶", "ei": "射", "ej": "麋",
    "ek": "鳗", "el": "绪", "em": "摁", "en": "响echo", "eo": "茄",
    "ep": "震", "eq": "耳", "er": "yes", "es": "吃", "et": "欧",
    "eu": "布", "ev": "二维", "ew": "简", "ez": "简"
}

letter_pairs_f = {
    "fa": "發", "fb": "脸书", "fc": "脸", "fd": "食", "fe": "铁",
    "ff": "蛙", "fg": "鱼", "fh": "幻", "fi": "飞机", "fj": "叉",
    "fk": "飞", "fl": "泡沫", "fm": "粉", "fn": "弃", "fo": "翻",
    "fp": "搞", "fq": "毛", "fr": "化fossil", "fs": "脚", "ft": "府",
    "fu": "废", "fv": "花", "fw": "狐", "fz": "狐"
}

letter_pairs_g = {
    "ga": "尬", "gb": "赌", "gc": "工程", "gd": "神", "ge": "哥",
    "gf": "票", "gg": "鬼", "gh": "巨", "gi": "漂", "gj": "守",
    "gk": "运/胶", "gl": "game", "gm": "枪", "gn": "围", "go": "缝",
    "gp": "国企", "gq": "草", "gr": "汽", "gs": "羊", "gt": "蛊",
    "gu": "给", "gv": "官网", "gw": "纱gauze"
}

letter_pairs_h = {
    "ha": "哈士奇", "hb": "hub", "hc": "嗝", "hd": "头", "he": "荷",
    "hf": "半", "hg": "抱", "hh": "", "hi": "hi", "hj": "对冲",
    "hk": "钩", "hl": "坡", "hm": "锤", "hn": "蜜", "ho": "吼",
    "hp": "堆", "hq": "总headquarter", "hr": "发", "hs": "马", "ht": "帽",
    "hu": "虎", "hv": "堂heaven", "hw": "业", "hz": "危hazzard"
}

letter_pairs_i = {
    "ia": "ian", "ib": "布洛芬", "ic": "冰", "id": "证", "ie": "网ie",
    "if": "如果", "ig": "点", "ih": "呼", "ii": "", "ij": "注",
    "ik": "知iknow", "il": "病ill", "im": "钢铁侠", "in": "吞", "io": "IO",
    "ip": "IP协", "iq": "智IQ", "ir": "iron铁", "is": "是is", "it": "它it",
    "iu": "IU", "iv": "ivy", "iw": "面interview", "iz": "眼eyes"
}

letter_pairs_j = {
    "ja": "jay", "jb": "jb", "jc": "警察", "jd": "玉", "je": "巨额",
    "jf": "杰jeff", "jg": "jug", "jh": "john", "ji": "鸡", "jj": "",
    "jk": "jack", "jl": "狱jail", "jm": "酱jam", "jn": "进", "jo": "jo",
    "jp": "jeep", "jq": "奸情", "jr": "罐jar", "js": "jesus", "jt": "jet喷",
    "ju": "菊", "jv": "狙", "jw": "颚", "jz": "jax"
}

letter_pairs_k = {
    "ka": "卡", "kb": "键keyboard", "kc": "踢", "kd": "孩", "ke": "🉑",
    "kf": "刀", "kg": "王king", "kh": "Khan", "ki": "凯", "kj": "抠脚",
    "kk": "", "kl": "杀", "km": "kim", "kn": "ken", "ko": "ko",
    "kp": "keep", "kq": "kick", "kr": "韩Korea", "ks": "亲kiss", "kt": "猫kitty",
    "ku": "哭", "kv": "Kelvin", "kw": "kiwi", "kz": "key"
}

letter_pairs_l = {
    "la": "辣", "lb": "室lab", "lc": "蕾", "ld": "领", "le": "lee",
    "lf": "叶", "lg": "腿", "lh": "笑", "li": "力", "lj": "垃圾",
    "lk": "锁", "ll": "", "lm": "檬", "ln": "狮", "lo": "lol",
    "lp": "圈", "lq": "饮", "lr": "狼人", "ls": "松", "lt": "拿铁",
    "lu": "露", "lv": "驴", "lw": "法", "lz": "蜥lizard"
}

letter_pairs_m = {
    "ma": "妈", "mb": "伙mob", "mc": "乐music", "md": "中", "me": "我",
    "mf": "饼muffin", "mg": "芒果", "mh": "meh", "mi": "秘", "mj": "麻将",
    "mk": "猴Monkey", "ml": "信mail", "mm": "", "mn": "钱", "mo": "月",
    "mp": "图map", "mq": "蚊", "mr": "镜", "ms": "鼠", "mt": "山",
    "mu": "目", "mv": "影", "mw": "mew", "mz": "maze"
}

letter_pairs_n = {
    "na": "娜", "nb": "菜", "nc": "脖", "nd": "粉noodle", "ne": "膝",
    "nf": "削nerf", "ng": "黑", "nh": "noah", "ni": "泥", "nj": "忍ninja",
    "nk": "耐nike", "nl": "甲nail", "nm": "名name", "nn": "", "no": "no",
    "np": "憩", "nq": "纳nasdaq", "nr": "北north", "ns": "鼻", "nt": "网",
    "nu": "弩", "nv": "女", "nw": "new", "nz": "纽newYork"
}

letter_pairs_o = {
    "oa": "洲", "ob": "观", "oc": "兽", "od": "奇", "oe": "偶尔",
    "of": "录", "og": "元老", "oh": "喔", "oi": "棒O-", "oj": "🉑ojbk",
    "ok": "橡", "ol": "油", "om": "欧盟", "on": "on", "oo": "",
    "op": "剧", "oq": "占", "or": "或OR", "os": "鸵/系", "ot": "燕麦",
    "ou": "ouch", "ov": "超", "ow": "鹰owl", "oz": "盎司oz"
}

letter_pairs_p = {
    "pa": "耙", "pb": "题", "pc": "pac本", "pd": "pod排期", "pe": "尿pee",
    "pf": "泡芙puff", "pg": "猪", "ph": "phone", "pi": "π", "pj": "鸽",
    "pk": "peek顶", "pl": "池", "pm": "榈", "pn": "笔", "po": "魄",
    "pp": "", "pq": "骗钱", "pr": "柱", "ps": "purse", "pt": "pot池",
    "pu": "谱", "pv": "pave", "pw": "paw", "pz": "pizza"
}

letter_pairs_q = {
    "qa": "QA答", "qb": "qb币", "qc": "奇才", "qd": "四", "qe": "队",
    "qf": "资格", "qg": "切割", "qh": "缺货", "qi": "琪", "qj": "抢劫",
    "qk": "快", "ql": "群里", "qm": "骑马", "qn": "queen", "qo": "商",
    "qp": "quip器", "qq": "", "qr": "亲人", "qs": "确实", "qt": "静",
    "qu": "区", "qv": "颤", "qw": "权威", "qz": "quiz测"
}

letter_pairs_r = {
    "ra": "RA", "rb": "robin", "rc": "米", "rd": "路", "re": "re",
    "rf": "顶", "rg": "reg", "rh": "富", "ri": "日", "rj": "笼",
    "rk": "石", "rl": "真", "rm": "屋", "rn": "雨", "ro": "肉",
    "rp": "绳", "rq": "req", "rr": "", "rs": "rose", "rt": "根",
    "ru": "乳", "rv": "河", "rw": "row行", "rz": "razor刮"
}

letter_pairs_s = {
    "sa": "洒", "sb": "sb傻", "sc": "社", "sd": "种", "se": "看",
    "sf": "三番", "sg": "唱", "sh": "shhh嘘", "si": "死", "sj": "赏金书记",
    "sk": "岩", "sl": "卖", "sm": "sum", "sn": "sin", "so": "so",
    "sp": "汤", "sq": "方", "sr": "星", "ss": "", "st": "坐",
    "su": "苏", "sv": "救", "sw": "saw", "sz": "sex性"
}

letter_pairs_t = {
    "ta": "茶", "tb": "管", "tc": "tic", "td": "ted", "te": "toe",
    "tf": "豆腐", "tg": "tag标", "th": "thigh", "ti": "替", "tj": "团建",
    "tk": "tank坦", "tl": "尾", "tm": "tm提莫", "tn": "teen", "to": "透",
    "tp": "带tape", "tq": "Tequila龙舌兰", "tr": "撕tear", "ts": "tissue",
    "tt": "", "tu": "图", "tv": "tv电视", "tw": "tow拖", "tz": "税"
}

letter_pairs_u = {
    "ua": "underarmour", "ub": "uber", "uc": "uc", "ud": "undo",
    "ue": "UAE", "uf": "ufo", "ug": "ug", "uh": "uhhh", "ui": "ui",
    "uj": "ujump", "uk": "uk", "ul": "unlock", "um": "伞", "un": "un",
    "uo": "uno", "up": "up", "uq": "独unique", "ur": "ur的", "us": "us",
    "ut": "utah", "uv": "universe", "uw": "uw", "uz": "uzi验"
}

letter_pairs_v = {
    "va": "VA", "vb": "颤vibrate", "vc": "疫vaccine", "vd": "video",
    "ve": "veevenus", "vf": "验verify/Vallyfair", "vg": "vegan",
    "vh": "vehicle", "vi": "via", "vj": "veggie", "vk": "viking",
    "vl": "villain", "vm": "vm", "vn": "van", "vo": "vo", "vp": "vp",
    "vq": "vaCCum", "vr": "var", "vs": "vs", "vt": "vet", "vu": "VU管",
    "vw": "vow", "vz": "vizier"
}

letter_pairs_w = {
    "wa": "娃", "wb": "web", "wc": "厕", "wd": "木", "we": "we",
    "wf": "狼", "wg": "wag", "wh": "愿", "wi": "wifi", "wj": "wj",
    "wk": "wok锅", "wl": "墙", "wm": "worm", "wn": "win", "wo": "wow",
    "wp": "whip鞭子", "wq": "武器", "wr": "war", "ws": "was", "wt": "water",
    "wu": "悟", "wv": "wave", "wz": "wizard"
}

letter_pairs_z = {
    "za": "砸", "zb": "僵", "zc": "锌", "zd": "zed", "ze": "泽",
    "zf": "政府", "zg": "zig", "zh": "痣", "zi": "渍", "zj": "宗教",
    "zk": "折扣", "zl": "zelle", "zm": "zoom", "zn": "zen", "zo": "zoo",
    "zp": "zip", "zq": "赚钱", "zr": "zero", "zs": "zeus", "zt": "主题",
    "zu": "族", "zv": "泽vi", "zw": "中文"
}

# Combine all letter pairs
letter_pairs = {}
for d in [letter_pairs_a, letter_pairs_b, letter_pairs_c, letter_pairs_d,
          letter_pairs_e, letter_pairs_f, letter_pairs_g, letter_pairs_h,
          letter_pairs_i, letter_pairs_j, letter_pairs_k, letter_pairs_l,
          letter_pairs_m, letter_pairs_n, letter_pairs_o, letter_pairs_p,
          letter_pairs_q, letter_pairs_r, letter_pairs_s, letter_pairs_t,
          letter_pairs_u, letter_pairs_v, letter_pairs_w, letter_pairs_z]:
    letter_pairs.update(d)

# Create an ordered dictionary, filtering out pairs with same letters
ordered_letter_pairs = OrderedDict(
    sorted(
        [(k, v) for k, v in letter_pairs.items() if k[0] != k[1]],
        key=lambda x: x[0]
    )
)

# Split into groups by ending letter
end_with_a = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('a')])
end_with_b = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('b')])
end_with_c = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('c')])
end_with_d = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('d')])
end_with_e = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('e')])
end_with_f = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('f')])
end_with_g = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('g')])
end_with_h = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('h')])
end_with_i = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('i')])
end_with_j = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('j')])
end_with_k = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('k')])
end_with_l = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('l')])
end_with_m = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('m')])
end_with_n = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('n')])
end_with_o = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('o')])
end_with_p = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('p')])
end_with_q = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('q')])
end_with_r = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('r')])
end_with_s = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('s')])
end_with_t = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('t')])
end_with_u = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('u')])
end_with_v = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('v')])
end_with_w = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('w')])
end_with_z = dict([(k, v) for k, v in ordered_letter_pairs.items() if k.endswith('x') or k.endswith('y') or k.endswith('z')])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_pairs/<mode>')
def get_pairs(mode):
    if mode == "full":
        pairs = list(letter_pairs.items())
    elif mode.startswith("start_"):
        letter = mode.split("_")[1]
        pairs = list(globals()[f"letter_pairs_{letter}"].items())
    elif mode.startswith("end_"):
        letter = mode.split("_")[1]
        pairs = list(globals()[f"end_with_{letter}"].items())
    else:
        pairs = []
    
    random.shuffle(pairs)
    return jsonify(pairs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
