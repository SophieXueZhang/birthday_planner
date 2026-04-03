"""
US Market Monetization Module
Shopping affiliates, venues, and services for American market
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
    """Product recommendation (US market)"""
    name: str
    category: str
    price: float  # USD
    original_price: float
    platform: str  # Amazon, Target, Walmart, etc.
    affiliate_link: str
    commission_rate: float
    rating: float
    review_count: int
    prime_eligible: bool = False  # Amazon Prime

    def get_commission(self) -> float:
        """Calculate commission in USD"""
        return self.price * self.commission_rate

    def get_discount(self) -> float:
        """Calculate discount percentage"""
        if self.original_price > 0:
            return (1 - self.price / self.original_price) * 100
        return 0


@dataclass
class VenueRecommendation:
    """Venue recommendation (US market)"""
    name: str
    venue_type: str  # "chuck_e_cheese", "trampoline_park", etc.
    address: str
    city: str
    state: str
    zip_code: str
    capacity: int
    price_per_child: float
    base_package_price: float
    facilities: List[str]
    rating: float
    review_count: int
    phone: str
    website: str
    booking_commission: float  # Our commission
    weather_dependent: bool = False


class USShoppingAffiliate:
    """US Shopping affiliate system (Amazon, Target, Walmart)"""

    # Sample product database (in production, use real affiliate APIs)
    PRODUCT_DATABASE = {
        "cake": [
            ProductRecommendation(
                name="Custom Photo Birthday Cake (8-inch)",
                category="Food",
                price=29.99,
                original_price=39.99,
                platform="Costco",
                affiliate_link="https://costco.com/cakes",
                commission_rate=0.0,  # No affiliate, but great recommendation
                rating=4.8,
                review_count=2450,
                prime_eligible=False
            ),
            ProductRecommendation(
                name="Chantilly Chip Birthday Cake",
                category="Food",
                price=24.99,
                original_price=24.99,
                platform="Whole Foods",
                affiliate_link="https://amazon.com/wholefoods/cake",
                commission_rate=0.03,
                rating=4.7,
                review_count=892,
                prime_eligible=True
            ),
        ],
        "balloons": [
            ProductRecommendation(
                name="100pc Pastel Balloon Garland Kit",
                category="Decorations",
                price=15.99,
                original_price=29.99,
                platform="Amazon",
                affiliate_link="https://amzn.to/balloon-garland-kit",
                commission_rate=0.04,
                rating=4.6,
                review_count=12453,
                prime_eligible=True
            ),
            ProductRecommendation(
                name="Jumbo Number Foil Balloons (40-inch)",
                category="Decorations",
                price=7.99,
                original_price=12.99,
                platform="Amazon",
                affiliate_link="https://amzn.to/number-balloons",
                commission_rate=0.04,
                rating=4.7,
                review_count=8932,
                prime_eligible=True
            ),
        ],
        "plates": [
            ProductRecommendation(
                name="Themed Party Plates & Napkins Set (Serves 24)",
                category="Tableware",
                price=19.99,
                original_price=34.99,
                platform="Amazon",
                affiliate_link="https://amzn.to/party-plates-set",
                commission_rate=0.04,
                rating=4.5,
                review_count=5234,
                prime_eligible=True
            ),
            ProductRecommendation(
                name="Up&Up Disposable Party Plates (50ct)",
                category="Tableware",
                price=8.99,
                original_price=8.99,
                platform="Target",
                affiliate_link="https://target.com/party-plates",
                commission_rate=0.08,
                rating=4.4,
                review_count=1567,
                prime_eligible=False
            ),
        ],
        "piñata": [
            ProductRecommendation(
                name="Pull-String Piñata (No Bat Needed)",
                category="Activities",
                price=16.99,
                original_price=24.99,
                platform="Amazon",
                affiliate_link="https://amzn.to/pull-string-pinata",
                commission_rate=0.04,
                rating=4.6,
                review_count=3421,
                prime_eligible=True
            ),
        ],
        "goody bags": [
            ProductRecommendation(
                name="Pre-Filled Party Favor Bags (12 pack)",
                category="Goody Bags",
                price=24.99,
                original_price=39.99,
                platform="Amazon",
                affiliate_link="https://amzn.to/goody-bags",
                commission_rate=0.04,
                rating=4.5,
                review_count=2876,
                prime_eligible=True
            ),
            ProductRecommendation(
                name="Bulk Party Favor Toys (100 pieces)",
                category="Goody Bags",
                price=19.99,
                original_price=34.99,
                platform="Oriental Trading",
                affiliate_link="https://orientaltrading.com/bulk-toys",
                commission_rate=0.05,
                rating=4.3,
                review_count=1234,
                prime_eligible=False
            ),
        ],
    }

    @staticmethod
    def get_recommendations(item_name: str, budget: float = 100) -> List[ProductRecommendation]:
        """Get product recommendations based on item name"""
        recommendations = []

        # Search for matching products
        search_terms = item_name.lower()
        for key, products in USShoppingAffiliate.PRODUCT_DATABASE.items():
            if key in search_terms or search_terms in key:
                recommendations.extend(products)

        # Sort by rating and reviews
        recommendations.sort(key=lambda x: (x.rating, x.review_count), reverse=True)

        # Filter by budget
        recommendations = [r for r in recommendations if r.price <= budget]

        return recommendations[:5]

    @staticmethod
    def show_product_comparison(recommendations: List[ProductRecommendation]):
        """Display product comparison table"""
        if not recommendations:
            console.print("[yellow]No recommendations found[/yellow]")
            return

        console.print("\n[bold cyan]💰 Smart Shopping Recommendations[/bold cyan]\n")

        table = Table(box=box.ROUNDED, show_header=True)
        table.add_column("Product", style="cyan", width=30)
        table.add_column("Store", style="yellow", width=10)
        table.add_column("Price", style="green", width=15)
        table.add_column("Rating", style="blue", width=12)
        table.add_column("Prime", style="magenta", width=8)

        for i, product in enumerate(recommendations, 1):
            discount = product.get_discount()
            discount_text = f"{discount:.0f}% OFF" if discount > 0 else ""

            price_text = f"${product.price:.2f}"
            if product.original_price > product.price:
                price_text = f"[green]${product.price:.2f}[/green]\n[dim strikethrough]${product.original_price:.2f}[/dim strikethrough]"

            prime_text = "✓" if product.prime_eligible else ""

            table.add_row(
                f"{i}. {product.name}\n[dim]{discount_text}[/dim]",
                product.platform,
                price_text,
                f"⭐{product.rating}\n[dim]{product.review_count} reviews[/dim]",
                prime_text
            )

        console.print(table)

        # Show savings
        total_save = sum(r.original_price - r.price for r in recommendations if r.original_price > r.price)
        if total_save > 0:
            console.print(f"\n[green]💡 Save ${total_save:.2f} by shopping through our recommendations![/green]")

        # Prime shipping notice
        prime_items = sum(1 for r in recommendations if r.prime_eligible)
        if prime_items > 0:
            console.print(f"[blue]📦 {prime_items} item(s) eligible for FREE Prime shipping[/blue]")


class USVenueMarketplace:
    """US venue marketplace"""

    VENUE_DATABASE = [
        VenueRecommendation(
            name="Chuck E. Cheese",
            venue_type="entertainment_center",
            address="123 Main Street",
            city="Los Angeles",
            state="CA",
            zip_code="90001",
            capacity=30,
            price_per_child=20.99,
            base_package_price=199.99,
            facilities=["Arcade games", "Pizza", "Birthday throne", "Show"],
            rating=4.2,
            review_count=1523,
            phone="(555) 123-4567",
            website="https://chuckecheese.com",
            booking_commission=25.00
        ),
        VenueRecommendation(
            name="Sky Zone Trampoline Park",
            venue_type="trampoline_park",
            address="456 Jump Lane",
            city="Los Angeles",
            state="CA",
            zip_code="90002",
            capacity=20,
            price_per_child=24.99,
            base_package_price=299.99,
            facilities=["Trampolines", "Dodgeball court", "Foam pit", "Private party room"],
            rating=4.7,
            review_count=2341,
            phone="(555) 234-5678",
            website="https://skyzone.com",
            booking_commission=30.00
        ),
        VenueRecommendation(
            name="Sunset Park Pavilion",
            venue_type="public_park",
            address="789 Park Avenue",
            city="Los Angeles",
            state="CA",
            zip_code="90003",
            capacity=50,
            price_per_child=0,
            base_package_price=50.00,  # Permit fee
            facilities=["Playground", "Picnic tables", "Grills", "Restrooms"],
            rating=4.5,
            review_count=892,
            phone="(555) 345-6789",
            website="https://laparks.org",
            booking_commission=0,  # No commission on parks
            weather_dependent=True
        ),
    ]

    @staticmethod
    def get_venue_recommendations(guest_count: int, budget: float) -> List[VenueRecommendation]:
        """Get venue recommendations based on guest count and budget"""
        recommendations = []

        for venue in USVenueMarketplace.VENUE_DATABASE:
            # Check capacity
            if venue.capacity >= guest_count:
                # Estimate total cost
                total_cost = venue.base_package_price
                if venue.price_per_child > 0:
                    total_cost = venue.base_package_price + (guest_count * venue.price_per_child)

                # Check if within budget
                if total_cost <= budget:
                    recommendations.append(venue)

        # Sort by rating
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        return recommendations

    @staticmethod
    def show_venue_recommendations(venues: List[VenueRecommendation]):
        """Display venue recommendations"""
        if not venues:
            console.print("[yellow]No suitable venues found for your budget and guest count[/yellow]")
            console.print("[cyan]💡 Tip: Consider a home party or public park to save money![/cyan]")
            return

        console.print("\n[bold cyan]🏠 Venue Recommendations[/bold cyan]\n")

        for i, venue in enumerate(venues, 1):
            facilities_text = ", ".join(venue.facilities[:4])

            price_info = f"${venue.base_package_price:.2f} base"
            if venue.price_per_child > 0:
                price_info += f" + ${venue.price_per_child:.2f}/child"

            weather_note = ""
            if venue.weather_dependent:
                weather_note = "\n⚠️  Weather-dependent - plan a backup!"

            panel_content = f"""
[bold]{venue.name}[/bold]
📍 {venue.address}, {venue.city}, {venue.state} {venue.zip_code}
👥 Capacity: {venue.capacity} guests
💰 Price: {price_info}
⭐ Rating: {venue.rating}/5.0 ({venue.review_count} reviews)
🏢 Facilities: {facilities_text}
📞 Phone: {venue.phone}
🌐 Website: {venue.website}{weather_note}

[dim]💡 Book through our platform for best rates![/dim]
"""
            console.print(Panel(panel_content, border_style="cyan"))


class USValueAddedServices:
    """Value-added services for US market"""

    SERVICES = {
        "custom_invitation_design": {
            "name": "Custom Invitation Design",
            "price": 49.99,
            "description": "Professional designer creates 3 custom invitation designs",
            "delivery_days": 2,
            "popular": True,
            "category": "Design"
        },
        "party_planning_consultation": {
            "name": "Party Planning Consultation",
            "price": 99.99,
            "description": "1-hour video call with expert party planner",
            "delivery_days": 0,
            "popular": True,
            "category": "Consultation"
        },
        "photographer_booking": {
            "name": "Professional Photographer",
            "price": 75.00,  # Our commission
            "description": "Book a local photographer (2-hour session)",
            "delivery_days": 0,
            "popular": False,
            "category": "Photography"
        },
        "themed_party_package": {
            "name": "Complete Themed Party Package",
            "price": 199.99,
            "description": "Everything you need for themed party (decorations, activities, favors)",
            "delivery_days": 5,
            "popular": True,
            "category": "Package"
        },
        "goody_bag_assembly": {
            "name": "Goody Bag Assembly Service",
            "price": 3.99,  # Per bag
            "description": "We assemble and deliver custom goody bags",
            "delivery_days": 3,
            "popular": False,
            "category": "Service"
        },
    }

    @staticmethod
    def show_services_marketplace():
        """Display services marketplace"""
        console.print("\n[bold cyan]💎 Services Marketplace[/bold cyan]\n")

        for service_id, service in USValueAddedServices.SERVICES.items():
            popular_tag = " [red]🔥 POPULAR[/red]" if service.get("popular") else ""

            console.print(f"[bold cyan]{service['name']}{popular_tag}[/bold cyan]")
            console.print(f"  💰 Price: ${service['price']:.2f}")
            console.print(f"  📝 {service['description']}")
            if service['delivery_days'] > 0:
                console.print(f"  ⏱️  Delivery: {service['delivery_days']} business days")
            else:
                console.print(f"  ⏱️  Instant service")
            console.print()


class SubscriptionTier:
    """US subscription tiers"""
    FREE = "free"
    PREMIUM = "premium"
    PARTY_PRO = "party_pro"

    TIER_INFO = {
        FREE: {
            "name": "Free Plan",
            "price": 0,
            "features": [
                "Plan 1 party at a time",
                "Basic shopping lists",
                "Standard checklist",
                "Text export",
                "Email invitations"
            ],
            "limits": {
                "max_parties": 1,
                "max_guests": 30,
                "export_formats": ["txt"],
                "invitation_designs": 3
            }
        },
        PREMIUM: {
            "name": "Premium",
            "price": 49,  # Annual
            "price_monthly": 8,
            "features": [
                "✓ Everything in Free",
                "Unlimited parties",
                "Advanced budget tracking",
                "PDF & Excel export",
                "30+ invitation templates",
                "Priority support",
                "Ad-free experience",
                "Shopping deal alerts"
            ],
            "limits": {
                "max_parties": -1,
                "max_guests": 100,
                "export_formats": ["txt", "pdf", "excel"],
                "invitation_designs": 30
            }
        },
        PARTY_PRO: {
            "name": "Party Pro",
            "price": 199,  # Annual
            "features": [
                "✓ Everything in Premium",
                "Multi-user collaboration",
                "Custom branding",
                "Vendor network access",
                "Dedicated account manager",
                "Event analytics",
                "API access",
                "Bulk discounts on services"
            ],
            "limits": {
                "max_parties": -1,
                "max_guests": -1,
                "export_formats": ["txt", "pdf", "excel", "csv", "api"],
                "invitation_designs": -1
            }
        }
    }


class MonetizationManager:
    """US market monetization manager"""

    def __init__(self, user_tier: str = SubscriptionTier.FREE):
        self.user_tier = user_tier
        self.total_commission_earned = 0.0

    def check_feature_access(self, feature_id: str) -> bool:
        """Check if user can access a feature"""
        premium_features = [
            "unlimited_parties",
            "advanced_export",
            "premium_templates",
            "budget_tracking",
            "deal_alerts"
        ]

        if feature_id in premium_features:
            return self.user_tier in [SubscriptionTier.PREMIUM, SubscriptionTier.PARTY_PRO]

        return True

    def show_upgrade_prompt(self, feature_name: str):
        """Show upgrade prompt"""
        console.print(f"\n[yellow]💎 '{feature_name}' is a Premium feature[/yellow]")
        console.print(f"[cyan]Upgrade to Premium for just $49/year ($4/month)[/cyan]")
        console.print(f"[green]✓ Save time ✓ Get deals ✓ Better parties[/green]")
        console.print(f"[dim]Type 'upgrade' to see pricing[/dim]\n")

    @staticmethod
    def show_pricing_comparison():
        """Display pricing comparison table"""
        console.print("\n[bold magenta]╔═══════════════════════════════════════════════════════════╗[/bold magenta]")
        console.print("[bold magenta]║           Choose Your Perfect Plan           ║[/bold magenta]")
        console.print("[bold magenta]╚═══════════════════════════════════════════════════════════╝[/bold magenta]\n")

        table = Table(box=box.DOUBLE, show_header=True)
        table.add_column("Feature", style="white", width=30)
        table.add_column("Free", style="yellow", width=15)
        table.add_column("Premium", style="green", width=15)
        table.add_column("Party Pro", style="cyan", width=15)

        # Price row
        table.add_row(
            "[bold]Price[/bold]",
            "[bold yellow]$0[/bold yellow]",
            "[bold green]$49/year\n$8/month[/bold green]",
            "[bold cyan]$199/year[/bold cyan]"
        )

        # Features
        features = [
            ("Active Parties", "1", "Unlimited", "Unlimited"),
            ("Guest Limit", "30", "100", "No limit"),
            ("Export Formats", "Text", "PDF/Excel", "All + API"),
            ("Invitation Templates", "3", "30+", "Unlimited"),
            ("Ads", "Yes", "No", "No"),
            ("Support", "Standard", "Priority", "Dedicated"),
        ]

        for feature_name, free, premium, pro in features:
            table.add_row(feature_name, free, premium, pro)

        console.print(table)

        # ROI analysis
        console.print("\n[bold cyan]💡 Return on Investment (Premium):[/bold cyan]")
        console.print("  • Price: $49/year = $4.08/month")
        console.print("  • Average savings from deals: $50+ per party")
        console.print("  • Time saved: 3+ hours per party")
        console.print("  [green]Plan 1 party = Premium pays for itself![/green]\n")
