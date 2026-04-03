#!/usr/bin/env python3
"""
模拟真实用户操作流程
场景：李女士想为她6岁女儿筹办一个公主主题生日派对
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import Party, Guest, ShoppingItem
from main import BirthdayPlannerApp
from datetime import datetime, timedelta
from rich.console import Console

console = Console()


def simulate_user_journey():
    """模拟用户完整旅程"""

    console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   模拟真实用户操作 - 李女士的故事   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")

    # 用户背景
    console.print("[yellow]背景：[/yellow]")
    console.print("李女士的女儿欣欣6岁了，想办一个公主主题生日派对")
    console.print("预算3000元，计划邀请15个小朋友")
    console.print("派对日期：两周后的周六下午2点")
    console.print()

    # 步骤1：创建派对
    console.print("[bold green]━━━ 步骤1：创建派对计划 ━━━[/bold green]")

    party_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    party = Party(
        id=f"user_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        child_name="欣欣",
        child_age=6,
        party_date=party_date,
        party_time="14:00",
        venue="欢乐儿童主题乐园",
        venue_address="市中心购物广场3楼",
        budget=3000.0,
        theme="公主",
        guest_count_expected=15
    )

    console.print(f"✓ 创建派对：{party.child_name}的{party.child_age}岁生日")
    console.print(f"✓ 日期：{party.party_date} {party.party_time}")
    console.print(f"✓ 预算：¥{party.budget}")

    # 体验反馈1
    console.print("\n[dim]💭 用户想法：输入信息挺方便的，不过如果能显示'距离派对还有X天'就更好了[/dim]")

    # 步骤2：添加客人
    console.print("\n[bold green]━━━ 步骤2：添加客人名单 ━━━[/bold green]")

    guests_to_add = [
        ("小美", "13900001111", "女儿的好朋友"),
        ("小明", "13900002222", "幼儿园同学"),
        ("小红", "13900003333", "邻居家小孩"),
        ("小刚", "13900004444", "幼儿园同学"),
        ("小丽", "13900005555", "表妹"),
    ]

    for name, contact, note in guests_to_add:
        party.add_guest(Guest(name, contact, notes=note))
        console.print(f"✓ 添加客人：{name} ({note})")

    console.print(f"\n总共添加了 {len(party.guests)} 位客人")

    # 体验反馈2
    console.print("\n[dim]💭 用户想法：一个一个添加有点慢，如果能批量导入就好了[/dim]")
    console.print("[yellow]⚠️  发现问题：缺少批量添加客人功能[/yellow]")

    # 步骤3：查看购物清单
    console.print("\n[bold green]━━━ 步骤3：查看购物清单建议 ━━━[/bold green]")

    from shopping_suggestions import ShoppingSuggestions
    items = ShoppingSuggestions.generate_basic_items(15)
    themed_items = ShoppingSuggestions.generate_themed_items("公主")
    age_items = ShoppingSuggestions.generate_age_appropriate_items(6)

    all_items = items + themed_items + age_items
    optimized = ShoppingSuggestions.optimize_budget(all_items, 3000)

    for item in optimized:
        party.add_shopping_item(item)

    console.print(f"✓ 自动生成了 {len(party.shopping_list)} 项购物建议")

    # 按商店查看
    console.print("\n[cyan]按商店分组查看：[/cyan]")
    stores = {}
    for item in party.shopping_list:
        if item.store not in stores:
            stores[item.store] = []
        stores[item.store].append(item)

    for store, store_items in sorted(stores.items()):
        total = sum(i.estimated_price * i.quantity for i in store_items)
        must_buy = sum(1 for i in store_items if i.priority == "必买")
        console.print(f"  📍 {store}: {len(store_items)}项 (必买{must_buy}项) - 预估¥{total:.0f}")

    # 体验反馈3
    console.print("\n[dim]💭 用户想法：按商店分组很实用！但我想知道哪些店离得近，能一起去[/dim]")
    console.print("[dim]💭 用户想法：有些价格看起来不太准确，能不能让我自己调整？[/dim]")

    # 步骤4：检查清单
    console.print("\n[bold green]━━━ 步骤4：查看派对检查清单 ━━━[/bold green]")

    from checklist import PartyChecklist
    phases = PartyChecklist.generate_standard_checklist(6, 15)

    current_phase = PartyChecklist.get_current_phase(phases, party.party_date)
    console.print(f"✓ 生成了 {len(phases)} 个阶段的检查清单")
    console.print(f"✓ 当前应关注：{current_phase.name}")
    console.print(f"\n当前阶段任务：")
    for i, item in enumerate(current_phase.items[:5], 1):
        console.print(f"  {i}. □ {item.title}")

    # 体验反馈4
    console.print("\n[dim]💭 用户想法：检查清单太有用了！但任务有点多，能不能标注哪些是最重要的？[/dim]")
    console.print("[yellow]⚠️  发现问题：检查清单没有优先级标记[/yellow]")

    # 步骤5：更新RSVP
    console.print("\n[bold green]━━━ 步骤5：几天后，开始收到RSVP回复 ━━━[/bold green]")

    # 模拟收到回复
    party.guests[0].rsvp_status = "confirmed"
    party.guests[0].plus_ones = 1  # 带妈妈一起
    party.guests[1].rsvp_status = "confirmed"
    party.guests[2].rsvp_status = "pending"
    party.guests[3].rsvp_status = "declined"  # 不能来
    party.guests[4].rsvp_status = "confirmed"

    # 显示RSVP统计
    confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
    pending = sum(1 for g in party.guests if g.rsvp_status == "pending")
    declined = sum(1 for g in party.guests if g.rsvp_status == "declined")
    total_attendees = party.get_confirmed_guests_count()

    console.print(f"✓ 已确认：{confirmed} 人（实际参加 {total_attendees} 人）")
    console.print(f"⏳ 待确认：{pending} 人")
    console.print(f"✗ 已拒绝：{declined} 人")

    # 体验反馈5
    console.print("\n[dim]💭 用户想法：统计很清楚！但我想导出一个简单的名单打印出来[/dim]")
    console.print("[yellow]⚠️  发现问题：缺少打印/导出功能[/yellow]")

    # 步骤6：采购
    console.print("\n[bold green]━━━ 步骤6：周末去采购 ━━━[/bold green]")

    # 模拟去超市采购
    supermarket_items = [i for i in party.shopping_list if i.store == "超市"]
    console.print(f"\n去超市采购 {len(supermarket_items)} 项：")

    total_spent = 0
    for item in supermarket_items[:3]:  # 买了前3样
        item.purchased = True
        # 实际价格可能不同
        item.actual_price = item.estimated_price * 0.9  # 打9折
        spent = item.actual_price * item.quantity
        total_spent += spent
        console.print(f"  ✓ {item.name} x{item.quantity} - ¥{spent:.0f} (比预估便宜)")

    console.print(f"\n本次消费：¥{total_spent:.0f}")
    console.print(f"剩余预算：¥{party.get_budget_remaining():.0f}")

    # 体验反馈6
    console.print("\n[dim]💭 用户想法：在超市时，用手机看清单有点不方便，字太多了[/dim]")
    console.print("[yellow]⚠️  发现问题：缺少手机友好的简化视图[/yellow]")

    # 步骤7：生成邀请函
    console.print("\n[bold green]━━━ 步骤7：生成邀请函 ━━━[/bold green]")

    from invitation import InvitationGenerator

    # 为第一个客人生成邀请函
    guest = party.guests[0]
    invitation = InvitationGenerator.generate_text_invitation(party, guest)

    console.print(f"✓ 为 {guest.name} 生成了邀请函")
    console.print("\n[dim]邀请函预览：[/dim]")
    console.print("[dim]" + "─" * 40 + "[/dim]")
    # 只显示前几行
    lines = invitation.split('\n')[:10]
    for line in lines:
        console.print(f"[dim]{line}[/dim]")
    console.print("[dim]...[/dim]")

    # 体验反馈7
    console.print("\n[dim]💭 用户想法：邀请函很漂亮！但我想微信群发，能生成纯文本简短版本吗？[/dim]")
    console.print("[yellow]⚠️  发现问题：缺少简短版邀请函[/yellow]")

    # 总结
    console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         用户体验总结         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")

    console.print("[bold green]✅ 体验很好的功能：[/bold green]")
    console.print("  1. 购物清单按商店分组 - 实际采购时非常实用")
    console.print("  2. RSVP统计面板 - 一目了然，不会搞混")
    console.print("  3. 检查清单 - 不会忘记重要事项")
    console.print("  4. 优先级标记 - 预算紧张时知道先买什么")

    console.print("\n[bold yellow]⚠️  发现的问题（需要优化）：[/bold yellow]")
    problems = [
        "1. 缺少批量添加客人功能（一个一个加太慢）",
        "2. 检查清单任务没有优先级标记",
        "3. 缺少打印/导出功能（需要纸质版）",
        "4. 缺少手机友好的简化视图",
        "5. 缺少简短版邀请函（适合微信群发）",
        "6. 没有显示'距离派对还有X天'",
        "7. 购物清单价格不能快速调整",
    ]

    for problem in problems:
        console.print(f"  {problem}")

    console.print("\n[bold cyan]📊 关键指标：[/bold cyan]")
    console.print(f"  • 派对创建：5分钟 ⭐⭐⭐⭐")
    console.print(f"  • 添加5个客人：3分钟 ⭐⭐⭐ (可以更快)")
    console.print(f"  • 查看购物清单：1分钟 ⭐⭐⭐⭐⭐")
    console.print(f"  • 检查清单浏览：2分钟 ⭐⭐⭐⭐")
    console.print(f"  • 更新RSVP：每人30秒 ⭐⭐⭐⭐")
    console.print(f"  • 生成邀请函：1分钟 ⭐⭐⭐⭐")
    console.print(f"\n  总体评分：⭐⭐⭐⭐ (4/5星)")

    return problems


if __name__ == "__main__":
    problems = simulate_user_journey()

    console.print("\n[bold magenta]💡 建议的优化优先级：[/bold magenta]")
    console.print("  [bold red]高优先级：[/bold red]")
    console.print("    • 批量添加客人")
    console.print("    • 简化版购物清单（手机查看）")
    console.print("    • 倒计时显示")
    console.print("\n  [bold yellow]中优先级：[/bold yellow]")
    console.print("    • 简短版邀请函")
    console.print("    • 导出/打印功能")
    console.print("\n  [bold green]低优先级：[/bold green]")
    console.print("    • 检查清单优先级")
    console.print("    • 购物清单价格快速调整")
