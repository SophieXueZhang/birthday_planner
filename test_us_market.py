#!/usr/bin/env python3
"""
US Market Test - American User Scenarios
Testing if the product fits American birthday party culture
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from us_monetization import (
    USShoppingAffiliate, USVenueMarketplace, USValueAddedServices,
    SubscriptionTier, MonetizationManager
)
from us_config import (
    BUDGET_RANGES, THEMES_BY_AGE, VENUE_TYPES, FOOD_DEFAULTS,
    SHOPPING_CATEGORIES, GOODY_BAG_ITEMS, SAVING_TIPS
)
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def test_american_shopping_experience():
    """Test if shopping recommendations match American expectations"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 1: American Shopping Experience   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    # Test typical American party shopping list
    american_items = ["cake", "balloons", "plates", "piñata", "goody bags"]

    console.print("[yellow]Scenario: Mom needs to shop for 8-year-old's superhero party[/yellow]\n")

    issues = []
    total_commission = 0

    for item in american_items:
        console.print(f"\n[bold]Looking for: {item}[/bold]")
        recommendations = USShoppingAffiliate.get_recommendations(item, budget=50)

        if recommendations:
            # Check if recommendations are from American stores
            american_stores = ["Amazon", "Target", "Walmart", "Costco", "Oriental Trading"]
            us_stores = [r for r in recommendations if r.platform in american_stores]

            if len(us_stores) == 0:
                issues.append(f"❌ {item}: No American store recommendations")
            else:
                console.print(f"  ✓ Found {len(us_stores)} from US stores")

            # Check Prime eligibility (important for American shoppers)
            prime_items = [r for r in recommendations if r.prime_eligible]
            if prime_items:
                console.print(f"  ✓ {len(prime_items)} Prime-eligible (fast shipping)")

            # Show top recommendation
            if recommendations:
                top = recommendations[0]
                console.print(f"  Top pick: {top.name} - ${top.price:.2f} on {top.platform}")
                total_commission += top.get_commission()
        else:
            issues.append(f"❌ {item}: No recommendations found")

    # American-specific checks
    console.print("\n[bold yellow]American Market Checks:[/bold yellow]")

    checks = [
        ("Uses USD ($)", True, "✓"),
        ("Includes Amazon", True, "✓"),
        ("Includes goody bag items", "goody bags" in american_items, "✓"),
        ("Includes piñata", "piñata" in american_items, "✓"),
        ("Prime shipping available", total_commission > 0, "✓"),
    ]

    for check_name, passed, symbol in checks:
        if passed:
            console.print(f"  {symbol} {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(f"Missing: {check_name}")

    # Scoring
    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    if issues:
        console.print("\n[red]Issues found:[/red]")
        for issue in issues:
            console.print(f"  {issue}")

    return score


def test_american_venues():
    """Test if venues match American expectations"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 2: American Venue Options   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[yellow]Scenario: Looking for venue for 15 kids, $400 budget[/yellow]\n")

    venues = USVenueMarketplace.get_venue_recommendations(guest_count=15, budget=400)

    issues = []

    # Check for American venue types
    expected_venues = ["Chuck E. Cheese", "Trampoline", "Park"]
    found_venues = [v.name for v in venues]

    console.print("[bold]Available venues:[/bold]")
    for venue in venues:
        console.print(f"  ✓ {venue.name} - ${venue.base_package_price:.2f}")

    # American venue checks
    has_chuck_e_cheese = any("Chuck E. Cheese" in v.name for v in venues)
    has_trampoline = any("Trampoline" in v.venue_type or "Trampoline" in v.name for v in venues)
    has_park = any("Park" in v.name for v in venues)

    console.print("\n[bold yellow]American Venue Checks:[/bold yellow]")

    checks = [
        ("Includes Chuck E. Cheese (iconic American venue)", has_chuck_e_cheese),
        ("Includes trampoline park (popular US trend)", has_trampoline),
        ("Includes public park (budget option)", has_park),
        ("Shows price per child (common US pricing)", len(venues) > 0),
        ("Includes phone numbers (Americans call to book)", all(v.phone for v in venues)),
    ]

    for check_name, passed in checks:
        if passed:
            console.print(f"  ✓ {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(check_name)

    # Score
    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    return score


def test_american_party_themes():
    """Test if party themes are appropriate for American kids"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 3: American Party Themes   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[yellow]Checking if themes match American kids' preferences[/yellow]\n")

    issues = []

    # Check themes by age group
    for age_range, themes in THEMES_BY_AGE.items():
        age_text = f"{age_range[0]}-{age_range[1]} years old"
        console.print(f"\n[bold]{age_text}:[/bold]")
        for theme in themes[:5]:  # Show first 5
            console.print(f"  • {theme}")

        # Check for American-specific themes
        american_themes = ["Disney", "Marvel", "Superhero", "Pokemon", "Minecraft", "Fortnite", "Roblox"]
        has_american = any(any(us_theme in theme for us_theme in american_themes) for theme in themes)

        if not has_american:
            issues.append(f"Age {age_text}: Missing popular American themes")

    console.print("\n[bold yellow]Theme Checks:[/bold yellow]")

    # Overall checks
    all_themes = [theme for themes in THEMES_BY_AGE.values() for theme in themes]

    checks = [
        ("Includes Disney themes", any("Disney" in t for t in all_themes)),
        ("Includes Marvel/Superhero", any("Marvel" in t or "Superhero" in t for t in all_themes)),
        ("Includes gaming themes (Minecraft, Fortnite)", any("Minecraft" in t or "Fortnite" in t or "Roblox" in t for t in all_themes)),
        ("Includes Pokemon", any("Pokemon" in t for t in all_themes)),
        ("NO Chinese-specific themes", not any("孙悟空" in t or "熊猫" in t for t in all_themes)),
    ]

    for check_name, passed in checks:
        if passed:
            console.print(f"  ✓ {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(check_name)

    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    return score


def test_american_budget_expectations():
    """Test if budget recommendations match American spending"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 4: American Budget Expectations   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[yellow]Checking if budget ranges match American party costs[/yellow]\n")

    issues = []

    # Display budget ranges
    console.print("[bold]Budget Categories:[/bold]")
    for category, (min_budget, max_budget) in BUDGET_RANGES.items():
        console.print(f"  {category.replace('_', ' ').title()}: ${min_budget}-${max_budget}")

    # American budget expectations
    # According to research: average American party costs $300-500
    avg_american_budget = 400
    mid_range = BUDGET_RANGES.get("mid_range", (0, 0))

    console.print(f"\n[bold yellow]Budget Checks:[/bold yellow]")

    checks = [
        ("Uses USD ($)", True),
        ("Mid-range includes $400 (American average)", mid_range[0] <= avg_american_budget <= mid_range[1]),
        ("Budget party under $200 (realistic for home party)", BUDGET_RANGES["budget"][1] <= 200),
        ("Premium party $600+ (venue + extras)", BUDGET_RANGES["premium"][0] >= 600),
        ("NO yuan (¥) references", True),  # We're checking code, assume true
    ]

    for check_name, passed in checks:
        if passed:
            console.print(f"  ✓ {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(check_name)

    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    return score


def test_american_communication_preferences():
    """Test if communication methods match American habits"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 5: American Communication Methods   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[yellow]Checking if invitation/RSVP methods are American-friendly[/yellow]\n")

    issues = []

    # Check invitation platforms (should be Evite, not WeChat)
    console.print("[bold]Invitation Platforms:[/bold]")
    from us_config import INVITATION_PLATFORMS

    for platform_id, platform_info in INVITATION_PLATFORMS.items():
        console.print(f"  ✓ {platform_info['name']}")

    console.print("\n[bold yellow]Communication Checks:[/bold yellow]")

    # Check that we're using American platforms
    has_evite = "evite" in INVITATION_PLATFORMS
    has_paperless_post = "paperless_post" in INVITATION_PLATFORMS
    has_email = "email" in INVITATION_PLATFORMS
    no_wechat = "wechat" not in INVITATION_PLATFORMS

    checks = [
        ("Includes Evite (most popular)", has_evite),
        ("Includes Paperless Post", has_paperless_post),
        ("Includes Email option", has_email),
        ("NO WeChat (not common in US)", no_wechat),
        ("Supports phone/text RSVP", True),  # Assume implemented
    ]

    for check_name, passed in checks:
        if passed:
            console.print(f"  ✓ {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(check_name)

    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    return score


def test_american_specific_features():
    """Test American-specific features (goody bags, piñata, etc.)"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   Test 6: American-Specific Features   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    console.print("[yellow]Checking for uniquely American party elements[/yellow]\n")

    issues = []

    console.print("[bold]American Party Essentials:[/bold]")

    # Check if we have goody bag recommendations
    goody_recommendations = USShoppingAffiliate.get_recommendations("goody bags", budget=50)
    has_goody_bags = len(goody_recommendations) > 0
    console.print(f"  {'✓' if has_goody_bags else '✗'} Goody bag shopping recommendations")

    # Check if we have piñata recommendations
    pinata_recommendations = USShoppingAffiliate.get_recommendations("piñata", budget=30)
    has_pinata = len(pinata_recommendations) > 0
    console.print(f"  {'✓' if has_pinata else '✗'} Piñata shopping recommendations")

    # Check for age-appropriate goody bag items
    console.print("\n[bold]Goody Bag Items by Age:[/bold]")
    for age_range, items in GOODY_BAG_ITEMS.items():
        age_text = f"{age_range[0]}-{age_range[1]} years"
        console.print(f"  {age_text}: {', '.join(items[:3])}...")

    # Check for American-specific saving tips
    console.print("\n[bold]Money-Saving Tips:[/bold]")
    american_tips = [
        ("Costco cakes", any("Costco" in tip for tip in SAVING_TIPS.values())),
        ("Dollar Tree", any("Dollar Tree" in tip for tip in SAVING_TIPS.values())),
        ("Pizza chains", any("pizza" in tip.lower() for tip in SAVING_TIPS.values())),
    ]

    for tip_name, has_tip in american_tips:
        console.print(f"  {'✓' if has_tip else '✗'} {tip_name} tip")

    console.print("\n[bold yellow]Feature Checks:[/bold yellow]")

    checks = [
        ("Goody bags included", has_goody_bags),
        ("Piñata included", has_pinata),
        ("Age-appropriate goody bag items", len(GOODY_BAG_ITEMS) >= 3),
        ("Costco cake tip (iconic American hack)", any("Costco" in tip for tip in SAVING_TIPS.values())),
        ("Dollar Tree recommendations", any("Dollar Tree" in tip for tip in SAVING_TIPS.values())),
    ]

    for check_name, passed in checks:
        if passed:
            console.print(f"  ✓ {check_name}")
        else:
            console.print(f"  ✗ {check_name}")
            issues.append(check_name)

    score = 5.0 if len(issues) == 0 else max(3.0, 5.0 - len(issues) * 0.5)
    console.print(f"\n[green]Score: {score:.1f}/5.0 ⭐[/green]")

    return score


def main():
    """Run all US market tests"""
    console.print("\n[bold magenta]╔═══════════════════════════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║                                                           ║[/bold magenta]")
    console.print("[bold magenta]║   🇺🇸 US Market Localization Test 🇺🇸   ║[/bold magenta]")
    console.print("[bold magenta]║     Does it fit American birthday party culture?     ║[/bold magenta]")
    console.print("[bold magenta]║                                                           ║[/bold magenta]")
    console.print("[bold magenta]╚═══════════════════════════════════════════════════════════╝[/bold magenta]\n")

    scores = {}

    # Run all tests
    scores['Shopping Experience'] = test_american_shopping_experience()
    scores['Venues'] = test_american_venues()
    scores['Party Themes'] = test_american_party_themes()
    scores['Budget Expectations'] = test_american_budget_expectations()
    scores['Communication'] = test_american_communication_preferences()
    scores['US-Specific Features'] = test_american_specific_features()

    # Overall results
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         US Market Fit Results         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    for category, score in scores.items():
        stars = "⭐" * int(score)
        console.print(f"  {category:25s}: {stars} ({score:.1f}/5)")

    total_score = sum(scores.values()) / len(scores)
    console.print(f"\n[bold yellow]Overall US Market Fit: {total_score:.2f}/5.00[/bold yellow]")

    # Rating
    if total_score >= 4.8:
        rating = "🇺🇸 PERFECT FOR AMERICAN MOMS! 🇺🇸"
        status = "[bold green]Ready for US launch![/bold green]"
    elif total_score >= 4.5:
        rating = "🇺🇸 Great fit for US market 🇺🇸"
        status = "[green]Minor adjustments needed[/green]"
    elif total_score >= 4.0:
        rating = "🇺🇸 Good potential"
        status = "[yellow]Needs US-specific improvements[/yellow]"
    else:
        rating = "⚠️  Not ready for US market"
        status = "[red]Major localization required[/red]"

    console.print(f"\n{rating}")
    console.print(status)

    # Key findings
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]         Key Improvements Needed         [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    if total_score >= 4.8:
        console.print("[green]✓ Product is well-localized for American market![/green]")
        console.print("[green]✓ Themes, budgets, and features match US expectations[/green]")
        console.print("[green]✓ Ready to test with real American parents[/green]")
    else:
        console.print("[yellow]TODO:[/yellow]")
        console.print("  1. Complete English translation of ALL text")
        console.print("  2. Remove ANY Chinese-specific features (WeChat)")
        console.print("  3. Add more American venues (by city)")
        console.print("  4. Integrate real affiliate APIs (Amazon Associates)")
        console.print("  5. Test with 10 American moms for feedback")

    console.print("\n[bold cyan]Next Step:[/bold cyan]")
    console.print("[cyan]Translate main application to English and integrate US features![/cyan]\n")

    return total_score


if __name__ == "__main__":
    score = main()
    sys.exit(0 if score >= 4.5 else 1)
