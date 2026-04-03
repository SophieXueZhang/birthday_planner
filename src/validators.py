"""
数据验证模块
"""
from datetime import datetime
import re


class DataValidator:
    """数据验证器"""

    @staticmethod
    def validate_date(date_str: str) -> tuple[bool, str]:
        """
        验证日期格式和合理性
        返回：(是否有效, 错误消息)
        """
        if not date_str:
            return False, "日期不能为空"

        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return False, "日期格式错误，应为YYYY-MM-DD"

        # 检查是否是过去的日期
        if date_obj < datetime.now():
            return False, "⚠️ 警告：日期已过去，确定要继续吗？"

        # 检查是否太远（超过2年）
        days_until = (date_obj - datetime.now()).days
        if days_until > 730:  # 2年
            return False, f"日期太远了（{days_until}天后），确定没有输错吗？"

        return True, ""

    @staticmethod
    def validate_time(time_str: str) -> tuple[bool, str]:
        """验证时间格式"""
        if not time_str:
            return False, "时间不能为空"

        try:
            datetime.strptime(time_str, "%H:%M")
            return True, ""
        except ValueError:
            return False, "时间格式错误，应为HH:MM（如14:00）"

    @staticmethod
    def validate_budget(budget: float) -> tuple[bool, str]:
        """验证预算合理性"""
        if budget <= 0:
            return False, "预算必须大于0"

        if budget < 100:
            return False, "预算太少了（建议至少100元）"

        if budget > 100000:
            return False, "⚠️ 预算超过10万，确定吗？"

        return True, ""

    @staticmethod
    def validate_age(age: int) -> tuple[bool, str]:
        """验证年龄合理性"""
        if age <= 0:
            return False, "年龄必须大于0"

        if age > 18:
            return False, "这个工具主要为儿童派对设计（建议18岁以下）"

        return True, ""

    @staticmethod
    def validate_guest_count(count: int) -> tuple[bool, str]:
        """验证客人数量"""
        if count < 0:
            return False, "客人数量不能为负数"

        if count == 0:
            return False, "⚠️ 没有客人的派对？"

        if count > 100:
            return False, f"客人太多了（{count}人），确定吗？"

        return True, ""

    @staticmethod
    def validate_contact(contact: str) -> tuple[bool, str]:
        """验证联系方式（简单验证）"""
        if not contact:
            return False, "联系方式不能为空"

        # 简单的电话号码验证（11位数字）
        if contact.isdigit() and len(contact) == 11:
            return True, ""

        # 简单的邮箱验证
        if "@" in contact and "." in contact:
            return True, ""

        return False, "请输入有效的电话号码（11位）或邮箱地址"

    @staticmethod
    def validate_price(price: float, field_name: str = "价格") -> tuple[bool, str]:
        """验证价格"""
        if price < 0:
            return False, f"{field_name}不能为负数"

        if price > 10000:
            return False, f"⚠️ {field_name}超过1万，确定吗？"

        return True, ""

    @staticmethod
    def validate_quantity(quantity: int) -> tuple[bool, str]:
        """验证数量"""
        if quantity <= 0:
            return False, "数量必须大于0"

        if quantity > 1000:
            return False, f"⚠️ 数量太大（{quantity}），确定吗？"

        return True, ""

    @staticmethod
    def sanitize_string(text: str, max_length: int = 200) -> str:
        """清理和限制字符串长度"""
        if not text:
            return ""

        # 去除首尾空白
        text = text.strip()

        # 限制长度
        if len(text) > max_length:
            text = text[:max_length]

        return text

    @staticmethod
    def validate_party_data(party_data: dict) -> tuple[bool, list]:
        """
        验证完整的派对数据
        返回：(是否全部有效, 错误消息列表)
        """
        errors = []

        # 验证日期
        if "party_date" in party_data:
            valid, msg = DataValidator.validate_date(party_data["party_date"])
            if not valid:
                errors.append(f"日期错误：{msg}")

        # 验证时间
        if "party_time" in party_data:
            valid, msg = DataValidator.validate_time(party_data["party_time"])
            if not valid:
                errors.append(f"时间错误：{msg}")

        # 验证预算
        if "budget" in party_data:
            valid, msg = DataValidator.validate_budget(party_data["budget"])
            if not valid:
                errors.append(f"预算错误：{msg}")

        # 验证年龄
        if "child_age" in party_data:
            valid, msg = DataValidator.validate_age(party_data["child_age"])
            if not valid:
                errors.append(f"年龄错误：{msg}")

        # 验证客人数量
        if "guest_count_expected" in party_data:
            valid, msg = DataValidator.validate_guest_count(party_data["guest_count_expected"])
            if not valid:
                errors.append(f"客人数量错误：{msg}")

        return len(errors) == 0, errors
