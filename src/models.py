"""
数据模型定义
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class Guest:
    """客人信息"""
    name: str
    contact: str  # 联系方式（电话或邮箱）
    rsvp_status: str = "pending"  # pending, confirmed, declined
    plus_ones: int = 0  # 额外带几个人
    dietary_restrictions: str = ""  # 饮食限制
    notes: str = ""  # 备注

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class ShoppingItem:
    """购物清单项"""
    name: str
    category: str  # 装饰、食物、礼物、用品等
    quantity: int = 1
    estimated_price: float = 0.0
    actual_price: float = 0.0
    purchased: bool = False
    notes: str = ""
    store: str = "通用"  # 推荐购买的商店
    priority: str = "必买"  # 必买、推荐、可选

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Party:
    """派对信息"""
    id: str
    child_name: str
    child_age: int
    party_date: str  # YYYY-MM-DD
    party_time: str  # HH:MM
    venue: str
    venue_address: str
    budget: float
    theme: str = ""
    guest_count_expected: int = 0
    guests: List[Guest] = field(default_factory=list)
    shopping_list: List[ShoppingItem] = field(default_factory=list)
    checklist_data: dict = field(default_factory=dict)  # 存储检查清单数据
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_guest(self, guest: Guest):
        """添加客人"""
        self.guests.append(guest)

    def remove_guest(self, guest_name: str):
        """移除客人"""
        self.guests = [g for g in self.guests if g.name != guest_name]

    def get_guest(self, guest_name: str) -> Optional[Guest]:
        """获取客人信息"""
        for guest in self.guests:
            if guest.name == guest_name:
                return guest
        return None

    def add_shopping_item(self, item: ShoppingItem):
        """添加购物项"""
        self.shopping_list.append(item)

    def remove_shopping_item(self, item_name: str):
        """移除购物项"""
        self.shopping_list = [item for item in self.shopping_list if item.name != item_name]

    def get_total_estimated_cost(self) -> float:
        """获取预估总成本"""
        return sum(item.estimated_price * item.quantity for item in self.shopping_list)

    def get_total_actual_cost(self) -> float:
        """获取实际总成本"""
        return sum(item.actual_price * item.quantity for item in self.shopping_list if item.purchased)

    def get_confirmed_guests_count(self) -> int:
        """获取确认参加的客人数量"""
        confirmed = sum(1 + g.plus_ones for g in self.guests if g.rsvp_status == "confirmed")
        return confirmed

    def get_budget_remaining(self) -> float:
        """获取剩余预算"""
        return self.budget - self.get_total_actual_cost()

    def to_dict(self):
        """转换为字典"""
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data):
        """从字典创建对象"""
        guests = [Guest.from_dict(g) for g in data.get('guests', [])]
        shopping_list = [ShoppingItem.from_dict(item) for item in data.get('shopping_list', [])]
        data['guests'] = guests
        data['shopping_list'] = shopping_list
        return cls(**data)

    def save_to_file(self, filepath: str):
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str):
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
