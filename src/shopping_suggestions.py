"""
购物清单建议生成器
"""
from models import ShoppingItem
from typing import List


class ShoppingSuggestions:
    """根据派对信息生成购物建议"""

    @staticmethod
    def generate_basic_items(guest_count: int, budget_per_person: float = 0) -> List[ShoppingItem]:
        """生成基本购物清单"""
        items = []

        # 装饰类
        items.extend([
            ShoppingItem("生日横幅", "装饰", 1, 30.0),
            ShoppingItem("气球套装", "装饰", 1, 50.0),
            ShoppingItem("彩带", "装饰", 3, 15.0),
            ShoppingItem("派对帽", "装饰", guest_count, 3.0),
            ShoppingItem("桌布", "装饰", 2, 25.0),
        ])

        # 餐具用品
        items.extend([
            ShoppingItem("一次性盘子", "用品", guest_count, 2.0),
            ShoppingItem("一次性杯子", "用品", guest_count, 1.5),
            ShoppingItem("餐巾纸", "用品", guest_count, 0.5),
            ShoppingItem("叉子勺子", "用品", guest_count, 1.0),
        ])

        # 食物和饮料
        items.extend([
            ShoppingItem("生日蛋糕", "食物", 1, 200.0),
            ShoppingItem("零食拼盘", "食物", 3, 40.0),
            ShoppingItem("水果拼盘", "食物", 2, 50.0),
            ShoppingItem("饮料", "食物", guest_count, 5.0),
            ShoppingItem("果汁", "食物", guest_count // 2, 8.0),
        ])

        # 娱乐和活动
        items.extend([
            ShoppingItem("派对游戏道具", "娱乐", 3, 30.0),
            ShoppingItem("音乐播放列表", "娱乐", 1, 0.0, notes="提前准备"),
        ])

        # 礼品和纪念品
        items.extend([
            ShoppingItem("小礼品袋", "礼物", guest_count, 15.0, notes="感谢礼物"),
            ShoppingItem("贴纸", "礼物", guest_count * 2, 2.0),
        ])

        # 其他
        items.extend([
            ShoppingItem("蜡烛", "用品", 1, 10.0),
            ShoppingItem("打火机/火柴", "用品", 1, 5.0),
        ])

        return items

    @staticmethod
    def generate_themed_items(theme: str) -> List[ShoppingItem]:
        """根据主题生成特定装饰品"""
        theme_items = {
            "超级英雄": [
                ShoppingItem("超级英雄海报", "装饰", 3, 25.0),
                ShoppingItem("超级英雄面具", "装饰", 10, 8.0),
                ShoppingItem("超级英雄主题盘子", "用品", 20, 3.0),
            ],
            "公主": [
                ShoppingItem("皇冠", "装饰", 10, 12.0),
                ShoppingItem("公主主题横幅", "装饰", 1, 35.0),
                ShoppingItem("粉色气球", "装饰", 50, 1.0),
            ],
            "恐龙": [
                ShoppingItem("恐龙玩偶", "装饰", 5, 20.0),
                ShoppingItem("恐龙主题餐具", "用品", 20, 3.0),
                ShoppingItem("恐龙脚印贴纸", "装饰", 30, 2.0),
            ],
            "海洋": [
                ShoppingItem("海洋生物气球", "装饰", 30, 2.0),
                ShoppingItem("蓝色桌布", "装饰", 2, 20.0),
                ShoppingItem("海星装饰", "装饰", 5, 8.0),
            ],
            "太空": [
                ShoppingItem("星球气球", "装饰", 20, 3.0),
                ShoppingItem("宇航员立牌", "装饰", 3, 30.0),
                ShoppingItem("星星灯饰", "装饰", 1, 50.0),
            ],
            "动物园": [
                ShoppingItem("动物面具", "装饰", 15, 8.0),
                ShoppingItem("动物气球", "装饰", 30, 2.0),
                ShoppingItem("丛林装饰藤蔓", "装饰", 5, 15.0),
            ],
        }

        theme_lower = theme.lower()
        for key, items in theme_items.items():
            if key.lower() in theme_lower or theme_lower in key.lower():
                return items

        return []

    @staticmethod
    def generate_age_appropriate_items(age: int) -> List[ShoppingItem]:
        """根据年龄生成适合的物品"""
        items = []

        if age <= 3:
            items.extend([
                ShoppingItem("软质玩具", "礼物", 5, 25.0),
                ShoppingItem("彩色积木", "娱乐", 2, 40.0),
                ShoppingItem("泡泡机", "娱乐", 1, 60.0),
            ])
        elif age <= 6:
            items.extend([
                ShoppingItem("绘画套装", "娱乐", 5, 30.0),
                ShoppingItem("拼图", "娱乐", 3, 35.0),
                ShoppingItem("小玩具套装", "礼物", 10, 20.0),
            ])
        elif age <= 10:
            items.extend([
                ShoppingItem("桌游", "娱乐", 2, 80.0),
                ShoppingItem("手工DIY套装", "娱乐", 5, 40.0),
                ShoppingItem("运动器材（足球/飞盘）", "娱乐", 2, 50.0),
            ])
        else:
            items.extend([
                ShoppingItem("电子游戏/游戏机租赁", "娱乐", 1, 200.0),
                ShoppingItem("卡拉OK设备", "娱乐", 1, 150.0),
                ShoppingItem("照相道具", "娱乐", 10, 15.0),
            ])

        return items

    @staticmethod
    def optimize_budget(items: List[ShoppingItem], max_budget: float) -> List[ShoppingItem]:
        """根据预算优化购物清单"""
        total = sum(item.estimated_price * item.quantity for item in items)

        if total <= max_budget:
            return items

        # 按优先级排序（基本用品 > 食物 > 装饰 > 娱乐 > 礼物）
        priority = {"用品": 1, "食物": 2, "装饰": 3, "娱乐": 4, "礼物": 5}

        sorted_items = sorted(items, key=lambda x: (priority.get(x.category, 6), -x.estimated_price))

        selected_items = []
        current_total = 0

        for item in sorted_items:
            item_cost = item.estimated_price * item.quantity
            if current_total + item_cost <= max_budget:
                selected_items.append(item)
                current_total += item_cost

        return selected_items
