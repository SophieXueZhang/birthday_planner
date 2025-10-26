#!/usr/bin/env python3
"""
示例测试脚本 - 演示如何创建派对计划
"""
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import Party, Guest, ShoppingItem
from invitation import InvitationGenerator
from shopping_suggestions import ShoppingSuggestions
from datetime import datetime


def create_example_party():
    """创建一个示例派对"""
    print("创建示例派对...")

    # 创建派对
    party = Party(
        id=f"example_party_{datetime.now().strftime('%Y%m%d')}",
        child_name="小明",
        child_age=8,
        party_date="2025-11-15",
        party_time="14:00",
        venue="欢乐儿童乐园",
        venue_address="北京市朝阳区欢乐街123号",
        budget=3000.0,
        theme="超级英雄",
        guest_count_expected=15
    )

    # 添加客人
    guests = [
        Guest("张三", "13800138001", plus_ones=1, rsvp_status="confirmed"),
        Guest("李四", "13800138002", plus_ones=0, rsvp_status="confirmed"),
        Guest("王五", "13800138003", plus_ones=2, rsvp_status="pending"),
        Guest("赵六", "13800138004", plus_ones=0, rsvp_status="declined"),
        Guest("孙七", "13800138005", dietary_restrictions="不吃海鲜", rsvp_status="confirmed"),
    ]

    for guest in guests:
        party.add_guest(guest)

    print(f"✓ 添加了 {len(guests)} 位客人")

    # 生成购物建议
    items = ShoppingSuggestions.generate_basic_items(15, 200)
    themed_items = ShoppingSuggestions.generate_themed_items("超级英雄")
    age_items = ShoppingSuggestions.generate_age_appropriate_items(8)

    all_items = items + themed_items + age_items
    optimized_items = ShoppingSuggestions.optimize_budget(all_items, party.budget)

    for item in optimized_items:
        party.add_shopping_item(item)

    print(f"✓ 添加了 {len(optimized_items)} 项购物清单")

    # 标记一些物品为已购买
    for i, item in enumerate(party.shopping_list[:5]):
        item.purchased = True
        item.actual_price = item.estimated_price * 0.95  # 实际价格稍低

    print(f"✓ 标记了 5 项为已购买")

    # 保存派对
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f"{party.id}.json")
    party.save_to_file(filepath)
    print(f"✓ 派对数据已保存到：{filepath}")

    # 生成邀请函示例
    inv_dir = os.path.join(data_dir, f"invitations_{party.id}")
    os.makedirs(inv_dir, exist_ok=True)

    # 生成文本邀请函
    for guest in party.guests[:2]:  # 只为前两位客人生成示例
        text_inv = InvitationGenerator.generate_text_invitation(party, guest)
        text_path = os.path.join(inv_dir, f"{guest.name}_invitation.txt")
        InvitationGenerator.save_invitation(text_inv, text_path)

        html_inv = InvitationGenerator.generate_html_invitation(party, guest)
        html_path = os.path.join(inv_dir, f"{guest.name}_invitation.html")
        InvitationGenerator.save_invitation(html_inv, html_path)

    print(f"✓ 生成了 2 份示例邀请函（文本和HTML格式）")
    print(f"  保存位置：{inv_dir}")

    # 显示派对概览
    print("\n" + "=" * 60)
    print("派对概览")
    print("=" * 60)
    print(f"小寿星：{party.child_name} ({party.child_age} 岁)")
    print(f"日期：{party.party_date} {party.party_time}")
    print(f"场地：{party.venue}")
    print(f"主题：{party.theme}")
    print(f"预算：¥{party.budget:.2f}")
    print(f"客人：{len(party.guests)} 人（确认：{party.get_confirmed_guests_count()}）")
    print(f"购物项：{len(party.shopping_list)} 项")
    print(f"预估花费：¥{party.get_total_estimated_cost():.2f}")
    print(f"实际花费：¥{party.get_total_actual_cost():.2f}")
    print(f"剩余预算：¥{party.get_budget_remaining():.2f}")
    print("=" * 60)

    print("\n示例派对创建完成！")
    print(f"您可以运行 'cd src && python3 main.py' 来加载这个派对并进行管理。")

    return party


if __name__ == "__main__":
    create_example_party()
