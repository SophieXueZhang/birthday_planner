"""
仪表盘/总览视图
让用户一眼看到所有关键信息
"""
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich import box

console = Console()


class PartyDashboard:
    """派对仪表盘"""

    @staticmethod
    def show_overview(party):
        """显示总览视图"""
        console.print("\n")
        console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
        console.print(f"[bold cyan]   {party.child_name}的{party.child_age}岁生日派对 - 总览   [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

        # 倒计时
        PartyDashboard._show_countdown(party)

        # 关键指标
        PartyDashboard._show_key_metrics(party)

        # 紧急事项
        PartyDashboard._show_urgent_items(party)

        console.print()

    @staticmethod
    def _show_countdown(party):
        """显示倒计时"""
        try:
            party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
            days_until = (party_dt - datetime.now()).days

            if days_until > 0:
                urgency = "green" if days_until > 14 else "yellow" if days_until > 7 else "red"
                console.print(f"[{urgency}]⏰ 距离派对还有 {days_until} 天[/{urgency}]")
            elif days_until == 0:
                console.print("[bold red]🎉 今天就是派对日！[/bold red]")
            else:
                console.print("[dim]派对已结束[/dim]")
        except:
            console.print("[dim]无效的派对日期[/dim]")

        console.print()

    @staticmethod
    def _show_key_metrics(party):
        """显示关键指标"""
        table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        table.add_column("指标", style="cyan", width=15)
        table.add_column("进度", width=60)

        # 检查清单完成度
        if party.checklist_phases:
            total_items = sum(len(phase.items) for phase in party.checklist_phases)
            completed_items = sum(
                sum(1 for item in phase.items if item.completed)
                for phase in party.checklist_phases
            )
            completion_rate = completed_items / total_items * 100 if total_items > 0 else 0

            bar = PartyDashboard._create_progress_bar(completion_rate)
            table.add_row(
                "📋 检查清单",
                f"{bar} {completed_items}/{total_items} ({completion_rate:.0f}%)"
            )

        # 客人RSVP状态
        total_guests = len(party.guests)
        confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
        declined = sum(1 for g in party.guests if g.rsvp_status == "declined")
        pending = total_guests - confirmed - declined

        if total_guests > 0:
            confirmed_rate = confirmed / total_guests * 100
            bar = PartyDashboard._create_progress_bar(confirmed_rate, color="green")
            table.add_row(
                "👥 客人确认",
                f"{bar} {confirmed}确认/{pending}待定/{declined}拒绝"
            )

        # 购物进度
        total_items = len(party.shopping_list)
        purchased = sum(1 for item in party.shopping_list if item.purchased)
        if total_items > 0:
            purchase_rate = purchased / total_items * 100
            bar = PartyDashboard._create_progress_bar(purchase_rate, color="blue")
            table.add_row(
                "🛒 购物进度",
                f"{bar} {purchased}/{total_items} ({purchase_rate:.0f}%)"
            )

        # 预算使用
        total_estimated = sum(item.estimated_price * item.quantity for item in party.shopping_list)
        total_spent = sum(item.actual_price * item.quantity for item in party.shopping_list if item.purchased)

        if party.budget > 0:
            spent_rate = (total_spent / party.budget) * 100
            bar_color = "green" if spent_rate < 80 else "yellow" if spent_rate < 100 else "red"
            bar = PartyDashboard._create_progress_bar(spent_rate, color=bar_color)

            remaining = party.budget - total_spent
            table.add_row(
                "💰 预算使用",
                f"{bar} 已花¥{total_spent:.0f}/预算¥{party.budget:.0f} (剩余¥{remaining:.0f})"
            )

        console.print(table)
        console.print()

    @staticmethod
    def _create_progress_bar(percentage: float, width: int = 20, color: str = "cyan") -> str:
        """创建文本进度条"""
        filled = int(percentage / 100 * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{color}]{bar}[/{color}]"

    @staticmethod
    def _show_urgent_items(party):
        """显示紧急事项"""
        urgent = []

        # 检查未完成的重要任务
        if party.checklist_phases:
            try:
                party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
                days_until = (party_dt - datetime.now()).days

                for phase in party.checklist_phases:
                    if phase.days_before >= days_until:  # 已到期或即将到期
                        for item in phase.items:
                            if not item.completed and hasattr(item, 'priority') and item.priority == "重要":
                                urgent.append(("重要任务", item.title, phase.name))
            except:
                pass

        # 检查未确认的客人
        pending_guests = [g for g in party.guests if g.rsvp_status == "pending"]
        if len(pending_guests) > 3:
            urgent.append(("客人确认", f"{len(pending_guests)}位客人未确认RSVP", "需要跟进"))

        # 检查必买但未购买的物品
        must_buy = [item for item in party.shopping_list
                   if hasattr(item, 'priority') and item.priority == "必买" and not item.purchased]
        if len(must_buy) > 5:
            urgent.append(("购物清单", f"{len(must_buy)}件必买物品未采购", "尽快购买"))

        # 检查预算超支
        total_estimated = sum(item.estimated_price * item.quantity for item in party.shopping_list)
        if total_estimated > party.budget:
            over = total_estimated - party.budget
            urgent.append(("预算警告", f"预计花费超出预算¥{over:.0f}", "需要调整"))

        # 显示紧急事项
        if urgent:
            console.print("[bold yellow]⚠️  需要注意：[/bold yellow]")
            for category, message, action in urgent[:5]:  # 最多显示5条
                console.print(f"  • [{category}] {message} - {action}")
            console.print()
        else:
            console.print("[bold green]✓ 一切顺利，没有紧急事项！[/bold green]\n")

    @staticmethod
    def show_quick_stats(party):
        """显示快速统计（精简版）"""
        try:
            party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
            days_until = (party_dt - datetime.now()).days
            urgency = "green" if days_until > 14 else "yellow" if days_until > 7 else "red"

            # 一行总结
            checklist_completion = 0
            if party.checklist_phases:
                total = sum(len(p.items) for p in party.checklist_phases)
                done = sum(sum(1 for i in p.items if i.completed) for p in party.checklist_phases)
                checklist_completion = done / total * 100 if total > 0 else 0

            confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
            total_guests = len(party.guests)

            console.print(
                f"[{urgency}]⏰ {days_until}天[/{urgency}] | "
                f"📋 {checklist_completion:.0f}% | "
                f"👥 {confirmed}/{total_guests}人 | "
                f"💰 ¥{party.budget:.0f}"
            )
        except:
            console.print("[dim]无法加载快速统计[/dim]")


class QuickActions:
    """快捷操作"""

    @staticmethod
    def show_quick_menu():
        """显示快捷操作菜单"""
        console.print("\n[bold cyan]快捷操作：[/bold cyan]")
        console.print("  1. 添加客人")
        console.print("  2. 添加购物项")
        console.print("  3. 标记任务完成")
        console.print("  4. 查看预算")
        console.print("  5. 导出清单")
        console.print("  0. 返回主菜单")

    @staticmethod
    def quick_add_guest(party):
        """快速添加客人"""
        from models import Guest

        name = console.input("\n客人姓名: ").strip()
        if not name:
            return None

        phone = console.input("电话（可选，回车跳过）: ").strip()

        guest = Guest(name=name, phone=phone if phone else "")
        party.add_guest(guest)
        console.print(f"[green]✓ 已添加客人：{name}[/green]")
        return guest

    @staticmethod
    def quick_add_shopping_item(party):
        """快速添加购物项"""
        from models import ShoppingItem

        name = console.input("\n物品名称: ").strip()
        if not name:
            return None

        try:
            price = float(console.input("价格（元）: ").strip())
            quantity = int(console.input("数量（默认1）: ").strip() or "1")
        except:
            console.print("[red]✗ 输入无效[/red]")
            return None

        item = ShoppingItem(
            name=name,
            category="其他",
            quantity=quantity,
            estimated_price=price,
            store="通用",
            priority="必买"
        )
        party.add_shopping_item(item)
        console.print(f"[green]✓ 已添加：{name} x{quantity} = ¥{price * quantity:.0f}[/green]")
        return item

    @staticmethod
    def quick_mark_task(party):
        """快速标记任务完成"""
        if not party.checklist_phases:
            console.print("[yellow]还没有检查清单[/yellow]")
            return

        # 显示未完成的重要任务
        console.print("\n[bold]未完成的重要任务：[/bold]")
        important_tasks = []

        for phase in party.checklist_phases:
            for item in phase.items:
                if not item.completed and hasattr(item, 'priority') and item.priority == "重要":
                    important_tasks.append((phase, item))

        if not important_tasks:
            console.print("[green]所有重要任务已完成！[/green]")
            return

        for i, (phase, item) in enumerate(important_tasks[:10], 1):
            console.print(f"  {i}. [{phase.name}] {item.title}")

        try:
            choice = int(console.input("\n选择要完成的任务（输入序号）: ").strip())
            if 1 <= choice <= len(important_tasks):
                phase, item = important_tasks[choice - 1]
                item.completed = True
                console.print(f"[green]✓ 已完成：{item.title}[/green]")
        except:
            console.print("[red]✗ 无效选择[/red]")
