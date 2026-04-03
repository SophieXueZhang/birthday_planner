"""
派对检查清单模块
"""
from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class ChecklistItem:
    """检查清单项"""
    title: str
    completed: bool = False
    notes: str = ""

    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class ChecklistPhase:
    """检查清单阶段"""
    name: str
    days_before: int  # 派对前多少天
    items: List[ChecklistItem] = field(default_factory=list)

    def get_deadline(self, party_date: str) -> str:
        """获取截止日期"""
        try:
            party_dt = datetime.strptime(party_date, "%Y-%m-%d")
            deadline = party_dt - timedelta(days=self.days_before)
            return deadline.strftime("%Y-%m-%d")
        except:
            return "未知"

    def is_overdue(self, party_date: str) -> bool:
        """是否已过期"""
        try:
            deadline = self.get_deadline(party_date)
            return datetime.now() > datetime.strptime(deadline, "%Y-%m-%d")
        except:
            return False

    def completion_rate(self) -> float:
        """完成率"""
        if not self.items:
            return 0.0
        completed = sum(1 for item in self.items if item.completed)
        return completed / len(self.items) * 100

    def to_dict(self):
        return {
            "name": self.name,
            "days_before": self.days_before,
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        items = [ChecklistItem.from_dict(item) for item in data.get("items", [])]
        return cls(
            name=data["name"],
            days_before=data["days_before"],
            items=items
        )


class PartyChecklist:
    """派对检查清单管理器"""

    @staticmethod
    def generate_standard_checklist(child_age: int, guest_count: int) -> List[ChecklistPhase]:
        """生成标准检查清单"""
        phases = []

        # 派对前30天
        phase_30 = ChecklistPhase("派对前1个月", 30)
        phase_30.items = [
            ChecklistItem("确定派对日期和时间"),
            ChecklistItem("预订派对场地"),
            ChecklistItem("确定派对主题"),
            ChecklistItem("列出客人名单"),
            ChecklistItem("制定预算计划"),
        ]
        phases.append(phase_30)

        # 派对前21天
        phase_21 = ChecklistPhase("派对前3周", 21)
        phase_21.items = [
            ChecklistItem("设计邀请函"),
            ChecklistItem("购买或制作邀请函"),
            ChecklistItem("确认场地细节（设施、规则等）"),
        ]
        phases.append(phase_21)

        # 派对前14天
        phase_14 = ChecklistPhase("派对前2周", 14)
        phase_14.items = [
            ChecklistItem("发送邀请函给所有客人"),
            ChecklistItem("预订生日蛋糕"),
            ChecklistItem("购买装饰品（气球、横幅、彩带等）"),
            ChecklistItem("计划派对活动和游戏"),
            ChecklistItem("准备游戏道具和奖品"),
        ]
        if child_age >= 6:
            phase_14.items.append(ChecklistItem("准备娱乐项目（音乐播放列表、视频等）"))
        phases.append(phase_14)

        # 派对前7天
        phase_7 = ChecklistPhase("派对前1周", 7)
        phase_7.items = [
            ChecklistItem("跟进未回复RSVP的客人"),
            ChecklistItem("确认最终参加人数"),
            ChecklistItem("购买派对用品（盘子、杯子、餐巾纸等）"),
            ChecklistItem("购买派对礼品袋和小礼物"),
            ChecklistItem("确认蛋糕订单和取货时间"),
        ]
        if guest_count > 20:
            phase_7.items.append(ChecklistItem("考虑请帮手协助派对当天"))
        phases.append(phase_7)

        # 派对前3天
        phase_3 = ChecklistPhase("派对前3天", 3)
        phase_3.items = [
            ChecklistItem("最后确认参加人数（给未确认的客人打电话）"),
            ChecklistItem("采购食物和饮料"),
            ChecklistItem("准备应急物品（创可贴、纸巾、垃圾袋）"),
            ChecklistItem("打印客人名单和签到表"),
            ChecklistItem("检查相机/手机电量，清理存储空间"),
        ]
        phases.append(phase_3)

        # 派对前1天
        phase_1 = ChecklistPhase("派对前1天", 1)
        phase_1.items = [
            ChecklistItem("充气球、准备装饰材料"),
            ChecklistItem("准备派对游戏和活动材料"),
            ChecklistItem("检查派对服装（寿星和家长）"),
            ChecklistItem("取蛋糕（或确认配送时间）"),
            ChecklistItem("给寿星准备生日帽/皇冠"),
            ChecklistItem("准备蜡烛和打火机"),
            ChecklistItem("检查天气预报（户外派对）"),
        ]
        phases.append(phase_1)

        # 派对当天
        phase_0 = ChecklistPhase("派对当天", 0)
        phase_0.items = [
            ChecklistItem("提前1-2小时到达场地"),
            ChecklistItem("布置装饰（气球、横幅、桌布等）"),
            ChecklistItem("摆放食物和饮料"),
            ChecklistItem("测试音乐播放设备"),
            ChecklistItem("设置签到台和礼物台"),
            ChecklistItem("准备好游戏道具"),
            ChecklistItem("检查洗手间用品"),
            ChecklistItem("设置拍照区域"),
            ChecklistItem("准备好应急物品"),
        ]
        phases.append(phase_0)

        # 派对后
        phase_after = ChecklistPhase("派对结束后", -1)
        phase_after.items = [
            ChecklistItem("清理场地"),
            ChecklistItem("归还租赁物品（如有）"),
            ChecklistItem("整理礼物清单"),
            ChecklistItem("发送感谢信给客人"),
            ChecklistItem("整理照片和视频"),
            ChecklistItem("记录本次派对经验（为下次做参考）"),
        ]
        phases.append(phase_after)

        return phases

    @staticmethod
    def get_current_phase(phases: List[ChecklistPhase], party_date: str) -> ChecklistPhase:
        """获取当前应该关注的阶段"""
        try:
            party_dt = datetime.strptime(party_date, "%Y-%m-%d")
            days_until = (party_dt - datetime.now()).days

            # 找到最接近的阶段
            for phase in phases:
                if days_until >= phase.days_before:
                    return phase

            # 如果都过了，返回最后一个
            return phases[-1] if phases else None
        except:
            return phases[0] if phases else None

    @staticmethod
    def get_urgent_items(phases: List[ChecklistPhase], party_date: str) -> List[tuple]:
        """获取紧急待办事项（未完成且已过期的）"""
        urgent = []
        for phase in phases:
            if phase.is_overdue(party_date):
                for item in phase.items:
                    if not item.completed:
                        urgent.append((phase, item))
        return urgent

    @staticmethod
    def overall_progress(phases: List[ChecklistPhase]) -> float:
        """总体完成进度"""
        total_items = sum(len(phase.items) for phase in phases)
        if total_items == 0:
            return 0.0
        completed_items = sum(
            sum(1 for item in phase.items if item.completed)
            for phase in phases
        )
        return completed_items / total_items * 100
