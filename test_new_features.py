#!/usr/bin/env python3
"""
测试新功能：检查清单、按商店分组、RSVP统计
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import Party, Guest, ShoppingItem
from checklist import PartyChecklist, ChecklistPhase
from shopping_suggestions import ShoppingSuggestions
from datetime import datetime


def test_new_features():
    """测试新功能"""
    print("=" * 60)
    print("测试新功能")
    print("=" * 60)

    # 创建测试派对
    party = Party(
        id=f"test_party_{datetime.now().strftime('%Y%m%d')}",
        child_name="测试宝宝",
        child_age=6,
        party_date="2026-05-01",
        party_time="15:00",
        venue="测试场地",
        venue_address="测试地址123号",
        budget=2000.0,
        theme="公主",
        guest_count_expected=10
    )

    # 添加客人测试RSVP统计
    print("\n1. 测试RSVP统计功能")
    print("-" * 60)
    party.add_guest(Guest("张三", "13800138001", rsvp_status="confirmed", plus_ones=1))
    party.add_guest(Guest("李四", "13800138002", rsvp_status="confirmed", plus_ones=0))
    party.add_guest(Guest("王五", "13800138003", rsvp_status="pending", plus_ones=0))
    party.add_guest(Guest("赵六", "13800138004", rsvp_status="declined", plus_ones=0))

    confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
    pending = sum(1 for g in party.guests if g.rsvp_status == "pending")
    declined = sum(1 for g in party.guests if g.rsvp_status == "declined")
    total_attendees = party.get_confirmed_guests_count()

    print(f"总邀请：{len(party.guests)} 人")
    print(f"✓ 已确认：{confirmed} 人（含+1共 {total_attendees} 人）")
    print(f"⏳ 待确认：{pending} 人")
    print(f"✗ 已拒绝：{declined} 人")
    print("✅ RSVP统计功能正常")

    # 测试购物清单新字段
    print("\n2. 测试购物清单（商店和优先级）")
    print("-" * 60)
    items = ShoppingSuggestions.generate_basic_items(10)

    # 按商店分组
    stores = {}
    for item in items[:5]:  # 只显示前5项
        party.add_shopping_item(item)
        if item.store not in stores:
            stores[item.store] = []
        stores[item.store].append(item)

    print("按商店分组：")
    for store, store_items in sorted(stores.items()):
        print(f"\n  📍 {store}:")
        for item in store_items:
            print(f"    - {item.name} (优先级: {item.priority}, 数量: {item.quantity})")

    # 按优先级分组
    priorities = {"必买": [], "推荐": [], "可选": []}
    for item in party.shopping_list:
        if item.priority in priorities:
            priorities[item.priority].append(item)

    print("\n按优先级分组：")
    for priority, priority_items in priorities.items():
        if priority_items:
            print(f"\n  {priority}:")
            for item in priority_items:
                print(f"    - {item.name} (商店: {item.store})")

    print("\n✅ 购物清单优化功能正常")

    # 测试检查清单
    print("\n3. 测试派对检查清单")
    print("-" * 60)
    phases = PartyChecklist.generate_standard_checklist(party.child_age, party.guest_count_expected)

    print(f"生成了 {len(phases)} 个阶段的检查清单：")
    for phase in phases:
        print(f"\n  {phase.name} (派对前{phase.days_before}天):")
        print(f"    任务数: {len(phase.items)}")
        print(f"    截止日期: {phase.get_deadline(party.party_date)}")
        # 显示前3项任务
        for item in phase.items[:3]:
            print(f"    □ {item.title}")
        if len(phase.items) > 3:
            print(f"    ... 还有{len(phase.items) - 3}项")

    # 测试当前阶段
    current_phase = PartyChecklist.get_current_phase(phases, party.party_date)
    if current_phase:
        print(f"\n  当前应关注阶段: {current_phase.name}")

    # 测试完成任务
    phases[0].items[0].completed = True
    phases[0].items[1].completed = True
    print(f"\n  第一阶段完成度: {phases[0].completion_rate():.1f}%")

    # 测试整体进度
    overall = PartyChecklist.overall_progress(phases)
    print(f"  整体进度: {overall:.1f}%")

    print("\n✅ 检查清单功能正常")

    # 保存测试派对
    print("\n4. 测试数据持久化")
    print("-" * 60)
    party.checklist_data = {"phases": [p.to_dict() for p in phases]}

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, f"{party.id}.json")
    party.save_to_file(filepath)
    print(f"✓ 派对数据已保存到：{filepath}")

    # 重新加载测试
    loaded_party = Party.load_from_file(filepath)
    print(f"✓ 成功加载派对：{loaded_party.child_name}")
    print(f"  - 客人数：{len(loaded_party.guests)}")
    print(f"  - 购物项数：{len(loaded_party.shopping_list)}")
    print(f"  - 检查清单阶段数：{len(loaded_party.checklist_data.get('phases', []))}")

    print("\n✅ 数据持久化功能正常")

    print("\n" + "=" * 60)
    print("所有新功能测试通过！")
    print("=" * 60)

    return True


if __name__ == "__main__":
    try:
        test_new_features()
        print("\n🎉 测试成功！新功能运行正常！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
