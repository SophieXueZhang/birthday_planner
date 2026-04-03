#!/usr/bin/env python3
"""
生日派对计划工具 - 主程序
"""
import os
import sys
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich import box
from rich.layout import Layout
from rich.text import Text

from models import Party, Guest, ShoppingItem
from invitation import InvitationGenerator
from shopping_suggestions import ShoppingSuggestions
from checklist import PartyChecklist, ChecklistPhase


console = Console()


class BirthdayPlannerApp:
    """生日派对计划应用"""

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.current_party: Optional[Party] = None

    def show_banner(self):
        """显示欢迎横幅"""
        banner = """
[bold magenta]
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🎉  生日派对计划工具  🎂                          ║
║                                                           ║
║        让每个孩子的生日都充满欢乐！                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
[/bold magenta]
"""
        console.print(banner)

    def main_menu(self):
        """主菜单"""
        while True:
            console.print("\n[bold cyan]主菜单[/bold cyan]")
            console.print("1. 创建新的派对计划")
            console.print("2. 加载现有派对计划")
            console.print("3. 退出")

            choice = Prompt.ask("请选择", choices=["1", "2", "3"])

            if choice == "1":
                self.create_new_party()
            elif choice == "2":
                self.load_party()
            elif choice == "3":
                console.print("[yellow]再见！祝派对顺利！[/yellow]")
                sys.exit(0)

    def create_new_party(self):
        """创建新派对"""
        console.print("\n[bold green]创建新的派对计划[/bold green]\n")

        # 收集基本信息
        child_name = Prompt.ask("孩子的名字")
        child_age = IntPrompt.ask("孩子的年龄")
        party_date = Prompt.ask("派对日期 (YYYY-MM-DD)")
        party_time = Prompt.ask("派对时间 (HH:MM)", default="14:00")
        venue = Prompt.ask("场地名称")
        venue_address = Prompt.ask("场地地址")
        budget = FloatPrompt.ask("预算（元）")
        theme = Prompt.ask("派对主题（可选，直接回车跳过）", default="")
        guest_count = IntPrompt.ask("预计客人数量")

        # 生成唯一ID
        party_id = f"party_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 创建派对对象
        self.current_party = Party(
            id=party_id,
            child_name=child_name,
            child_age=child_age,
            party_date=party_date,
            party_time=party_time,
            venue=venue,
            venue_address=venue_address,
            budget=budget,
            theme=theme,
            guest_count_expected=guest_count
        )

        # 自动生成购物建议
        if Confirm.ask("\n要自动生成购物清单建议吗？"):
            self.generate_shopping_suggestions()

        self.save_party()
        console.print(f"\n[green]✓ 派对计划已创建！[/green]")
        self.party_menu()

    def generate_shopping_suggestions(self):
        """生成购物建议"""
        if not self.current_party:
            return

        console.print("\n[cyan]正在生成购物建议...[/cyan]")

        # 生成基本物品
        items = ShoppingSuggestions.generate_basic_items(
            self.current_party.guest_count_expected,
            self.current_party.budget / max(self.current_party.guest_count_expected, 1)
        )

        # 添加主题物品
        if self.current_party.theme:
            themed_items = ShoppingSuggestions.generate_themed_items(self.current_party.theme)
            items.extend(themed_items)

        # 添加年龄适合的物品
        age_items = ShoppingSuggestions.generate_age_appropriate_items(self.current_party.child_age)
        items.extend(age_items)

        # 根据预算优化
        items = ShoppingSuggestions.optimize_budget(items, self.current_party.budget)

        # 添加到派对
        for item in items:
            self.current_party.add_shopping_item(item)

        console.print(f"[green]✓ 已生成 {len(items)} 项购物建议[/green]")

    def load_party(self):
        """加载现有派对"""
        files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]

        if not files:
            console.print("[yellow]没有找到已保存的派对计划[/yellow]")
            return

        console.print("\n[bold cyan]已保存的派对：[/bold cyan]")
        for i, file in enumerate(files, 1):
            console.print(f"{i}. {file[:-5]}")

        choice = IntPrompt.ask("选择要加载的派对（输入序号）", default=1)
        if 1 <= choice <= len(files):
            filepath = os.path.join(self.data_dir, files[choice - 1])
            self.current_party = Party.load_from_file(filepath)
            console.print(f"[green]✓ 已加载派对：{self.current_party.child_name} 的生日派对[/green]")
            self.party_menu()
        else:
            console.print("[red]无效的选择[/red]")

    def save_party(self):
        """保存派对"""
        if self.current_party:
            filepath = os.path.join(self.data_dir, f"{self.current_party.id}.json")
            self.current_party.save_to_file(filepath)

    def party_menu(self):
        """派对管理菜单"""
        while True:
            self.show_party_overview()

            console.print("\n[bold cyan]派对管理[/bold cyan]")
            console.print("1. 管理客人名单")
            console.print("2. 管理购物清单")
            console.print("3. 派对检查清单")
            console.print("4. 生成邀请函")
            console.print("5. 查看预算状态")
            console.print("6. 保存并返回主菜单")

            choice = Prompt.ask("请选择", choices=["1", "2", "3", "4", "5", "6"])

            if choice == "1":
                self.manage_guests()
            elif choice == "2":
                self.manage_shopping_list()
            elif choice == "3":
                self.manage_checklist()
            elif choice == "4":
                self.generate_invitations()
            elif choice == "5":
                self.show_budget_status()
            elif choice == "6":
                self.save_party()
                console.print("[green]✓ 已保存[/green]")
                break

    def show_party_overview(self):
        """显示派对概览"""
        if not self.current_party:
            return

        party = self.current_party

        # RSVP统计
        pending_count = sum(1 for g in party.guests if g.rsvp_status == "pending")
        confirmed_count = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
        declined_count = sum(1 for g in party.guests if g.rsvp_status == "declined")
        total_attendees = party.get_confirmed_guests_count()

        overview = f"""
[bold cyan]派对概览[/bold cyan]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
小寿星：{party.child_name} ({party.child_age} 岁)
日期：{party.party_date} {party.party_time}
场地：{party.venue}
主题：{party.theme if party.theme else '无'}
预算：¥{party.budget:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[bold yellow]客人统计：[/bold yellow]
  总邀请：{len(party.guests)} 人
  [green]✓ 已确认：{confirmed_count} 人（含+1共 {total_attendees} 人）[/green]
  [yellow]⏳ 待确认：{pending_count} 人[/yellow]
  [red]✗ 已拒绝：{declined_count} 人[/red]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
购物项：{len(party.shopping_list)} 项
预估花费：¥{party.get_total_estimated_cost():.2f}
实际花费：¥{party.get_total_actual_cost():.2f}
剩余预算：¥{party.get_budget_remaining():.2f}
"""
        console.print(Panel(overview, border_style="cyan"))

    def manage_guests(self):
        """管理客人"""
        while True:
            console.print("\n[bold cyan]客人管理[/bold cyan]")
            console.print("1. 添加客人")
            console.print("2. 查看客人列表")
            console.print("3. 更新RSVP状态")
            console.print("4. 删除客人")
            console.print("5. 返回")

            choice = Prompt.ask("请选择", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self.add_guest()
            elif choice == "2":
                self.show_guests()
            elif choice == "3":
                self.update_rsvp()
            elif choice == "4":
                self.remove_guest()
            elif choice == "5":
                break

    def add_guest(self):
        """添加客人"""
        console.print("\n[bold green]添加客人[/bold green]")
        name = Prompt.ask("客人姓名")
        contact = Prompt.ask("联系方式")
        plus_ones = IntPrompt.ask("额外带几个人", default=0)
        dietary = Prompt.ask("饮食限制（可选）", default="")
        notes = Prompt.ask("备注（可选）", default="")

        guest = Guest(
            name=name,
            contact=contact,
            plus_ones=plus_ones,
            dietary_restrictions=dietary,
            notes=notes
        )

        self.current_party.add_guest(guest)
        console.print(f"[green]✓ 已添加客人：{name}[/green]")

    def show_guests(self):
        """显示客人列表"""
        if not self.current_party.guests:
            console.print("[yellow]还没有添加客人[/yellow]")
            return

        table = Table(title="客人列表", box=box.ROUNDED)
        table.add_column("姓名", style="cyan")
        table.add_column("联系方式", style="white")
        table.add_column("RSVP", style="yellow")
        table.add_column("+人数", style="magenta")
        table.add_column("饮食限制", style="green")
        table.add_column("备注", style="blue")

        for guest in self.current_party.guests:
            status_color = {
                "pending": "[yellow]待确认[/yellow]",
                "confirmed": "[green]已确认[/green]",
                "declined": "[red]已拒绝[/red]"
            }
            table.add_row(
                guest.name,
                guest.contact,
                status_color.get(guest.rsvp_status, guest.rsvp_status),
                str(guest.plus_ones),
                guest.dietary_restrictions,
                guest.notes
            )

        console.print(table)

    def update_rsvp(self):
        """更新RSVP状态"""
        if not self.current_party.guests:
            console.print("[yellow]还没有添加客人[/yellow]")
            return

        self.show_guests()
        name = Prompt.ask("\n要更新哪位客人的状态？（输入姓名）")
        guest = self.current_party.get_guest(name)

        if not guest:
            console.print("[red]找不到该客人[/red]")
            return

        console.print(f"\n更新 {name} 的状态")
        status = Prompt.ask("状态", choices=["pending", "confirmed", "declined"], default=guest.rsvp_status)
        guest.rsvp_status = status

        if status == "confirmed":
            plus_ones = IntPrompt.ask("额外带几个人", default=guest.plus_ones)
            guest.plus_ones = plus_ones

        console.print(f"[green]✓ 已更新 {name} 的状态[/green]")

    def remove_guest(self):
        """删除客人"""
        if not self.current_party.guests:
            console.print("[yellow]还没有添加客人[/yellow]")
            return

        self.show_guests()
        name = Prompt.ask("\n要删除哪位客人？（输入姓名）")

        if Confirm.ask(f"确定要删除 {name} 吗？"):
            self.current_party.remove_guest(name)
            console.print(f"[green]✓ 已删除客人：{name}[/green]")

    def manage_shopping_list(self):
        """管理购物清单"""
        while True:
            console.print("\n[bold cyan]购物清单管理[/bold cyan]")
            console.print("1. 添加购物项")
            console.print("2. 查看购物清单")
            console.print("3. 标记为已购买")
            console.print("4. 删除购物项")
            console.print("5. 按类别查看")
            console.print("6. 按商店查看（采购路线）")
            console.print("7. 按优先级查看")
            console.print("8. 返回")

            choice = Prompt.ask("请选择", choices=["1", "2", "3", "4", "5", "6", "7", "8"])

            if choice == "1":
                self.add_shopping_item()
            elif choice == "2":
                self.show_shopping_list()
            elif choice == "3":
                self.mark_as_purchased()
            elif choice == "4":
                self.remove_shopping_item()
            elif choice == "5":
                self.show_by_category()
            elif choice == "6":
                self.show_by_store()
            elif choice == "7":
                self.show_by_priority()
            elif choice == "8":
                break

    def add_shopping_item(self):
        """添加购物项"""
        console.print("\n[bold green]添加购物项[/bold green]")
        name = Prompt.ask("物品名称")
        category = Prompt.ask("类别", default="其他")
        quantity = IntPrompt.ask("数量", default=1)
        estimated_price = FloatPrompt.ask("预估单价（元）", default=0.0)
        notes = Prompt.ask("备注（可选）", default="")

        item = ShoppingItem(
            name=name,
            category=category,
            quantity=quantity,
            estimated_price=estimated_price,
            notes=notes
        )

        self.current_party.add_shopping_item(item)
        console.print(f"[green]✓ 已添加：{name}[/green]")

    def show_shopping_list(self, items=None):
        """显示购物清单"""
        if items is None:
            items = self.current_party.shopping_list

        if not items:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        table = Table(title="购物清单", box=box.ROUNDED)
        table.add_column("物品", style="cyan")
        table.add_column("类别", style="magenta")
        table.add_column("数量", style="yellow")
        table.add_column("预估单价", style="green")
        table.add_column("预估总价", style="green")
        table.add_column("实际单价", style="blue")
        table.add_column("实际总价", style="blue")
        table.add_column("状态", style="white")
        table.add_column("备注", style="white")

        for item in items:
            status = "[green]✓ 已购买[/green]" if item.purchased else "[yellow]待购买[/yellow]"
            table.add_row(
                item.name,
                item.category,
                str(item.quantity),
                f"¥{item.estimated_price:.2f}",
                f"¥{item.estimated_price * item.quantity:.2f}",
                f"¥{item.actual_price:.2f}" if item.actual_price > 0 else "-",
                f"¥{item.actual_price * item.quantity:.2f}" if item.actual_price > 0 else "-",
                status,
                item.notes
            )

        console.print(table)

        # 统计信息
        total_estimated = sum(item.estimated_price * item.quantity for item in items)
        total_actual = sum(item.actual_price * item.quantity for item in items if item.purchased)
        purchased_count = sum(1 for item in items if item.purchased)

        console.print(f"\n[cyan]统计：共 {len(items)} 项，已购买 {purchased_count} 项[/cyan]")
        console.print(f"[green]预估总额：¥{total_estimated:.2f}[/green]")
        console.print(f"[blue]实际花费：¥{total_actual:.2f}[/blue]")

    def mark_as_purchased(self):
        """标记为已购买"""
        if not self.current_party.shopping_list:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        self.show_shopping_list()
        name = Prompt.ask("\n要标记哪个物品？（输入名称）")

        for item in self.current_party.shopping_list:
            if item.name == name:
                if item.purchased:
                    console.print("[yellow]该物品已经标记为已购买[/yellow]")
                    return

                item.purchased = True
                actual_price = FloatPrompt.ask("实际单价（元）", default=item.estimated_price)
                item.actual_price = actual_price
                console.print(f"[green]✓ 已标记 {name} 为已购买[/green]")
                return

        console.print("[red]找不到该物品[/red]")

    def remove_shopping_item(self):
        """删除购物项"""
        if not self.current_party.shopping_list:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        self.show_shopping_list()
        name = Prompt.ask("\n要删除哪个物品？（输入名称）")

        if Confirm.ask(f"确定要删除 {name} 吗？"):
            self.current_party.remove_shopping_item(name)
            console.print(f"[green]✓ 已删除：{name}[/green]")

    def show_by_category(self):
        """按类别显示"""
        if not self.current_party.shopping_list:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        categories = {}
        for item in self.current_party.shopping_list:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)

        for category, items in categories.items():
            console.print(f"\n[bold magenta]--- {category} ---[/bold magenta]")
            self.show_shopping_list(items)

    def generate_invitations(self):
        """生成邀请函"""
        if not self.current_party.guests:
            console.print("[yellow]还没有添加客人，无法生成邀请函[/yellow]")
            return

        console.print("\n[bold cyan]生成邀请函[/bold cyan]")
        console.print("1. 生成所有客人的邀请函（文本格式）")
        console.print("2. 生成所有客人的邀请函（HTML格式）")
        console.print("3. 生成单个客人的邀请函")
        console.print("4. 返回")

        choice = Prompt.ask("请选择", choices=["1", "2", "3", "4"])

        if choice == "4":
            return

        inv_dir = os.path.join(self.data_dir, f"invitations_{self.current_party.id}")
        os.makedirs(inv_dir, exist_ok=True)

        if choice == "1":
            # 文本格式
            for guest in self.current_party.guests:
                invitation = InvitationGenerator.generate_text_invitation(self.current_party, guest)
                filepath = os.path.join(inv_dir, f"{guest.name}_invitation.txt")
                InvitationGenerator.save_invitation(invitation, filepath)

            console.print(f"[green]✓ 已生成 {len(self.current_party.guests)} 份文本邀请函[/green]")
            console.print(f"[cyan]保存位置：{inv_dir}[/cyan]")

        elif choice == "2":
            # HTML格式
            for guest in self.current_party.guests:
                invitation = InvitationGenerator.generate_html_invitation(self.current_party, guest)
                filepath = os.path.join(inv_dir, f"{guest.name}_invitation.html")
                InvitationGenerator.save_invitation(invitation, filepath)

            console.print(f"[green]✓ 已生成 {len(self.current_party.guests)} 份HTML邀请函[/green]")
            console.print(f"[cyan]保存位置：{inv_dir}[/cyan]")

        elif choice == "3":
            # 单个客人
            self.show_guests()
            name = Prompt.ask("\n要为哪位客人生成邀请函？（输入姓名）")
            guest = self.current_party.get_guest(name)

            if not guest:
                console.print("[red]找不到该客人[/red]")
                return

            format_choice = Prompt.ask("选择格式", choices=["text", "html"])

            if format_choice == "text":
                invitation = InvitationGenerator.generate_text_invitation(self.current_party, guest)
                filepath = os.path.join(inv_dir, f"{guest.name}_invitation.txt")
            else:
                invitation = InvitationGenerator.generate_html_invitation(self.current_party, guest)
                filepath = os.path.join(inv_dir, f"{guest.name}_invitation.html")

            InvitationGenerator.save_invitation(invitation, filepath)
            console.print(f"[green]✓ 已生成邀请函[/green]")
            console.print(f"[cyan]保存位置：{filepath}[/cyan]")

            # 显示预览
            if Confirm.ask("要查看预览吗？"):
                console.print("\n" + "=" * 60)
                console.print(invitation)
                console.print("=" * 60)

    def show_budget_status(self):
        """显示预算状态"""
        party = self.current_party

        table = Table(title="预算状态", box=box.DOUBLE)
        table.add_column("项目", style="cyan")
        table.add_column("金额", style="yellow", justify="right")

        table.add_row("总预算", f"¥{party.budget:.2f}")
        table.add_row("预估花费", f"¥{party.get_total_estimated_cost():.2f}")
        table.add_row("实际花费", f"¥{party.get_total_actual_cost():.2f}")
        table.add_row("剩余预算", f"¥{party.get_budget_remaining():.2f}")

        console.print(table)

        # 预算警告
        remaining = party.get_budget_remaining()
        if remaining < 0:
            console.print("\n[bold red]⚠ 警告：预算已超支！[/bold red]")
        elif remaining < party.budget * 0.1:
            console.print("\n[bold yellow]⚠ 注意：预算即将用完[/bold yellow]")
        else:
            console.print("\n[bold green]✓ 预算充足[/bold green]")

        # 按类别显示花费
        if party.shopping_list:
            console.print("\n[bold cyan]各类别花费：[/bold cyan]")
            categories = {}
            for item in party.shopping_list:
                if item.category not in categories:
                    categories[item.category] = {"estimated": 0, "actual": 0}
                categories[item.category]["estimated"] += item.estimated_price * item.quantity
                if item.purchased:
                    categories[item.category]["actual"] += item.actual_price * item.quantity

            cat_table = Table(box=box.SIMPLE)
            cat_table.add_column("类别", style="magenta")
            cat_table.add_column("预估", style="green", justify="right")
            cat_table.add_column("实际", style="blue", justify="right")

            for category, amounts in sorted(categories.items()):
                cat_table.add_row(
                    category,
                    f"¥{amounts['estimated']:.2f}",
                    f"¥{amounts['actual']:.2f}"
                )

            console.print(cat_table)

    def show_by_store(self):
        """按商店分组显示购物清单"""
        if not self.current_party.shopping_list:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        stores = {}
        for item in self.current_party.shopping_list:
            if item.store not in stores:
                stores[item.store] = []
            stores[item.store].append(item)

        # 按商店显示
        for store, items in sorted(stores.items()):
            console.print(f"\n[bold magenta]━━━ 📍 {store} ━━━[/bold magenta]")

            table = Table(box=box.SIMPLE)
            table.add_column("物品", style="cyan")
            table.add_column("数量", style="yellow")
            table.add_column("优先级", style="white")
            table.add_column("预估", style="green", justify="right")
            table.add_column("状态", style="white")

            store_total = 0
            for item in items:
                status = "✓" if item.purchased else "□"
                priority_color = {
                    "必买": "[bold red]必买[/bold red]",
                    "推荐": "[yellow]推荐[/yellow]",
                    "可选": "[dim]可选[/dim]"
                }
                table.add_row(
                    item.name,
                    str(item.quantity),
                    priority_color.get(item.priority, item.priority),
                    f"¥{item.estimated_price * item.quantity:.2f}",
                    status
                )
                if not item.purchased:
                    store_total += item.estimated_price * item.quantity

            console.print(table)
            console.print(f"[cyan]该店预估花费：¥{store_total:.2f}[/cyan]")

    def show_by_priority(self):
        """按优先级显示购物清单"""
        if not self.current_party.shopping_list:
            console.print("[yellow]购物清单为空[/yellow]")
            return

        priorities = {"必买": [], "推荐": [], "可选": []}
        for item in self.current_party.shopping_list:
            if item.priority in priorities:
                priorities[item.priority].append(item)
            else:
                priorities.setdefault("其他", []).append(item)

        # 按优先级显示
        priority_order = ["必买", "推荐", "可选", "其他"]
        for priority in priority_order:
            if priority not in priorities or not priorities[priority]:
                continue

            items = priorities[priority]
            console.print(f"\n[bold magenta]━━━ {priority} ━━━[/bold magenta]")

            table = Table(box=box.SIMPLE)
            table.add_column("物品", style="cyan")
            table.add_column("商店", style="yellow")
            table.add_column("数量", style="white")
            table.add_column("预估", style="green", justify="right")
            table.add_column("状态", style="white")

            for item in items:
                status = "[green]✓ 已购买[/green]" if item.purchased else "[yellow]待购买[/yellow]"
                table.add_row(
                    item.name,
                    item.store,
                    str(item.quantity),
                    f"¥{item.estimated_price * item.quantity:.2f}",
                    status
                )

            console.print(table)

    def manage_checklist(self):
        """管理派对检查清单"""
        # 如果没有检查清单数据，生成标准清单
        if not self.current_party.checklist_data:
            phases = PartyChecklist.generate_standard_checklist(
                self.current_party.child_age,
                self.current_party.guest_count_expected
            )
            self.current_party.checklist_data = {
                "phases": [phase.to_dict() for phase in phases]
            }

        while True:
            console.print("\n[bold cyan]派对检查清单[/bold cyan]")
            console.print("1. 查看完整清单")
            console.print("2. 查看当前阶段任务")
            console.print("3. 标记任务完成")
            console.print("4. 查看紧急待办")
            console.print("5. 返回")

            choice = Prompt.ask("请选择", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self.show_full_checklist()
            elif choice == "2":
                self.show_current_phase()
            elif choice == "3":
                self.mark_checklist_item()
            elif choice == "4":
                self.show_urgent_items()
            elif choice == "5":
                break

    def show_full_checklist(self):
        """显示完整检查清单"""
        phases = [ChecklistPhase.from_dict(p) for p in self.current_party.checklist_data.get("phases", [])]

        if not phases:
            console.print("[yellow]没有检查清单[/yellow]")
            return

        total_progress = PartyChecklist.overall_progress(phases)
        console.print(f"\n[bold cyan]整体进度：{total_progress:.1f}%[/bold cyan]\n")

        for phase in phases:
            deadline = phase.get_deadline(self.current_party.party_date)
            is_overdue = phase.is_overdue(self.current_party.party_date)
            progress = phase.completion_rate()

            # 标题
            title = f"{phase.name} (截止：{deadline})"
            if is_overdue:
                title += " ⚠️ 已过期"

            console.print(f"\n[bold yellow]{title}[/bold yellow]")
            console.print(f"完成度：{progress:.0f}%")

            # 任务列表
            for item in phase.items:
                status = "[green]✓[/green]" if item.completed else "[dim]□[/dim]"
                console.print(f"  {status} {item.title}")
                if item.notes:
                    console.print(f"     [dim]{item.notes}[/dim]")

    def show_current_phase(self):
        """显示当前阶段任务"""
        phases = [ChecklistPhase.from_dict(p) for p in self.current_party.checklist_data.get("phases", [])]

        if not phases:
            console.print("[yellow]没有检查清单[/yellow]")
            return

        current = PartyChecklist.get_current_phase(phases, self.current_party.party_date)

        if not current:
            console.print("[yellow]无当前阶段[/yellow]")
            return

        console.print(f"\n[bold cyan]当前阶段：{current.name}[/bold cyan]")
        console.print(f"完成度：{current.completion_rate():.0f}%\n")

        for item in current.items:
            status = "[green]✓[/green]" if item.completed else "[yellow]□[/yellow]"
            console.print(f"  {status} {item.title}")
            if item.notes:
                console.print(f"     [dim]{item.notes}[/dim]")

    def mark_checklist_item(self):
        """标记检查清单项为完成"""
        phases = [ChecklistPhase.from_dict(p) for p in self.current_party.checklist_data.get("phases", [])]

        if not phases:
            console.print("[yellow]没有检查清单[/yellow]")
            return

        # 显示所有未完成的任务
        console.print("\n[bold cyan]未完成的任务：[/bold cyan]\n")
        uncompleted = []
        index = 1
        for phase in phases:
            for item in phase.items:
                if not item.completed:
                    console.print(f"{index}. [{phase.name}] {item.title}")
                    uncompleted.append((phase, item))
                    index += 1

        if not uncompleted:
            console.print("[green]所有任务已完成！[/green]")
            return

        choice = IntPrompt.ask("\n选择要标记完成的任务（输入序号）", default=1)

        if 1 <= choice <= len(uncompleted):
            phase, item = uncompleted[choice - 1]
            item.completed = True

            # 保存更新
            self.current_party.checklist_data["phases"] = [p.to_dict() for p in phases]

            console.print(f"[green]✓ 已完成：{item.title}[/green]")
        else:
            console.print("[red]无效的选择[/red]")

    def show_urgent_items(self):
        """显示紧急待办事项"""
        phases = [ChecklistPhase.from_dict(p) for p in self.current_party.checklist_data.get("phases", [])]

        if not phases:
            console.print("[yellow]没有检查清单[/yellow]")
            return

        urgent = PartyChecklist.get_urgent_items(phases, self.current_party.party_date)

        if not urgent:
            console.print("[green]没有紧急待办事项！[/green]")
            return

        console.print(f"\n[bold red]⚠️  紧急待办事项（{len(urgent)}项）[/bold red]\n")

        for phase, item in urgent:
            console.print(f"[yellow]• [{phase.name}] {item.title}[/yellow]")
            if item.notes:
                console.print(f"  [dim]{item.notes}[/dim]")

    def run(self):
        """运行应用"""
        self.show_banner()
        self.main_menu()


if __name__ == "__main__":
    app = BirthdayPlannerApp()
    app.run()
