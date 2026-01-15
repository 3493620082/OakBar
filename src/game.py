import datetime
import json
import random
import time
from pathlib import Path

from pygame import mixer
from colorama import Fore
import os
from src.const import *

class GameFuncs:
    def f_clearScreen(self):
        os.system("cls")

    def f_length(self, text):
        length = 0
        for c in str(text):
            if ord(c) <= 127:
                length += 1
            else:
                length += 2
        return length

    def f_printTitle(self, title=""):
        num = (100 - self.f_length(title)) // 2
        print("\n" + "="*num + title + "="*num + "\n")

    def f_fontColor(self, color=Fore.YELLOW):
        print(color, end="")

    def f_writeConfig(self, config):
        with open("src\\config.json", 'w', encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def f_printFS(self, text=""):
        print(FIVE_SPACE + text)

    def f_printCenter(self, text=""):
        num = (100 - self.f_length(text)) // 2
        print(" "*num + text)

    def f_createSaveFile(self):
        with open("save\\_temp.json", 'r', encoding="utf-8") as f:
            _temp = json.load(f)
        now = datetime.datetime.now()
        file_name = now.strftime("%Y-%m-%d %H-%M-%S")  # 文件名
        with open(f"save\\{file_name}.json", 'w', encoding="utf-8") as f:
            _temp["文件"] = file_name + ".json"
            json.dump(_temp, f, ensure_ascii=False, indent=4)
            return file_name

    def f_readSaveData(self, file_name):
        with open(f"save\\{file_name}.json", 'r', encoding="utf-8") as f:
            return json.load(f)

    def f_sleep(self, sec=2):
        time.sleep(sec)

    def f_chance(self, num):
        """
        根据num设定概率，返回True或False
        :param num: 概率
        :return: True或False
        """
        return random.random() < num / 100

    def f_printStock(self):
        text = "库存: "
        for k, v in getGameData().kucun.items():
            if k[-1] != "酒":
                text += f"{k}{getGameData().kucun[k]} / "
            else:
                text += f"{k}{getGameData().kucun[k]}桶 / "
        text = text[:-3]  # 去掉最后一个"/"符号
        self.f_printCenter(text)

    def f_buyFromMarket(self, limit, name, price, num):
        # 先判断限购数量
        if limit[name] >= num:
            # 再判断余额是否充足
            total_price = num * price
            if getGameData().jinbi >= total_price:
                # 执行购买逻辑
                limit[name] -= num
                getGameData().kucun[name] += num
                getGameData().jinbi -= total_price
                input(f"\n{FIVE_SPACE}{name}x{num}购买成功!")
            else:
                input(f"\n{FIVE_SPACE}余额不足!")
        else:
            input(f"\n{FIVE_SPACE}{name}的剩余数量不够!")

    def f_buyFromSmuggler(self, name, price, num):
        total_price = price * num
        if getGameData().jinbi >= total_price:
            getGameData().jinbi -= total_price
            getGameData().kucun[name] += num
            input(f"\n{FIVE_SPACE}{name}x{num}购买成功!")
        else:
            input(f"\n{FIVE_SPACE}余额不足!")

    def f_getCustomers(self):
        """
        ①0-20：每天刷新1-3个基础级别客人
        ②20-40：每天刷新2-6个客人，级别涵盖基础和低级客人
        ③40-60：每天刷新4-9个客人，级别涵盖基础、低级和中级客人
        ④60-80：每天刷新6-12个客人，级别涵盖基础、低级、中级和高级客人
        ⑤80-100：每天刷新8-15个客人，级别涵盖基础、低级、中级、高级和稀有客人
        :return: 随机抽取的NPC组成的列表
        """
        shengwang = getGameData().shengwang
        # 客人数量和具体客人
        temp = []
        num = 0
        if 0 <= shengwang < 20:
            num = random.randint(1,3)
            temp.extend(NPCS["基础"])
        elif shengwang < 40:
            num = random.randint(2,6)
            temp.extend(NPCS["基础"])
            temp.extend(NPCS["低级"])
        elif shengwang < 60:
            num = random.randint(4,9)
            temp.extend(NPCS["基础"])
            temp.extend(NPCS["低级"])
            temp.extend(NPCS["中级"])
        elif shengwang < 80:
            num = random.randint(6,12)
            temp.extend(NPCS["基础"])
            temp.extend(NPCS["低级"])
            temp.extend(NPCS["中级"])
            temp.extend(NPCS["高级"])
        elif shengwang < 100:
            num = random.randint(8,15)
            temp.extend(NPCS["基础"])
            temp.extend(NPCS["低级"])
            temp.extend(NPCS["中级"])
            temp.extend(NPCS["高级"])
            temp.extend(NPCS["稀有"])
        return random.choices(temp, k=num)

    def f_printLongText(self, text):
        text_list = [text[i:i + 40] for i in range(0, self.f_length(text), 40)]
        for i in text_list:
            self.f_printFS(i)

class GamePage(GameFuncs):
    def page_mainMenu(self):
        while True:
            self.f_clearScreen()
            self.f_printTitle(CONFIG["game_name"])
            self.f_printFS("1. 玩新游戏")
            self.f_printFS("2. 读取存档")
            self.f_printFS("3. 删除存档")
            self.f_printFS("4. 游戏设置")
            self.f_printFS("5. 退出游戏")
            self.f_printTitle("")
            choice = input(f"{FIVE_SPACE}输入选项: ")
            if choice in ["1","2","3","4","5"]:
                if choice == "1":
                    self.page_playNewGame()
                elif choice == "2":
                    self.page_choiceSave()
                elif choice == "3":
                    self.page_deleteSave()
                elif choice == "4":
                    self.page_gameSetting()
                elif choice == "5":
                    input()

    def page_gameSetting(self):
        while True:
            self.f_clearScreen()
            self.f_printTitle("游戏设置")
            self.f_printFS("1. 音乐音量: " + str(CONFIG["music_vol"]))
            # TODO:其他设置项
            self.f_printFS("0. 返回")
            self.f_printTitle()
            choice = input(f"{FIVE_SPACE}输入选项: ")
            if choice == "0":
                break
            elif choice == "1":
                try:
                    vol = int(input(f"{FIVE_SPACE}输入数值: "))
                    if vol > 10: vol = 10
                    elif vol < 0:vol = 0
                    CONFIG["music_vol"] = vol
                    self.f_writeConfig(CONFIG)
                    mixer.music.set_volume(CONFIG["music_vol"] / 10)
                except Exception:
                    print("输入有误!")

    def page_playNewGame(self):
        # 播放动画
        with open("media\\story\\1.txt", 'r', encoding="utf-8") as f:
            for line in list(f):
                self.f_clearScreen()
                self.f_printTitle(CONFIG["game_name"])
                print("\n\n\n")
                self.f_printFS(line.replace("\n", ""))
                print("\n\n\n")
                self.f_printTitle()
                input(f"{FIVE_SPACE}回车继续...")
        self.f_clearScreen()
        # 创建并加载存档
        file_name = self.f_createSaveFile()
        getGameData().init(self.f_readSaveData(file_name))
        self.page_main()

    def page_choiceSave(self):
        while True:
            self.f_clearScreen()
            self.f_printTitle("选择存档")
            files = os.listdir("save\\")
            files.remove("_temp.json")
            # 取出掉列表中所有文件名的.json后缀
            files = list(map(lambda file_name: file_name.replace(".json", ""), files))
            for i in range(len(files)):
                self.f_printFS(f"{i+1}. {files[i]}")
            self.f_printTitle()
            self.f_printFS("0. 返回\n")
            try:
                choice = int(input(f"{FIVE_SPACE}输入选项: "))
                if choice == 0:
                    return
                elif choice in list(range(1, len(files)+1)):
                    file_name = files[choice - 1]
                    # 加载存档数据，然后结束循环，在底部开始游戏
                    getGameData().init(self.f_readSaveData(file_name))
                    break
            except Exception:
                self.f_printFS("选项不存在")
                self.f_sleep()
        # 如果上面选择了返回，函数会直接return，不会来到这里
        # 来到这里说明是选择了存档，所以开始游戏
        self.page_main()

    def page_deleteSave(self):
        while True:
            self.f_clearScreen()
            self.f_printTitle("删除存档")
            files = os.listdir("save\\")
            files.remove("_temp.json")
            # 取出掉列表中所有文件名的.json后缀
            files = list(map(lambda file_name: file_name.replace(".json", ""), files))
            for i in range(len(files)):
                self.f_printFS(f"{i+1}. {files[i]}")
            self.f_printTitle()
            self.f_printFS("0. 返回\n")
            try:
                choice = int(input(f"{FIVE_SPACE}输入选项: "))
                if choice == 0:
                    return
                elif choice in list(range(1, len(files)+1)):
                    confirm = input(f"{FIVE_SPACE}确定要删除存档吗(1是/0否): ")
                    if confirm == "1":
                        f = Path("save\\" + files[choice - 1] + ".json")
                        try:
                            if f.exists() and f.is_file():
                                f.unlink()
                        except Exception:
                            pass
                    break
            except Exception:
                self.f_printFS("选项不存在")
                self.f_sleep()

    def page_main(self):
        self.f_clearScreen()
        self.f_printTitle(CONFIG["game_name"])
        print("\n\n\n")
        self.f_printCenter("按下回车开始游戏")
        print("\n\n\n")
        self.f_printTitle()
        input()
        gameData = getGameData()  # 游戏数据
        while True:
            self.f_clearScreen()
            self.f_printTitle(f" 奥克的酒馆 | {gameData.getSeason()} 第{gameData.tianshu}天 ")
            text = f"当前金币: {gameData.getMoney()}枚 | 酒馆声望: {gameData.shengwang} | 酒馆耐久: {gameData.naijiu}"
            self.f_printCenter(text)
            print()  # 空行
            self.f_printStock()
            print()  # 空行
            self.f_fontColor(Fore.CYAN)
            self.f_printCenter("今日操作")
            print()
            self.f_printFS("1. 酿酒工坊（麦酒/蜜酒/果酒）")
            self.f_printFS("2. 采购原料（市集采购/走私商高价急购）")
            self.f_printFS("3. 开门营业（接待客人，赚取金币+声望）")
            self.f_printFS("4. 修缮酒馆（提升耐久，消耗金币）")
            self.f_printFS("5. 查看账本（销量/利润/债务）")
            self.f_printFS("6. 结束今日")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            self.f_printFS("-1. 保存")
            self.f_printFS("-2. 退出")
            print()
            choice = input(f"{FIVE_SPACE}输入选项: ")
            if choice == "-1":
                gameData.save()
                self.f_printFS("保存完成\n")
                self.f_sleep()
            elif choice == "-2":
                gameData.save()
                break
            elif choice in ["1","2","3","4","5","6"]:
                if choice == "1":
                    self.page_brew()
                elif choice == "2":
                    self.page_buyResource()
                elif choice == "3":
                    self.page_open()
                elif choice == "4":
                    self.page_fixBar()
                elif choice == "5":
                    pass
                elif choice == "6":
                    pass
                # 结束今日->营业结果->随机事件->季节结算->解锁新内容

    # 酿酒工坊界面
    def page_brew(self):
        gameData = getGameData()
        while True:
            self.f_clearScreen()
            self.f_printTitle("奥克的酿酒工坊")
            self.f_printStock()
            print()
            self.f_printCenter("不同酒品需不同原料，成功率受「酿酒技巧」影响")
            print()
            self.f_fontColor(Fore.CYAN)
            self.f_printFS("- 麦酒: 3 麦芽 = 1 桶（成本低，大众款）")
            self.f_printFS("- 蜜酒: 2 蜂蜜 + 1 麦芽 = 1 桶（售价高，受贵族喜欢）")
            self.f_printFS("- 果酒: 2 浆果 + 1 麦芽 = 1 桶（秋季浆果最多）")
            self.f_fontColor(Fore.YELLOW)
            print()
            self.f_printFS(f"酿酒技巧: {gameData.niangjiu}%")
            self.f_printTitle()
            self.f_printFS("选择酿酒类型: 1. 麦酒 2. 蜜酒 3. 果酒")
            self.f_printFS("离开酿造工坊: 0")
            print()
            choice = input(f"{FIVE_SPACE}输入选项: ")
            if choice == "0":
                break
            elif choice in ["1","2","3"]:
                success = self.f_chance(gameData.niangjiu)
                # 判断材料是否够消耗
                kucun = gameData.kucun
                if choice == "1" and kucun["麦芽"] >= 3:
                    gameData.kucun["麦芽"] -= 3
                    if success:
                        gameData.kucun["麦酒"] += 1
                        print(Fore.GREEN)  # 空行
                        self.f_printFS("酿酒成功！消耗 3 麦芽，麦酒 + 1 桶")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")
                    else:
                        print(Fore.RED)
                        self.f_printFS("酿酒失败！损耗 3 麦芽")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")
                elif choice == "2" and kucun["蜂蜜"] >= 2 and kucun["麦芽"] >= 1:
                    gameData.kucun["蜂蜜"] -= 2
                    gameData.kucun["麦芽"] -= 1
                    if success:
                        gameData.kucun["蜜酒"] += 1
                        print(Fore.GREEN)
                        self.f_printFS("酿酒成功！消耗 2 蜂蜜 1 麦芽，蜜酒 + 1 桶")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")
                    else:
                        print(Fore.RED)
                        self.f_printFS("酿酒失败！损耗 2 蜂蜜 1 麦芽")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")
                elif choice == "3" and kucun["浆果"] >= 2 and kucun["麦芽"] >= 1:
                    gameData.kucun["浆果"] -= 2
                    gameData.kucun["麦芽"] -= 1
                    if success:
                        gameData.kucun["果酒"] += 1
                        print(Fore.GREEN)
                        self.f_printFS("酿酒成功！消耗 2 浆果 1 麦芽，果酒 + 1 桶")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")
                    else:
                        print(Fore.RED)
                        self.f_printFS("酿酒失败！损耗 2 浆果 1 麦芽")
                        print(Fore.YELLOW)
                        input(f"{FIVE_SPACE}回车继续...")

    # 采购原料界面
    def page_buyResource(self):
        gameData = getGameData()
        # 每天的原料购买上限
        limit = {
            "麦芽": 25,
            "蜂蜜": 15,
            "浆果": 20,
            "木材": 20
        }
        while True:
            self.f_clearScreen()
            self.f_printTitle("采购原料")
            self.f_printCenter(f"当前金币: {gameData.getMoney()}枚")
            print()
            self.f_printStock()
            print()
            self.f_printCenter("集市采购价格稳定，但每天原料数量有限")
            self.f_printCenter("走私商人价格约贵50%，但是数量不限")
            print()
            text = "限购: "
            for k, v in limit.items():
                text += f"{k}{v}份 / "
            self.f_printCenter(text[:-3])
            print()
            self.f_fontColor(Fore.CYAN)
            self.f_printFS("- 市集采购（1.麦芽=0.2金币 2.蜂蜜=0.33金币 3.浆果=0.50金币 4.木材=0.25金币）")
            self.f_printFS("- 走私商人（5.麦芽=0.3金币 6.蜂蜜=0.50金币 7.浆果=0.75金币 8.木材=0.35金币）")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            self.f_printFS("离开采购集市: 0")
            print()
            try:
                choice = int(input(f"{FIVE_SPACE}输入选项: "))
                if choice == 0:
                    break
                elif choice in [1,2,3,4]:  # 集市交易
                    num = int(input(f"{FIVE_SPACE}输入数量: "))
                    if choice == 1:  # 集市麦芽
                        self.f_buyFromMarket(limit, "麦芽", 0.2, num)
                    elif choice == 2:  # 集市蜂蜜
                        self.f_buyFromMarket(limit, "蜂蜜", 0.33, num)
                    elif choice == 3:  # 集市浆果
                        self.f_buyFromMarket(limit, "浆果", 0.50, num)
                    elif choice == 4:  # 集市木材
                        self.f_buyFromMarket(limit, "木材", 0.25, num)
                elif choice in [5,6,7,8]:  # 走私商交易
                    num = int(input(f"{FIVE_SPACE}输入数量: "))
                    if choice == 5:  # 走私麦芽
                        self.f_buyFromSmuggler("麦芽", 0.3, num)
                    elif choice == 6:  # 走私蜂蜜
                        self.f_buyFromSmuggler("蜂蜜", 0.5, num)
                    elif choice == 7:  # 走私浆果
                        self.f_buyFromSmuggler("浆果", 0.75, num)
                    elif choice == 8:  # 走私木材
                        self.f_buyFromSmuggler("木材", 0.35, num)
            except Exception:
                self.f_printFS("输入有误!")
                self.f_sleep()

    # 开门营业界面
    def page_open(self):
        gameData = getGameData()
        customers = self.f_getCustomers()  # 因为每日只需要获取一次客人数量，所以放在循环外部
        while True:
            self.f_clearScreen()
            self.f_printTitle("奥克的酒馆营业中")
            # 酒馆信息
            text = f"当前金币: {gameData.getMoney()}枚 | 酒馆声望: {gameData.shengwang} | 酒馆耐久: {gameData.naijiu}"
            self.f_printCenter(text)
            print()
            # 库存
            self.f_printStock()
            print()
            # 提示
            self.f_printCenter("客流量和消费额受声望、酒馆耐久影响。单位：1杯=0.25桶")
            print()
            # 客人
            self.f_fontColor(Fore.CYAN)
            self.f_printCenter(f"今日客人数量: {len(customers)}")
            print()
            # 当前客人
            cst = customers[0]
            cst_need = {"数量": random.choice(cst["需求数量"]), "酒类": random.choice(cst["需求酒类"]), "消费": 0}
            cst_need["消费"] = gameData.shoujia[cst_need["酒类"]] * cst_need["数量"]
            text = f'- {cst["名字"]}: 需要 {cst_need["数量"]} 杯 {cst_need["酒类"]}'
            self.f_printFS(text)
            text = f'- 消费: {cst_need["消费"]} 金币'
            self.f_printFS(text)
            print()
            self.f_printFS("-"*42 + " 操作 " + "-"*42)
            print()
            text = f'1.接待（增加声望，增加收入） 2.赶走（降低声望，有几率闹事） 3.结束营业'
            self.f_printCenter(text)
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            # 选项
            choice = input(f"{FIVE_SPACE}输入选项: ")
            print()
            if choice == "1":  # 接待
                # 酒水充足，达成交易
                if gameData.kucun[cst_need["酒类"]] >= cst_need["数量"] * 0.25:
                    gameData.kucun[cst_need["酒类"]] -= cst_need["数量"] * 0.25  # 减少库存
                    gameData.jinbi += cst_need["消费"]  # 增加金币
                    # 将该客人从客人列表中移出
                    del customers[0]
                    # 触发客人对话
                    text = cst["名字"] + random.choice(NPC_DRUNK_WORDS)
                    if self.f_length(text) >= 90:
                        self.f_printLongText(text)
                    else:
                        self.f_printFS(text)
                    input(f'{FIVE_SPACE}接待完成， +{cst_need["消费"]}金币')
                # 酒水不足，交易失败
                else:
                    self.f_printFS("酒水不足，无法完成接待\n")
                    if self.f_chance(10):  # 10%的概率客人生气闹事
                        text = f'{cst["名字"]} 因为没喝到酒非常生气，掀翻了酒馆好几个桌子，虽然你及时制止了他，但还是损失了一些物品'
                        if self.f_length(text) >= 90:  # 如果文本太长处理一下
                            self.f_printLongText(text)
                        else:
                            self.f_printFS(text)
                        input(f"{FIVE_SPACE}酒馆耐久 -2")
                    else:  # 客人没有生气，离开酒馆
                        input(f'{FIVE_SPACE}{cst["名字"]} 有些失望，摇摇头离开了酒馆')
            elif choice == "2":  # 赶走，必掉声望，50%几率闹事
                pass
            elif choice == "3":
                confirm = input(f"\n{FIVE_SPACE}确定要结束今日营业吗(1是/0否): ")
                if confirm == "1":
                    input(f"\n{FIVE_SPACE}已结束今日营业")
                    break

    # 修缮酒馆界面
    def page_fixBar(self):
        pass
    # TODO:修缮酒馆

class GameData:
    def init(self, data):
        self.file_name = data["文件"]
        self.jinbi = data["金币"]
        self.shengwang = data["声望"]
        self.naijiu = data["耐久"]
        self.tianshu = data["天数"]
        self.jijie = data["季节"]
        self.zhaiwu = data["债务"]
        self.niangjiu = data["酿酒"]
        self.kucun = data["库存"]
        self.shoujia = data["售价"]

    def save(self):
        with open(f"save\\{self.file_name}", 'w', encoding="utf-8") as f:
            data = {
                "文件": self.file_name,
                "金币": self.jinbi,
                "声望": self.shengwang,
                "耐久": self.naijiu,
                "天数": self.tianshu,
                "季节": self.jijie,
                "债务": self.zhaiwu,
                "酿酒": self.niangjiu,
                "库存": self.kucun,
                "售价": self.shoujia
            }
            json.dump(data, f, ensure_ascii=False, indent=4)

    def getSeason(self):
        if self.jijie == 1:return "春季"
        elif self.jijie == 2:return "夏季"
        elif self.jijie == 3:return "秋季"
        elif self.jijie == 4:return "冬季"
        return None

    def getMoney(self):
        if float(self.jinbi).is_integer():  # 如果当前金币值是整数则使用int转换一下然后返回
            return int(self.jinbi)
        else:
            return self.jinbi

_gameData = GameData()
def getGameData():
    return _gameData
