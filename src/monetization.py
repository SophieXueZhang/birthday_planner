"""
商业化模块 - 盈利功能
包括：购物导购、会员系统、增值服务
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


@dataclass
class ProductRecommendation:
    """商品推荐"""
    name: str
    category: str
    price: float
    original_price: float  # 原价
    platform: str  # 平台：淘宝、京东、拼多多
    affiliate_link: str  # 联盟链接
    commission_rate: float  # 佣金率
    rating: float  # 评分
    sales: int  # 销量
    store_name: str  # 店铺名

    def get_commission(self) -> float:
        """计算佣金"""
        return self.price * self.commission_rate

    def get_discount(self) -> float:
        """计算折扣"""
        if self.original_price > 0:
            return (1 - self.price / self.original_price) * 100
        return 0


@dataclass
class VenueRecommendation:
    """场地推荐"""
    name: str
    address: str
    capacity: int  # 可容纳人数
    price_range: str  # 价格区间
    facilities: List[str]  # 设施
    rating: float
    contact: str
    commission: float  # 推荐佣金
    booking_link: str


@dataclass
class PremiumFeature:
    """专业版功能"""
    feature_id: str
    name: str
    description: str
    required_tier: str  # free, pro, enterprise


class SubscriptionTier:
    """订阅等级"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

    TIER_INFO = {
        FREE: {
            "name": "免费版",
            "price": 0,
            "features": [
                "基础派对规划",
                "单个派对管理",
                "基础购物清单",
                "简单文本导出",
                "标准客服支持"
            ],
            "limits": {
                "max_parties": 1,
                "max_guests_per_party": 30,
                "export_formats": ["txt"],
                "invitation_templates": 3
            }
        },
        PRO: {
            "name": "专业版",
            "price": 99,  # 年费
            "price_monthly": 19,
            "features": [
                "✓ 免费版所有功能",
                "无限派对数量",
                "多派对对比分析",
                "高级导出（PDF、Excel、图片）",
                "50+ 专业邀请函模板",
                "预算优化AI建议",
                "数据云同步",
                "优先客服支持",
                "无广告体验"
            ],
            "limits": {
                "max_parties": -1,  # 无限
                "max_guests_per_party": 200,
                "export_formats": ["txt", "pdf", "excel", "image"],
                "invitation_templates": 50
            }
        },
        ENTERPRISE: {
            "name": "企业版",
            "price": 5000,  # 年费
            "features": [
                "✓ 专业版所有功能",
                "多用户协作",
                "品牌定制",
                "API接入",
                "专属客户经理",
                "数据分析报告",
                "商家管理后台"
            ],
            "limits": {
                "max_parties": -1,
                "max_guests_per_party": -1,
                "export_formats": ["txt", "pdf", "excel", "image", "api"],
                "invitation_templates": -1
            }
        }
    }


class ShoppingAffiliate:
    """购物联盟导购系统"""

    # 模拟商品数据库（实际应该对接真实API）
    PRODUCT_DATABASE = {
        "蛋糕": [
            ProductRecommendation(
                name="8寸奶油水果生日蛋糕",
                category="蛋糕",
                price=158.0,
                original_price=228.0,
                platform="淘宝",
                affiliate_link="https://s.click.taobao.com/xxx",
                commission_rate=0.15,
                rating=4.9,
                sales=5230,
                store_name="甜蜜时光烘焙"
            ),
            ProductRecommendation(
                name="10寸双层芭比公主蛋糕",
                category="蛋糕",
                price=268.0,
                original_price=398.0,
                platform="京东",
                affiliate_link="https://union.jd.com/xxx",
                commission_rate=0.12,
                rating=4.8,
                sales=3156,
                store_name="好利来旗舰店"
            ),
        ],
        "气球": [
            ProductRecommendation(
                name="马卡龙色气球100个装",
                category="装饰",
                price=29.9,
                original_price=59.8,
                platform="拼多多",
                affiliate_link="https://p.pinduoduo.com/xxx",
                commission_rate=0.25,
                rating=4.7,
                sales=12450,
                store_name="派对装饰专营"
            ),
            ProductRecommendation(
                name="铝膜数字气球套装",
                category="装饰",
                price=35.8,
                original_price=68.0,
                platform="淘宝",
                affiliate_link="https://s.click.taobao.com/yyy",
                commission_rate=0.20,
                rating=4.8,
                sales=8930,
                store_name="气球王国"
            ),
        ],
        "餐具": [
            ProductRecommendation(
                name="一次性餐具套装50人份",
                category="用品",
                price=45.0,
                original_price=89.0,
                platform="京东",
                affiliate_link="https://union.jd.com/yyy",
                commission_rate=0.18,
                rating=4.6,
                sales=6780,
                store_name="派对用品旗舰店"
            ),
        ],
    }

    @staticmethod
    def get_recommendations(item_name: str, budget: float = 1000) -> List[ProductRecommendation]:
        """获取商品推荐"""
        recommendations = []

        # 查找匹配的商品
        for key, products in ShoppingAffiliate.PRODUCT_DATABASE.items():
            if key in item_name or item_name in key:
                recommendations.extend(products)

        # 按评分和销量排序
        recommendations.sort(key=lambda x: (x.rating, x.sales), reverse=True)

        # 筛选符合预算的
        recommendations = [r for r in recommendations if r.price <= budget]

        return recommendations[:5]  # 返回前5个

    @staticmethod
    def show_product_comparison(recommendations: List[ProductRecommendation]):
        """显示商品对比表"""
        if not recommendations:
            console.print("[yellow]暂无推荐商品[/yellow]")
            return

        console.print("\n[bold cyan]💰 智能购物推荐（含优惠）[/bold cyan]\n")

        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("商品", style="cyan", width=25)
        table.add_column("平台", style="yellow", width=8)
        table.add_column("价格", style="green", width=12)
        table.add_column("折扣", style="magenta", width=8)
        table.add_column("评分", style="blue", width=8)
        table.add_column("销量", style="white", width=10)

        for i, product in enumerate(recommendations, 1):
            discount = product.get_discount()
            discount_text = f"{discount:.0f}%OFF" if discount > 0 else "-"

            price_text = f"¥{product.price:.0f}"
            if product.original_price > product.price:
                price_text = f"[green]¥{product.price:.0f}[/green]\n[dim strikethrough]¥{product.original_price:.0f}[/dim strikethrough]"

            table.add_row(
                f"{i}. {product.name}\n[dim]{product.store_name}[/dim]",
                product.platform,
                price_text,
                f"[red]{discount_text}[/red]" if discount > 0 else "-",
                f"⭐{product.rating}",
                f"{product.sales}+"
            )

        console.print(table)

        # 显示省钱提示
        total_save = sum(r.original_price - r.price for r in recommendations if r.original_price > r.price)
        if total_save > 0:
            console.print(f"\n[green]💡 通过平台购买可节省：¥{total_save:.0f}[/green]")

        # 显示佣金（调试用，实际不展示给用户）
        # total_commission = sum(r.get_commission() for r in recommendations)
        # console.print(f"[dim]（平台收益：¥{total_commission:.2f}）[/dim]")


class VenueMarketplace:
    """场地市场"""

    VENUE_DATABASE = [
        VenueRecommendation(
            name="欢乐时光儿童乐园",
            address="朝阳区望京SOHO 3层",
            capacity=30,
            price_range="¥800-1500",
            facilities=["游乐设施", "独立派对房", "音响设备", "桌椅"],
            rating=4.8,
            contact="400-888-6666",
            commission=100.0,
            booking_link="https://booking.example.com/venue1"
        ),
        VenueRecommendation(
            name="彩虹糖亲子餐厅",
            address="海淀区中关村大街1号",
            capacity=25,
            price_range="¥600-1200",
            facilities=["儿童餐", "游戏区", "拍照背景墙"],
            rating=4.6,
            contact="010-8888-9999",
            commission=80.0,
            booking_link="https://booking.example.com/venue2"
        ),
    ]

    @staticmethod
    def get_venue_recommendations(guest_count: int, budget: float) -> List[VenueRecommendation]:
        """获取场地推荐"""
        recommendations = []

        for venue in VenueMarketplace.VENUE_DATABASE:
            # 过滤容量合适的
            if venue.capacity >= guest_count:
                # 解析价格区间
                price_parts = venue.price_range.replace("¥", "").split("-")
                min_price = float(price_parts[0])
                max_price = float(price_parts[1]) if len(price_parts) > 1 else min_price

                # 预算合适的
                if min_price <= budget:
                    recommendations.append(venue)

        # 按评分排序
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        return recommendations

    @staticmethod
    def show_venue_recommendations(venues: List[VenueRecommendation]):
        """显示场地推荐"""
        if not venues:
            console.print("[yellow]暂无合适的场地推荐[/yellow]")
            return

        console.print("\n[bold cyan]🏠 场地推荐[/bold cyan]\n")

        for i, venue in enumerate(venues, 1):
            facilities_text = "、".join(venue.facilities[:4])

            panel_content = f"""
[bold]{venue.name}[/bold]
📍 {venue.address}
👥 容纳：{venue.capacity}人
💰 价格：{venue.price_range}
⭐ 评分：{venue.rating}
🏢 设施：{facilities_text}
📞 联系：{venue.contact}

[dim]💡 通过平台预订可享优惠[/dim]
"""
            console.print(Panel(panel_content, border_style="cyan"))


class ValueAddedServices:
    """增值服务市场"""

    SERVICES = {
        "custom_invitation": {
            "name": "定制邀请函设计",
            "price": 199,
            "description": "专业设计师1对1定制，3款方案选择",
            "delivery_days": 2,
            "popular": True
        },
        "party_consultation": {
            "name": "派对策划咨询",
            "price": 299,
            "description": "资深策划师1小时视频咨询，提供专业建议",
            "delivery_days": 0,
            "popular": True
        },
        "photographer": {
            "name": "专业摄影师推荐",
            "price": 100,  # 佣金
            "description": "推荐本地优秀摄影师，拍摄费用另计",
            "delivery_days": 0,
            "popular": False
        },
        "theme_package": {
            "name": "主题派对套餐",
            "price": 50,  # 佣金
            "description": "与品牌合作的主题套餐（冰雪奇缘、汪汪队等）",
            "delivery_days": 7,
            "popular": True
        },
    }

    @staticmethod
    def show_services_marketplace():
        """显示增值服务市场"""
        console.print("\n[bold cyan]💎 增值服务市场[/bold cyan]\n")

        for service_id, service in ValueAddedServices.SERVICES.items():
            popular_tag = " [red]🔥热门[/red]" if service.get("popular") else ""

            console.print(f"[bold cyan]{service['name']}{popular_tag}[/bold cyan]")
            console.print(f"  💰 价格：¥{service['price']}")
            console.print(f"  📝 {service['description']}")
            console.print(f"  ⏱️  交付时间：{service['delivery_days']}天" if service['delivery_days'] > 0 else "  ⏱️  即时服务")
            console.print()


class RevenueTracker:
    """收益追踪（内部使用）"""

    def __init__(self):
        self.commission_history: List[Dict] = []
        self.subscription_revenue: float = 0
        self.service_revenue: float = 0

    def track_commission(self, product: ProductRecommendation, user_id: str):
        """追踪佣金"""
        commission = product.get_commission()
        self.commission_history.append({
            "timestamp": datetime.now(),
            "user_id": user_id,
            "product": product.name,
            "platform": product.platform,
            "price": product.price,
            "commission": commission
        })

    def get_total_commission(self) -> float:
        """获取总佣金"""
        return sum(item["commission"] for item in self.commission_history)

    def get_revenue_report(self) -> Dict:
        """获取收益报告"""
        return {
            "commission_total": self.get_total_commission(),
            "subscription_total": self.subscription_revenue,
            "service_total": self.service_revenue,
            "grand_total": self.get_total_commission() + self.subscription_revenue + self.service_revenue,
            "commission_count": len(self.commission_history)
        }


class MonetizationManager:
    """商业化管理器"""

    def __init__(self, user_tier: str = SubscriptionTier.FREE):
        self.user_tier = user_tier
        self.revenue_tracker = RevenueTracker()

    def check_feature_access(self, feature_id: str) -> bool:
        """检查功能访问权限"""
        # 简化版，实际应该从数据库读取feature定义
        pro_features = [
            "unlimited_parties",
            "advanced_export",
            "premium_templates",
            "cloud_sync",
            "no_ads"
        ]

        if feature_id in pro_features:
            return self.user_tier in [SubscriptionTier.PRO, SubscriptionTier.ENTERPRISE]

        return True  # 免费功能

    def show_upgrade_prompt(self, feature_name: str):
        """显示升级提示"""
        console.print(f"\n[yellow]💎 '{feature_name}' 是专业版功能[/yellow]")
        console.print(f"[cyan]升级到专业版即可使用：仅¥99/年（¥8.25/月）[/cyan]")
        console.print(f"[dim]输入 'upgrade' 查看详情[/dim]\n")

    @staticmethod
    def show_pricing_comparison():
        """显示定价对比"""
        console.print("\n[bold magenta]╔═══════════════════════════════════════════════════════════╗[/bold magenta]")
        console.print("[bold magenta]║              选择适合你的方案              ║[/bold magenta]")
        console.print("[bold magenta]╚═══════════════════════════════════════════════════════════╝[/bold magenta]\n")

        table = Table(box=box.DOUBLE, show_header=True)
        table.add_column("功能", style="white", width=30)
        table.add_column("免费版", style="yellow", width=15)
        table.add_column("专业版", style="green", width=15)
        table.add_column("企业版", style="cyan", width=15)

        # 价格行
        table.add_row(
            "[bold]价格[/bold]",
            "[bold yellow]¥0[/bold yellow]",
            "[bold green]¥99/年\n¥19/月[/bold green]",
            "[bold cyan]¥5,000/年[/bold cyan]"
        )

        # 功能对比
        features = [
            ("派对数量", "1个", "无限", "无限"),
            ("客人数量", "30人/派对", "200人/派对", "无限"),
            ("导出格式", "文本", "PDF/Excel/图片", "全部+API"),
            ("邀请函模板", "3个", "50+", "无限+定制"),
            ("数据同步", "❌", "✓", "✓"),
            ("广告", "有", "无", "无"),
            ("客服支持", "标准", "优先", "专属经理"),
        ]

        for feature_name, free, pro, enterprise in features:
            table.add_row(feature_name, free, pro, enterprise)

        console.print(table)

        # ROI分析
        console.print("\n[bold cyan]💡 投资回报分析（专业版）：[/bold cyan]")
        console.print("  • 每年办2次派对：¥99 ÷ 2 = ¥49.5/次")
        console.print("  • 省时省力：节省4小时规划时间/次 × ¥50时薪 = ¥200价值")
        console.print("  • 购物优惠：平均节省¥100/次 × 2次 = ¥200")
        console.print("  [green]总价值：¥400+ > 投入：¥99（4倍回报）[/green]\n")
