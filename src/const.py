import json

FIVE_SPACE = " "*5

with open("src\\config.json", 'r', encoding="utf-8") as f:
    CONFIG = json.load(f)

with open("src\\npc.json", 'r', encoding="utf-8") as f:
    NPCS = json.load(f)

NPC_DRUNK_WORDS = [
    "今天的心情貌似很不错，一边喝一边笑",
    "貌似有点悲伤，喝醉后一直念叨着听不清的话",
    "拍着桌子嚷嚷“再来一壶！”，酒杯都晃得洒了半杯",
    "抱着酒坛趴在桌上，嘴里嘟囔着“这酒没去年的甜”",
    "拉着旁边人的袖子，碎碎念自己年轻时的威风事",
    "眼神发直盯着空酒杯，突然“啪”地一拍桌：“谁偷喝了我的酒？！”",
    "红着脸哼跑调的小曲，脚还跟着乱晃拍子",
    "捏着酒杯眼泪吧嗒往下掉，嘴里念叨“你怎么就走了啊”",
]
