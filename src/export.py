"""
导出和打印功能模块
"""
from models import Party
from datetime import datetime


class PartyExporter:
    """派对数据导出器"""

    @staticmethod
    def export_guest_checkin_sheet(party: Party) -> str:
        """导出客人签到表（适合打印）"""
        output = []
        output.append("=" * 60)
        output.append(f"{party.child_name} 的生日派对 - 客人签到表")
        output.append("=" * 60)
        output.append(f"日期：{party.party_date} {party.party_time}")
        output.append(f"场地：{party.venue}")
        output.append("=" * 60)
        output.append("")

        # 只显示已确认的客人
        confirmed_guests = [g for g in party.guests if g.rsvp_status == "confirmed"]

        if not confirmed_guests:
            output.append("暂无确认参加的客人")
            return "\n".join(output)

        output.append(f"预计参加：{len(confirmed_guests)} 位客人")
        output.append("")
        output.append("-" * 60)

        for i, guest in enumerate(confirmed_guests, 1):
            output.append(f"{i}. {guest.name}")
            if guest.plus_ones > 0:
                output.append(f"   (+{guest.plus_ones}人)")
            if guest.dietary_restrictions:
                output.append(f"   饮食限制：{guest.dietary_restrictions}")
            output.append(f"   签到：□  到场时间：_______")
            output.append("")

        output.append("-" * 60)
        total_count = sum(1 + g.plus_ones for g in confirmed_guests)
        output.append(f"总计：{total_count} 人（含+1）")
        output.append("")
        output.append("备注：")
        output.append("_" * 60)
        output.append("_" * 60)

        return "\n".join(output)

    @staticmethod
    def export_shopping_list_simple(party: Party, by_store: bool = True) -> str:
        """导出简化购物清单（适合打印和手机查看）"""
        output = []
        output.append("=" * 60)
        output.append(f"{party.child_name} 的生日派对 - 购物清单")
        output.append("=" * 60)
        output.append(f"预算：¥{party.budget:.2f}")
        output.append("")

        if not party.shopping_list:
            output.append("购物清单为空")
            return "\n".join(output)

        # 只显示未购买的
        unpurchased = [item for item in party.shopping_list if not item.purchased]

        if not unpurchased:
            output.append("所有物品已购买！")
            return "\n".join(output)

        if by_store:
            # 按商店分组
            stores = {}
            for item in unpurchased:
                if item.store not in stores:
                    stores[item.store] = []
                stores[item.store].append(item)

            for store, items in sorted(stores.items()):
                output.append(f"【{store}】")
                output.append("-" * 60)
                for item in items:
                    priority_mark = "★" if item.priority == "必买" else "☆"
                    checkbox = "□"
                    output.append(f"  {checkbox} {item.name} x{item.quantity}  {priority_mark}")
                    output.append(f"     预估：¥{item.estimated_price * item.quantity:.2f}")
                    if item.notes:
                        output.append(f"     备注：{item.notes}")

                store_total = sum(i.estimated_price * i.quantity for i in items)
                output.append(f"     小计：¥{store_total:.2f}")
                output.append("")
        else:
            # 按优先级分组
            priorities = {"必买": [], "推荐": [], "可选": []}
            for item in unpurchased:
                if item.priority in priorities:
                    priorities[item.priority].append(item)

            for priority in ["必买", "推荐", "可选"]:
                if not priorities[priority]:
                    continue

                output.append(f"【{priority}】")
                output.append("-" * 60)
                for item in priorities[priority]:
                    checkbox = "□"
                    output.append(f"  {checkbox} {item.name} x{item.quantity} - {item.store}")
                    output.append(f"     预估：¥{item.estimated_price * item.quantity:.2f}")
                output.append("")

        total = sum(i.estimated_price * i.quantity for i in unpurchased)
        output.append("=" * 60)
        output.append(f"待购总额：¥{total:.2f}")
        output.append(f"剩余预算：¥{party.get_budget_remaining():.2f}")

        return "\n".join(output)

    @staticmethod
    def export_party_summary(party: Party) -> str:
        """导出派对完整总结"""
        output = []
        output.append("=" * 60)
        output.append(f"{party.child_name} 的 {party.child_age} 岁生日派对计划")
        output.append("=" * 60)
        output.append("")

        # 基本信息
        output.append("【基本信息】")
        output.append("-" * 60)
        output.append(f"小寿星：{party.child_name}")
        output.append(f"年龄：{party.child_age} 岁")
        output.append(f"日期：{party.party_date} {party.party_time}")

        # 计算倒计时
        try:
            party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
            days_until = (party_dt - datetime.now()).days
            if days_until > 0:
                output.append(f"倒计时：还有 {days_until} 天")
            elif days_until == 0:
                output.append("倒计时：就是今天！")
        except:
            pass

        output.append(f"场地：{party.venue}")
        output.append(f"地址：{party.venue_address}")
        if party.theme:
            output.append(f"主题：{party.theme}")
        output.append("")

        # 预算信息
        output.append("【预算情况】")
        output.append("-" * 60)
        output.append(f"总预算：¥{party.budget:.2f}")
        output.append(f"预估花费：¥{party.get_total_estimated_cost():.2f}")
        output.append(f"实际花费：¥{party.get_total_actual_cost():.2f}")
        output.append(f"剩余预算：¥{party.get_budget_remaining():.2f}")
        output.append("")

        # 客人统计
        output.append("【客人统计】")
        output.append("-" * 60)
        confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
        pending = sum(1 for g in party.guests if g.rsvp_status == "pending")
        declined = sum(1 for g in party.guests if g.rsvp_status == "declined")
        total_attendees = party.get_confirmed_guests_count()

        output.append(f"总邀请：{len(party.guests)} 人")
        output.append(f"已确认：{confirmed} 人（实际参加 {total_attendees} 人）")
        output.append(f"待确认：{pending} 人")
        output.append(f"已拒绝：{declined} 人")
        output.append("")

        # 购物进度
        output.append("【购物进度】")
        output.append("-" * 60)
        total_items = len(party.shopping_list)
        purchased_items = sum(1 for i in party.shopping_list if i.purchased)
        if total_items > 0:
            progress = purchased_items / total_items * 100
            output.append(f"总计：{total_items} 项")
            output.append(f"已购买：{purchased_items} 项")
            output.append(f"待购买：{total_items - purchased_items} 项")
            output.append(f"完成度：{progress:.1f}%")
        else:
            output.append("暂无购物清单")
        output.append("")

        if party.notes:
            output.append("【备注】")
            output.append("-" * 60)
            output.append(party.notes)
            output.append("")

        output.append("=" * 60)
        output.append(f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return "\n".join(output)

    @staticmethod
    def export_wechat_invitation(party: Party) -> str:
        """导出简短版邀请函（适合微信群发）"""
        lines = []
        lines.append(f"🎉 {party.child_name}的{party.child_age}岁生日派对邀请 🎉")
        lines.append("")
        lines.append(f"📅 时间：{party.party_date} {party.party_time}")
        lines.append(f"📍 地点：{party.venue}")
        if party.venue_address:
            lines.append(f"      {party.venue_address}")
        if party.theme:
            lines.append(f"🎨 主题：{party.theme}")
        lines.append("")
        lines.append("期待您的光临！")
        lines.append("请回复确认是否能参加 😊")

        return "\n".join(lines)

    @staticmethod
    def save_export(content: str, filepath: str):
        """保存导出内容到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
