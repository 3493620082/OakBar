import os
import json

def main():
    unlock = False  # 解锁状态

    with open("..\\npc.json", 'r', encoding="utf-8") as f:
        NPCS = json.load(f)

    def foo(it_list):
        for i in range(len(it_list)):
            it_list[i]["故事"]["解锁"] = unlock
        return it_list

    NPCS["基础"] = foo(NPCS["基础"])
    NPCS["低级"] = foo(NPCS["低级"])
    NPCS["中级"] = foo(NPCS["中级"])
    NPCS["高级"] = foo(NPCS["高级"])
    NPCS["稀有"] = foo(NPCS["稀有"])

    with open("..\\npc.json", 'w', encoding="utf-8") as f:
        json.dump(NPCS, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()