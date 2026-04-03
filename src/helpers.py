"""
用户帮助和新手引导模块
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


class UserHelper:
    """用户帮助系统"""

    @staticmethod
    def show_welcome_guide():
        """显示欢迎引导（新手）"""
        guide = """
[bold cyan]👋 欢迎使用生日派对计划工具！[/bold cyan]

[yellow]📖 快速入门（3步）：[/yellow]

  1️⃣  创建派对
     • 输入孩子信息和派对日期
     • 系统自动生成购物清单建议

  2️⃣  管理准备工作
     • 添加客人并追踪RSVP
     • 按商店分组查看购物清单
     • 使用检查清单不遗漏重要事项

  3️⃣  导出和分享
     • 导出客人签到表
     • 生成微信邀请函
     • 打印购物清单去采购

[green]💡 小贴士：[/green]
  • 随时输入 'help' 或 '?' 查看帮助
  • 所有数据自动保存，不用担心丢失
  • 可以随时返回修改，直到满意为止

[dim]按回车继续...[/dim]
"""
        console.print(Panel(guide, border_style="cyan"))

    @staticmethod
    def show_help():
        """显示帮助文档"""
        table = Table(title="帮助文档", box=box.ROUNDED, show_header=True)
        table.add_column("功能", style="cyan", width=20)
        table.add_column("说明", style="white", width=50)

        table.add_row(
            "派对管理",
            "创建、查看、修改派对信息"
        )
        table.add_row(
            "客人管理",
            "添加客人、追踪RSVP状态、批量导入"
        )
        table.add_row(
            "购物清单",
            "自动生成建议、按商店/优先级查看、快速调整价格"
        )
        table.add_row(
            "检查清单",
            "8阶段46项任务，确保不遗漏重要事项"
        )
        table.add_row(
            "导出/打印",
            "签到表、购物清单、派对总结、微信邀请函"
        )
        table.add_row(
            "预算跟踪",
            "实时监控花费，避免超支"
        )

        console.print("\n")
        console.print(table)

        console.print("\n[bold yellow]💡 使用技巧：[/bold yellow]")
        console.print("  • 批量添加客人：用逗号分隔 '姓名,电话,备注'")
        console.print("  • 日期输入：支持 2026-05-01 或 5月1日")
        console.print("  • 简化版购物清单：适合手机查看和截图")
        console.print("  • 导出功能：可打印纸质版带去采购")

    @staticmethod
    def show_budget_tips():
        """显示省钱建议"""
        tips = """
[bold yellow]💰 省钱小贴士[/bold yellow]

[green]可以自制的：[/green]
  • 邀请函 - 用手机设计图片
  • 装饰品 - DIY气球拱门、纸花
  • 小礼物 - 手工糖果包、贴纸

[green]可以借用的：[/green]
  • 音响设备 - 问朋友借蓝牙音箱
  • 桌椅 - 场地通常提供
  • 游戏道具 - 用家里的玩具

[green]可以省略的：[/green]
  • 派对帽 - 如果预算紧张可以不买
  • 礼品袋 - 可以简化为糖果+贴纸
  • 专业摄影 - 家长用手机拍照

[green]省钱技巧：[/green]
  • 蛋糕：超市蛋糕比定制便宜50%
  • 装饰：网购比实体店便宜30-50%
  • 食物：自己准备比外卖便宜
  • 时间：非周末价格更优惠
"""
        console.print(Panel(tips, border_style="yellow"))

    @staticmethod
    def parse_friendly_date(date_str: str) -> str:
        """
        解析友好的日期格式
        支持: 2026-05-01, 5月1日, 5-1, 2026年5月1日
        """
        import re
        from datetime import datetime

        date_str = date_str.strip()

        # 标准格式
        if re.match(r'\d{4}-\d{1,2}-\d{1,2}', date_str):
            return date_str

        # 中文格式: 5月1日
        match = re.match(r'(\d{1,2})月(\d{1,2})[日号]?', date_str)
        if match:
            month, day = match.groups()
            year = datetime.now().year
            # 如果日期已过，使用明年
            try:
                test_date = datetime(year, int(month), int(day))
                if test_date < datetime.now():
                    year += 1
            except:
                pass
            return f"{year}-{int(month):02d}-{int(day):02d}"

        # 年月日格式: 2026年5月1日
        match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})[日号]?', date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"

        # 简写格式: 5-1
        match = re.match(r'(\d{1,2})-(\d{1,2})$', date_str)
        if match:
            month, day = match.groups()
            year = datetime.now().year
            try:
                test_date = datetime(year, int(month), int(day))
                if test_date < datetime.now():
                    year += 1
            except:
                pass
            return f"{year}-{int(month):02d}-{int(day):02d}"

        # 无法解析，返回原值
        return date_str


class MoneySaving:
    """省钱建议系统"""

    @staticmethod
    def analyze_budget(shopping_list, budget: float) -> dict:
        """分析预算并给出建议"""
        total_estimated = sum(item.estimated_price * item.quantity for item in shopping_list)

        suggestions = {
            "diy_items": [],  # 可以自制
            "optional_items": [],  # 可以省略
            "cheaper_alternatives": [],  # 便宜替代
            "savings_potential": 0  # 潜在节省
        }

        for item in shopping_list:
            # 可以自制的物品
            diy_keywords = ["邀请函", "装饰", "游戏道具", "小礼物", "彩带", "横幅"]
            if any(k in item.name for k in diy_keywords):
                savings = item.estimated_price * item.quantity * 0.7  # 可节省70%
                suggestions["diy_items"].append({
                    "name": item.name,
                    "savings": savings,
                    "tip": "可以自己动手制作"
                })
                suggestions["savings_potential"] += savings

            # 可以省略的物品（可选优先级）
            if item.priority == "可选":
                savings = item.estimated_price * item.quantity
                suggestions["optional_items"].append({
                    "name": item.name,
                    "savings": savings,
                    "tip": "预算紧张时可以省略"
                })

            # 有便宜替代的物品
            expensive_items = ["蛋糕", "摄影", "场地"]
            if any(k in item.name for k in expensive_items):
                if "蛋糕" in item.name:
                    savings = item.estimated_price * 0.5
                    suggestions["cheaper_alternatives"].append({
                        "name": item.name,
                        "original_price": item.estimated_price,
                        "alternative": "超市蛋糕",
                        "new_price": item.estimated_price * 0.5,
                        "savings": savings
                    })
                    suggestions["savings_potential"] += savings

        return suggestions

    @staticmethod
    def show_savings_report(shopping_list, budget: float):
        """显示省钱报告"""
        suggestions = MoneySaving.analyze_budget(shopping_list, budget)

        console.print("\n[bold yellow]💰 省钱建议报告[/bold yellow]\n")

        if suggestions["diy_items"]:
            console.print("[green]可以自制（节省材料费）：[/green]")
            for item in suggestions["diy_items"]:
                console.print(f"  • {item['name']} - 可节省约¥{item['savings']:.0f}")
            console.print()

        if suggestions["cheaper_alternatives"]:
            console.print("[green]便宜替代方案：[/green]")
            for item in suggestions["cheaper_alternatives"]:
                console.print(f"  • {item['name']}: ¥{item['original_price']:.0f}")
                console.print(f"    → {item['alternative']}: ¥{item['new_price']:.0f}")
                console.print(f"    节省：¥{item['savings']:.0f}")
            console.print()

        if suggestions["optional_items"]:
            console.print("[yellow]预算紧张可省略：[/yellow]")
            for item in suggestions["optional_items"]:
                console.print(f"  • {item['name']} - 可节省¥{item['savings']:.0f}")
            console.print()

        console.print(f"[bold cyan]潜在节省总额：¥{suggestions['savings_potential']:.0f}[/bold cyan]")

        total_estimated = sum(i.estimated_price * i.quantity for i in shopping_list)
        if suggestions["savings_potential"] > 0:
            new_total = total_estimated - suggestions["savings_potential"]
            console.print(f"优化后预算：¥{new_total:.0f}")

            if new_total <= budget:
                console.print("[green]✓ 优化后在预算内！[/green]")
            else:
                console.print(f"[yellow]还需再省¥{new_total - budget:.0f}[/yellow]")
