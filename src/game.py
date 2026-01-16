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
                getGameData().today["收入"] -= total_price
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
            getGameData().today["收入"] -= total_price
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
        """
        判断文本长度，如果超过长度则换行打印
        如果不超长则正常打印
        :param text: 文本字符串
        :return: 无
        """
        if self.f_length(text) >= 90:  # 如果文本太长处理一下
            text_list = [text[i:i + 40] for i in range(0, self.f_length(text), 40)]
            for i in text_list:
                self.f_printFS(i)
        else:
            self.f_printFS(text)

    def f_addShengWang(self, shengwang):
        getGameData().shengwang = round(getGameData().shengwang + shengwang, 2)
        if getGameData().shengwang > 100:
            getGameData().shengwang = 100

    def f_decShengWang(self, shengwang):
        getGameData().shengwang = round(getGameData().shengwang - shengwang, 2)
        if getGameData().shengwang < 0:
            getGameData().shengwang = 0

    def f_addNaijiu(self, naijiu):
        getGameData().naijiu += naijiu
        if getGameData().naijiu > 100:
            getGameData().naijiu = 100

    def f_decNaijiu(self, naijiu):
        getGameData().naijiu -= naijiu
        if getGameData().naijiu < 0:
            getGameData().naijiu = 0

    def f_confirm(self, text, yes_text):
        confirm = input(f"{FIVE_SPACE}{text}(1是/0否): ")
        if confirm == "1":
            input(f"\n{FIVE_SPACE}{yes_text}")
            return True
        return False

    def f_printCaozuo(self):
        self.f_printFS("—" * 21 + " 操作 " + "—" * 21)
        print()

    def f_centerSpace(self, width, text):
        """
        输入要居中的宽度和文本，计算并返回所需的空格字符串
        :param width: 总宽度
        :param text: 文本
        :return: 所需的空格字符串
        """
        return " "*((width - self.f_length(text)) // 2)

    def f_finishToday(self):
        """
        结束今日
        :return: 无
        """
        # 1、判断是否需要还债
        if getGameData().zhaiwu != 0:
            # 本天是不是月末
            if self.f_isLastDayOfMonth(getGameData().tianshu):
                self.f_clearScreen()
                self.f_printTitle(CONFIG["game_name"])
                print("\n\n\n")
                if getGameData().jinbi >= 10:
                    getGameData().jinbi -= 10
                    getGameData().zhaiwu -= 10
                    getGameData().zhangben["债务"] -= 10
                    getGameData().today["收入"] -= 10
                    self.f_printCenter(f"今天是月末，自动还债10金币，剩余金币{getGameData().jinbi}")
                else:
                    getGameData().naijiu -= 20
                    getGameData().today["耐久"] -= 20
                    self.f_printCenter(f"今天是月末，你的钱不足以还款，酒馆被打砸一通，耐久-20")
                print("\n\n\n")
                self.f_printTitle()
                input(f"{FIVE_SPACE}按下回车继续...")
        # 2、天数+1
        getGameData().tianshu += 1
        # 1、保存游戏数据
        getGameData().save()

    def f_isLastDayOfMonth(self, day: int) -> bool:
            """
            [豆包AI生成]
            判断给定天数是否为当月最后一天（按平年规则，不考虑闰年）
            规则：一三五七八十腊（1、3、5、7、8、10、12月）31天，
                  四六九冬（4、6、9、11月）30天，2月28天
            支持天数大于365天（自动循环计算对应年份的天数）
            :param day: 天数
            :return: True或False
            """
            # 平年各月天数（索引0占位，对应1-12月）
            month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            # 处理天数大于365的情况（循环计算）
            total_days_in_year = 365
            normalized_day = (day - 1) % total_days_in_year + 1  # 确保结果在1-365之间
            # 计算当前天数对应的月份
            current_sum = 0
            target_month = 0
            for month in range(1, 13):
                current_sum += month_days[month]
                if normalized_day <= current_sum:
                    target_month = month
                    break
            # 判断是否为当前月份的最后一天
            last_day_of_month = month_days[target_month]
            # 计算当前月份的第一天（总天数累加值 - 当月天数 + 1）
            first_day_of_month = current_sum - last_day_of_month + 1
            # 计算当前天数在当月的日期
            day_in_month = normalized_day - first_day_of_month + 1
            return day_in_month == last_day_of_month

    def f_addNiangJiu(self, num):
        getGameData().niangjiu += num
        if getGameData().niangjiu >= 100:
            getGameData().niangjiu = 100

    def f_setSoundVolume(self):
        for k in SOUNDS.keys():
            SOUNDS[k].set_volume(CONFIG["sound_vol"] / 10)

    def f_addSound(self, name, file_name):
        file_path = "media\\sound\\"
        SOUNDS[name] = mixer.Sound(file_path + file_name)

    def f_initSounds(self):
        # 这里添加所有的音效
        self.f_addSound("翻页", "翻页.ogg")
        self.f_addSound("酿酒工坊", "酿酒工坊.ogg")
        self.f_addSound("采购原料", "采购原料.ogg")
        self.f_addSound("开门营业", "开门营业.ogg")
        self.f_addSound("修缮酒馆", "修缮酒馆.ogg")
        # 设置音效音量
        self.f_setSoundVolume()

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
                    SOUNDS["翻页"].play()
                    self.page_playNewGame()
                elif choice == "2":
                    SOUNDS["翻页"].play()
                    self.page_choiceSave()
                elif choice == "3":
                    SOUNDS["翻页"].play()
                    self.page_deleteSave()
                elif choice == "4":
                    SOUNDS["翻页"].play()
                    self.page_gameSetting()
                elif choice == "5":
                    break

    def page_gameSetting(self):
        while True:
            self.f_clearScreen()
            self.f_printTitle("游戏设置")
            self.f_printFS("1. 音乐音量: " + str(CONFIG["music_vol"]))
            self.f_printFS("2. 音效音量: " + str(CONFIG["sound_vol"]))
            print()
            self.f_printFS("0. 返回")
            self.f_printFS("-  Ctrl+鼠标滚轮放大界面")
            self.f_printFS("-  游戏界面宽度不齐请将窗口字体改为新宋体：右键窗口标题栏-属性-字体")
            self.f_printTitle()
            try:
                choice = input(f"{FIVE_SPACE}输入选项: ")
                if choice == "0":
                    break
                elif choice == "1":
                    vol = int(input(f"{FIVE_SPACE}输入数值: "))
                    if vol > 10: vol = 10
                    elif vol < 0:vol = 0
                    CONFIG["music_vol"] = vol
                    self.f_writeConfig(CONFIG)
                    mixer.music.set_volume(CONFIG["music_vol"] / 10)
                elif choice == "2":
                    vol = int(input(f'{FIVE_SPACE}输入数值: '))
                    if vol > 10: vol = 10
                    elif vol < 0:vol = 0
                    CONFIG["sound_vol"] = vol
                    self.f_writeConfig(CONFIG)
                    self.f_setSoundVolume()
            except Exception:
                print("输入有误!")

    def page_playNewGame(self):
        # 播放动画
        with open("media\\story\\1.txt", 'r', encoding="utf-8") as f:
            for line in list(f):
                SOUNDS["翻页"].play()
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
                self.f_printFS(f"{i+1}. {files[i]} 第{self.f_readSaveData(files[i])['天数']}天")
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
                self.f_printFS(f"{i+1}. {files[i]} 第{self.f_readSaveData(files[i])['天数']}天")
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
        # 第几天界面
        self.page_tianshu()
        while True:
            # 主界面内容
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
                SOUNDS["翻页"].play()
                if choice == "1":
                    self.page_brew()
                elif choice == "2":
                    self.page_buyResource()
                elif choice == "3":
                    self.page_open()
                elif choice == "4":
                    self.page_fixBar()
                elif choice == "5":  # 账本
                    self.page_ledger()
                # 结束今日->营业结果->随机事件
                # 酿酒、采购、营业、修缮和结束今日 这5个选项都会触发结算函数
                if choice in ["1","2","3","4","6"]:
                    # 今日已完成界面
                    self.page_wancheng()
                    # 结算数据
                    self.f_finishToday()
                    # 显示营业结果
                    self.page_todayResult()
                    # 随机事件
                    self.page_randomEvent()
                    # 今日结束语界面
                    self.page_endToday()
                    # 第几天界面
                    self.page_tianshu()

    # 酿酒工坊界面
    def page_brew(self):
        gameData = getGameData()
        # 声望-1
        gameData.shengwang -= 1
        # 今日声望-1
        gameData.today["声望"] -= 1
        # 开始播放音效
        SOUNDS["酿酒工坊"].play(-1)
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
            print()
            self.f_printFS(f"酿酒技巧: {gameData.niangjiu}%\n")
            self.f_printCaozuo()
            self.f_printCenter("选择酿酒类型: 1.麦酒 2.蜜酒 3.果酒")
            self.f_printCenter("离开酿造工坊: 0")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            print()
            choice = input(f"{FIVE_SPACE}输入选项: ")
            if choice == "0":
                break
            elif choice in ["1","2","3"]:
                success = self.f_chance(gameData.niangjiu)
                # 材料
                kucun = gameData.kucun
                if choice == "1":
                    # 材料足够
                    if kucun["麦芽"] >= 3:
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
                    # 材料不够
                    else:
                        input(f'{FIVE_SPACE}麦酒 酿酒材料不足!')
                elif choice == "2":
                    if kucun["蜂蜜"] >= 2 and kucun["麦芽"] >= 1:
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
                    else:
                        input(f'{FIVE_SPACE}蜜酒 酿酒材料不足!')
                elif choice == "3":
                    if kucun["浆果"] >= 2 and kucun["麦芽"] >= 1:
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
                    else:
                        input(f'{FIVE_SPACE}果酒 酿酒材料不足!')
        # 关闭音效
        SOUNDS["酿酒工坊"].stop()

    # 采购原料界面
    def page_buyResource(self):
        gameData = getGameData()
        # 声望-1
        gameData.shengwang -= 1
        # 今日声望-1
        gameData.today["声望"] -= 1
        # 每天的原料购买上限
        limit = {
            "麦芽": 25,
            "蜂蜜": 15,
            "浆果": 20,
            "木材": 20
        }
        SOUNDS["采购原料"].play(-1)
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
            print()
            self.f_printCaozuo()
            self.f_printCenter("离开采购集市: 0")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
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
        SOUNDS["采购原料"].stop()

    # 开门营业界面
    def page_open(self):
        gameData = getGameData()
        customers = self.f_getCustomers()  # 因为每日只需要获取一次客人数量，所以放在循环外部
        SOUNDS["开门营业"].play(-1)
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
            # 有客人
            if len(customers) != 0:  # 排队客人不小于0个
                cst = customers[0]
                cst_need = {"数量": random.choice(cst["需求数量"]), "酒类": random.choice(cst["需求酒类"]), "消费": 0}
                cst_need["消费"] = round(gameData.shoujia[cst_need["酒类"]] * cst_need["数量"], 2)
                text = f'- {cst["名字"]}: 需要 {cst_need["数量"]} 杯 {cst_need["酒类"]}'
                self.f_printFS(text)
                text = f'- 消费: {cst_need["消费"]} 金币'
                self.f_printFS(text)
                print()
                self.f_printCaozuo()
                text = f'1.接待（增加声望，增加收入） 2.赶走（降低声望，有几率闹事） 3.结束营业'
                self.f_printCenter(text)
            # 没有客人
            else:
                self.f_printCaozuo()
                text = f'3.结束营业'
                self.f_printCenter(text)
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            # 选项
            choice = input(f"{FIVE_SPACE}输入选项: ")
            print()
            # 有客人才能处理1和2选项
            if len(customers) != 0:
                # 接待
                if choice == "1":
                    # 酒水充足，达成交易
                    if round(gameData.kucun[cst_need["酒类"]], 2) >= round(cst_need["数量"] * 0.25, 2):
                        # 减少库存
                        gameData.kucun[cst_need["酒类"]] = round(gameData.kucun[cst_need["酒类"]] - cst_need["数量"] * 0.25, 2)
                        # 在账本增添酒类销量
                        gameData.zhangben["销量"][cst_need["酒类"]] = round(gameData.zhangben["销量"][cst_need["酒类"]] + cst_need["数量"] * 0.25, 2)
                        # 增加金币
                        gameData.jinbi = round(gameData.jinbi + cst_need["消费"], 2)
                        # 在账本增添利润
                        gameData.zhangben["利润"] = round(gameData.zhangben["利润"] + cst_need["消费"], 2)
                        # 增加声望
                        self.f_addShengWang(cst["声望增加"])
                        # 小费
                        isTip = self.f_chance(cst["小费"]["概率"])
                        tip = 0
                        if isTip:
                            tip += random.randint(cst["小费"]["金额"]["min"], cst["小费"]["金额"]["max"])
                            gameData.jinbi += tip
                        # 在今日中增加销量、声望和收入
                        gameData.today["销量"][cst_need["酒类"]] += cst_need["数量"] * 0.25
                        gameData.today["声望"] += cst["声望增加"]
                        gameData.today["收入"] += (tip + cst_need["消费"])
                        # 将该客人从客人列表中移出
                        del customers[0]
                        # 触发客人对话
                        text = cst["名字"] + random.choice(NPC_DRUNK_WORDS)
                        if self.f_length(text) >= 90:
                            self.f_printLongText(text)
                        else:
                            self.f_printFS(text)
                        # 结语
                        text = f'{FIVE_SPACE}接待完成， +{cst_need["消费"]}金币\n{FIVE_SPACE}小费: {tip}金币\n{FIVE_SPACE}声望增加: {cst["声望增加"]}'
                        input(text)
                    # 酒水不足，交易失败
                    else:
                        self.f_printFS("酒水不足，无法完成接待\n")
                        if self.f_chance(10):  # 10%的概率客人生气闹事
                            text = f'{cst["名字"]} 因为没喝到酒非常生气，掀翻了酒馆好几个桌子，虽然你及时制止了他，但还是损失了一些物品'
                            self.f_printLongText(text)
                            self.f_decNaijiu(2)
                            gameData.today["耐久"] -= 2
                            input(f"{FIVE_SPACE}酒馆耐久 -2")
                        else:  # 客人没有生气，离开酒馆
                            input(f'{FIVE_SPACE}{cst["名字"]} 有些失望，摇摇头离开了酒馆')
                # 赶走
                elif choice == "2":
                    # 扣除声望
                    self.f_decShengWang(0.5)
                    gameData.today["声望"] -= 0.5
                    # 闹事
                    if self.f_chance(50):
                        text = f'{cst["名字"]}听说你要赶走他，非常的生气，愤怒的他砸坏了你几张桌子，你及时制止了他，但还不不可避免的损失了些东西'
                        self.f_printLongText(text)
                        # 扣除耐久
                        self.f_decNaijiu(2)
                        gameData.today["耐久"] -= 2
                        input(f'{FIVE_SPACE}酒馆耐久 -2')
                    else:
                        text = f'{cst["名字"]}听说你要赶走他，失落又生气的离开了...'
                        input(f'{FIVE_SPACE}{text}')
                # 结束营业
                elif choice == "3":
                    if self.f_confirm("确定要结束今日营业吗", "已结束今日营业"):
                        break
            # 结束营业
            elif choice == "3":
                if self.f_confirm("确定要结束今日营业吗", "已结束今日营业"):
                    break
        SOUNDS["开门营业"].stop()

    # 修缮酒馆界面
    def page_fixBar(self):
        gameData = getGameData()
        # 声望-1
        gameData.shengwang -= 1
        # 今日声望-1
        gameData.today["声望"] -= 1
        SOUNDS["修缮酒馆"].play(-1)
        while True:
            self.f_clearScreen()
            self.f_printTitle("修缮奥克的酒馆")
            # 信息
            text = f"当前金币: {gameData.getMoney()}枚 | 酒馆声望: {gameData.shengwang} | 酒馆耐久: {gameData.naijiu}"
            self.f_printCenter(text)
            print()
            # 提示
            self.f_printCenter("不同修缮等级消耗不同金币，提升耐久和声望")
            print()
            self.f_fontColor(Fore.CYAN)
            self.f_printFS("- 简易修补：1 枚金币 -> 耐久 + 2")
            self.f_printFS("- 更换木桌：3 枚金币 -> 耐久 + 4，声望 + 1")
            print()
            self.f_printCaozuo()
            self.f_printCenter("1.简易修补 2.更换木桌 0.结束修缮")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            choice = input(f'{FIVE_SPACE}输入选项: ')
            print()
            if choice == "1":
                # 金币足够
                if gameData.jinbi >= 1:
                    gameData.jinbi -= 1
                    self.f_addNaijiu(2)
                    gameData.today["收入"] -= 1
                    gameData.today["耐久"] += 2
                    input(f'{FIVE_SPACE}简易修补完成，酒馆耐久 +2')
                # 金币不够
                else:
                    input(f'{FIVE_SPACE}简易修补失败，金币不够')
            elif choice == "2":
                # 金币足够
                if gameData.jinbi >= 3:
                    gameData.jinbi -= 3
                    self.f_addNaijiu(4)
                    self.f_addShengWang(1)
                    gameData.today["收入"] -= 3
                    gameData.today["耐久"] += 4
                    gameData.today["声望"] += 1
                    input(f'{FIVE_SPACE}更换木桌完成，酒馆耐久 +4，酒馆声望 +1')
                # 金币不够
                else:
                    input(f'{FIVE_SPACE}更换木桌失败，金币不够')
            elif choice == "0":
                input(f'{FIVE_SPACE}已结束酒馆修缮')
                break
        SOUNDS["修缮酒馆"].stop()

    # 查看账本界面
    def page_ledger(self):
        gameData = getGameData()
        while True:
            self.f_clearScreen()
            self.f_printTitle("奥克的酒馆账本")
            self.f_fontColor(Fore.CYAN)
            # 标题
            self.f_printFS("—"*21 + " 账本 " + "—"*21)
            print()
            # 3项标题
            zhangben = gameData.zhangben
            space = " "*13
            text = f'{space}销量{space * 2}利润{space * 2}债务\n'
            self.f_printFS(text)
            # 数据
            left_list = []
            for k in zhangben["销量"].keys():
                sales = zhangben["销量"][k]
                text = f"{k}:{sales}桶"
                left_space = self.f_centerSpace(30, text)
                left_list.append(f"{left_space}{text}{left_space}")
            middle_space = " "*((30 - self.f_length(zhangben["利润"])) // 2)
            middle = f'{middle_space}{zhangben["利润"]}{middle_space}'
            right_space = " "*((30 - self.f_length(zhangben["债务"])) // 2)
            right = f'{right_space}{zhangben["债务"]}{right_space}'
            # 打印这3行
            self.f_printFS(left_list[0] + middle + right)
            self.f_printFS(left_list[1])
            self.f_printFS(left_list[2])
            print()
            # 操作
            self.f_printCaozuo()
            self.f_printCenter("0. 结束查看")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            choice = input(f'{FIVE_SPACE}输入选项: ')
            if choice == "0":
                break

    # 今日营业结果界面
    def page_todayResult(self):
        gameData = getGameData()
        while True:
            self.f_clearScreen()
            self.f_printTitle("今日营业结果")
            self.f_fontColor(Fore.CYAN)
            # 标题
            self.f_printFS("—"*20 + " 营业结果 " + "—"*20)
            print()
            # 收入
            self.f_printFS(f"- 收入: {round(gameData.today['收入'], 2)}\n")
            # 销量
            one   = f'麦酒:{gameData.today["销量"]["麦酒"]}桶'
            two   = f'蜜酒:{gameData.today["销量"]["蜜酒"]}桶'
            three = f'果酒:{gameData.today["销量"]["果酒"]}桶'
            self.f_printFS(f"- 销量: {one}{FIVE_SPACE}{two}{FIVE_SPACE}{three}\n")
            # 声望
            self.f_printFS(f"- 声望: {round(gameData.today['声望'], 2)}\n")
            # 耐久
            self.f_printFS(f"- 耐久: {gameData.today['耐久']}")
            self.f_fontColor(Fore.YELLOW)
            self.f_printTitle()
            input(f'{FIVE_SPACE}按下回车继续...')
            # 重置每日的状态
            gameData.today = {
                "收入": 0,
                "销量": {
                    "麦酒": 0,
                    "蜜酒": 0,
                    "果酒": 0
                },
                "声望": 0,
                "耐久": 0
            }
            break

    # 随机事件界面
    def page_randomEvent(self):
        """
        发生随机事件
        正面事件：
            商队路过，高价收购 10 桶麦酒（收入 10 枚，声望 + 5）
            隐士赠送稀有酿酒配方（提升酿酒成功率 10%）
        负面事件：
            领主收税，需缴纳 2 枚金币（不交则声望 - 10）
            酒馆闹鼠患，损耗 5 份麦芽，耐久 - 5
            醉酒佣兵闹事，打坏家具（耐久 - 15，需花 1 枚修缮）
        :return: 无
        """
        # 发生随机事件
        if self.f_chance(30):
            is_good = self.f_chance(50)
            # 正面事件
            if is_good:
                event = random.choice(["商队","隐士"])
                if event == "商队":
                    self.f_clearScreen()
                    self.f_printTitle("随机事件")
                    print("\n\n\n")
                    self.f_printCenter("商队路过，高价收购 10 桶麦酒")
                    self.f_printCenter("（收入 10 枚，声望 + 5）")
                    print("\n\n\n")
                    self.f_printCenter("1. 接收 2.拒绝（其它输入也是拒绝）")
                    self.f_printTitle()
                    choice = input(f'{FIVE_SPACE}输入选项: ')
                    print()
                    if choice == "1":
                        # 数量足够
                        if getGameData().kucun["麦酒"] >= 10:
                            getGameData().jinbi += 10
                            getGameData().shengwang += 5
                            getGameData().kucun["麦酒"] -= 10
                            getGameData().zhangben["利润"] += 10
                            getGameData().zhangben["销量"]["麦酒"] += 10
                            input(f'{FIVE_SPACE}交易成功！金币 +10 声望 +5')
                        # 数量不够
                        else:
                            input(f'{FIVE_SPACE}交易失败！麦酒数量不够')
                    else:
                        input(f'{FIVE_SPACE}你拒绝了交易，按下回车继续...')
                elif event == "隐士":
                    self.f_clearScreen()
                    self.f_printTitle("随机事件")
                    print("\n\n\n")
                    self.f_printCenter("一个不知从哪里来的隐士，进来讨了一杯水喝，走后留下了一份稀有的酿酒配方")
                    self.f_printCenter("（提升酿酒成功率 10%）")
                    print("\n\n\n")
                    self.f_printTitle()
                    input(f'{FIVE_SPACE}按下回车继续...')
            # 负面事件
            else:
                event = random.choice(["领主","鼠患","闹事"])
                if event == "领主":
                    self.f_clearScreen()
                    self.f_printTitle("随机事件")
                    print("\n\n\n")
                    self.f_printCenter("领主收税，需缴纳 2 枚金币")
                    self.f_printCenter("（不交则声望 - 10）")
                    print("\n\n\n")
                    self.f_printCenter("1. 交税 2. 拒绝交税（其它输入也是拒绝）")
                    self.f_printTitle()
                    choice = input(f'{FIVE_SPACE}输入选项: ')
                    print()
                    if choice == "1":
                        # 如果钱够
                        if getGameData().jinbi >= 2:
                            getGameData().jinbi -= 2
                            input(f'{FIVE_SPACE}交税完成！你的酒馆相安无事...')
                        # 钱不够
                        else:
                            getGameData().shengwang -= 10
                            input(f'{FIVE_SPACE}交税失败！你的金币不够，酒馆声望 -10')
                    else:
                        getGameData().shengwang -= 10
                        input(f'{FIVE_SPACE}拒绝交税！酒馆声望 -10')
                elif event == "鼠患":
                    self.f_clearScreen()
                    self.f_printTitle("随机事件")
                    print("\n\n\n")
                    self.f_printCenter("酒馆闹鼠患，损耗 5 份麦芽，酒馆耐久 - 5")
                    print("\n\n\n")
                    # 扣除麦芽5份
                    getGameData().kucun["麦芽"] -= 5
                    if getGameData().kucun["麦芽"] < 0:
                        getGameData().kucun["麦芽"] = 0
                    # 扣除酒馆耐久5
                    getGameData().naijiu -= 5
                    if getGameData().naijiu < 0:
                        getGameData().naijiu = 0
                    # 等待
                    input(f'{FIVE_SPACE}酒馆闹鼠患，糟糕透了...')
                elif event == "闹事":
                    self.f_clearScreen()
                    self.f_printTitle("随机事件")
                    print("\n\n\n")
                    self.f_printCenter("醉酒佣兵闹事，打坏家具")
                    self.f_printCenter("（耐久 - 10，需花 1 枚修缮）")
                    print("\n\n\n")
                    # 扣除酒馆耐久10
                    getGameData().naijiu -= 10
                    if getGameData().naijiu < 0:
                        getGameData().naijiu = 0
                    # 选项
                    self.f_printCenter("1. 修缮 2. 不管（其它输入也是拒绝）")
                    self.f_printTitle()
                    choice = input(f'{FIVE_SPACE}输入选项: ')
                    if choice == "1":
                        # 钱足够
                        if getGameData().jinbi >= 1:
                            getGameData().jinbi -= 1
                            getGameData().naijiu += 10
                            input(f'{FIVE_SPACE}修缮成功！这些可恶的醉酒佣兵真不是东西...')
                        # 钱不够
                        else:
                            input(f'{FIVE_SPACE}钱不够修缮家具，只能先不管了...')
                    else:
                        input(f'{FIVE_SPACE}先暂时不修了，下次他们敢来一定要让他们吃点苦头...')
        # 未发生随机事件
        else:
            self.f_clearScreen()
            self.f_printTitle("随机事件")
            print("\n\n\n")
            self.f_printCenter("今天是个宁静的夜晚，没有任何事件发生...")
            print("\n\n\n")
            self.f_printTitle()
            input(f'{FIVE_SPACE}按下回车继续...')

    # 结束语界面
    def page_endToday(self):
        for i in range(3):
            self.f_clearScreen()
            self.f_printTitle(CONFIG["game_name"])
            print("\n\n\n")
            self.f_printCenter("酒馆的一天结束了" + "."*(i+1))
            print("\n\n\n")
            self.f_printTitle()
            self.f_sleep(0.5)

    # 今日已完成界面
    def page_wancheng(self):
        self.f_clearScreen()
        self.f_printTitle(CONFIG["game_name"])
        print("\n\n\n")
        self.f_printCenter("今日操作已完成")
        print("\n\n\n")
        self.f_printTitle()
        self.f_sleep()

    # 天数界面
    def page_tianshu(self):
        self.f_clearScreen()
        SOUNDS["翻页"].play()
        self.f_printTitle(CONFIG["game_name"])
        print("\n\n\n")
        self.f_printCenter(f'第{getGameData().tianshu}天')
        print("\n\n\n")
        self.f_printTitle()
        self.f_sleep()

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
        self.zhangben = data["账本"]
        # 今日数据，不保存存档，打印完今日营业结果后重置
        self.today = {
            "收入": 0,
            "销量": {
                "麦酒": 0,
                "蜜酒": 0,
                "果酒": 0
            },
            "声望": 0,
            "耐久": 0
        }

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
                "售价": self.shoujia,
                "账本": self.zhangben
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
