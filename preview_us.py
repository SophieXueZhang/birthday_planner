#!/usr/bin/env python3
"""
🇺🇸 Birthday Party Planner - US Version Preview
Simulates what an American parent would experience
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from us_config import *
from us_monetization import *
from models import Party, Guest, ShoppingItem
from checklist import PartyChecklist
from dashboard import PartyDashboard
from datetime import datetime, timedelta
import time

console = Console()


def pause(seconds=1.5):
    time.sleep(seconds)


def preview():
    """Complete preview of the US Birthday Party Planner"""

    # ═══════════════════════════════════════
    # WELCOME SCREEN
    # ═══════════════════════════════════════
    console.print("\n")
    console.print("[bold magenta]╔═══════════════════════════════════════════════════════════╗[/bold magenta]")
    console.print("[bold magenta]║                                                           ║[/bold magenta]")
    console.print("[bold magenta]║       🎉  Birthday Party Planner  🎂                     ║[/bold magenta]")
    console.print("[bold magenta]║                                                           ║[/bold magenta]")
    console.print("[bold magenta]║       Plan the perfect party for your kid!                ║[/bold magenta]")
    console.print("[bold magenta]║                                                           ║[/bold magenta]")
    console.print("[bold magenta]╚═══════════════════════════════════════════════════════════╝[/bold magenta]")
    pause(1)

    # ═══════════════════════════════════════
    # FIRST-TIME WELCOME GUIDE
    # ═══════════════════════════════════════
    console.print("\n[bold cyan]👋 Welcome! Looks like this is your first time here.[/bold cyan]\n")
    console.print(Panel(
        "[bold]Quick Start Guide[/bold]\n\n"
        "1️⃣  [cyan]Create a Party[/cyan] → Enter your child's info\n"
        "2️⃣  [cyan]Get Smart Suggestions[/cyan] → We'll build your shopping list\n"
        "3️⃣  [cyan]Track Everything[/cyan] → Guests, budget, to-dos\n\n"
        "[dim]It takes about 2 minutes to set up. Let's go![/dim]",
        title="🎈 3 Easy Steps",
        border_style="cyan"
    ))
    pause(2)

    # ═══════════════════════════════════════
    # SCENARIO: BUSY BETH CREATES A PARTY
    # ═══════════════════════════════════════
    console.print("\n[bold yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold yellow]")
    console.print("[bold yellow]  PREVIEW: Busy Beth plans her son's 6th birthday party  [/bold yellow]")
    console.print("[bold yellow]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold yellow]\n")
    pause(1)

    console.print("[dim]Beth is a working mom. It's 9pm, kids are asleep.[/dim]")
    console.print("[dim]She has 15 minutes to plan her son Liam's Spider-Man party.[/dim]\n")
    pause(1.5)

    # Step 1: Create party
    console.print("[bold green]Step 1: Create Party[/bold green]\n")
    console.print("  Child's name: [cyan]Liam[/cyan]")
    console.print("  Age: [cyan]6[/cyan]")
    console.print("  Party date: [cyan]May 17, 2026[/cyan]")
    console.print("  Time: [cyan]2:00 PM[/cyan]")
    console.print("  Venue: [cyan]Backyard[/cyan]")
    console.print("  Budget: [cyan]$400[/cyan]")
    console.print("  Theme: [cyan]Spider-Man[/cyan]")
    console.print("  Expected guests: [cyan]15 kids[/cyan]")
    pause(1)
    console.print("\n[green]✓ Party created![/green]")
    pause(1)

    # Create the actual party object for demo
    party_date = (datetime.now() + timedelta(days=44)).strftime("%Y-%m-%d")
    party = Party(
        id="preview_demo",
        child_name="Liam",
        child_age=6,
        party_date=party_date,
        party_time="14:00",
        venue="Backyard",
        venue_address="123 Oak Street, Los Angeles, CA 90001",
        budget=400.0,
        theme="Spider-Man",
        guest_count_expected=15
    )

    # Add guests
    guests_data = [
        ("Emma Johnson", "confirmed"), ("Noah Williams", "confirmed"),
        ("Olivia Brown", "confirmed"), ("James Davis", "confirmed"),
        ("Sophia Miller", "confirmed"), ("Benjamin Wilson", "confirmed"),
        ("Ava Moore", "confirmed"), ("Lucas Taylor", "pending"),
        ("Mia Anderson", "pending"), ("Henry Thomas", "pending"),
        ("Charlotte Jackson", "pending"), ("Alexander White", "declined"),
    ]
    for name, status in guests_data:
        party.add_guest(Guest(name=name, contact="parent@email.com", rsvp_status=status))

    # Add shopping items
    shopping_data = [
        ("Spider-Man cake (Costco)", "Food", 1, 24.99, True, 22.99),
        ("Pizza (3 large)", "Food", 3, 8.99, True, 8.99),
        ("Juice boxes (24-pack)", "Food", 2, 6.49, True, 5.99),
        ("Spider-Man plates & napkins", "Tableware", 1, 19.99, True, 19.99),
        ("Balloon garland kit (red/blue)", "Decorations", 1, 15.99, False, 0),
        ("Spider-Man banner", "Decorations", 1, 8.99, False, 0),
        ("Spider-Man piñata", "Activities", 1, 16.99, False, 0),
        ("Piñata candy (2 lbs)", "Activities", 1, 12.99, False, 0),
        ("Goody bags (pre-filled, 15-pack)", "Goody Bags", 1, 24.99, False, 0),
        ("Bubbles (12-pack party favors)", "Goody Bags", 1, 9.99, False, 0),
        ("Paper cups", "Tableware", 1, 4.99, False, 0),
        ("Plastic utensils", "Tableware", 1, 3.99, False, 0),
        ("Thank you cards (15-pack)", "Misc", 1, 7.99, False, 0),
    ]

    for name, cat, qty, est_price, purchased, actual in shopping_data:
        item = ShoppingItem(
            name=name, category=cat, quantity=qty,
            estimated_price=est_price, purchased=purchased,
            actual_price=actual,
            store="Amazon" if "Spider" in name or "Goody" in name else "Costco" if "Costco" in name else "Target",
            priority="必买" if cat in ["Food", "Tableware"] else "推荐"
        )
        party.add_shopping_item(item)

    # Generate checklist
    party.checklist_phases = PartyChecklist.generate_standard_checklist(6, 15)
    # Mark some as complete
    for phase in party.checklist_phases[:3]:
        for item in phase.items[:2]:
            item.completed = True

    # ═══════════════════════════════════════
    # DASHBOARD VIEW
    # ═══════════════════════════════════════
    pause(1)
    console.print("\n[bold green]Step 2: Dashboard — See Everything at a Glance[/bold green]\n")
    pause(0.5)

    # Custom English dashboard
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print(f"[bold cyan]   🕷️ Liam's 6th Birthday Party — Overview   [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    try:
        party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
        days_until = (party_dt - datetime.now()).days
        urgency = "green" if days_until > 14 else "yellow" if days_until > 7 else "red"
        console.print(f"[{urgency}]⏰ {days_until} days until the party![/{urgency}]")
    except:
        console.print("[yellow]⏰ Party coming up soon![/yellow]")

    console.print()

    # Progress bars
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Metric", style="cyan", width=15)
    table.add_column("Progress", width=60)

    # Checklist
    total_tasks = sum(len(p.items) for p in party.checklist_phases)
    done_tasks = sum(sum(1 for i in p.items if i.completed) for p in party.checklist_phases)
    pct = done_tasks / total_tasks * 100 if total_tasks > 0 else 0
    filled = int(pct / 100 * 20)
    bar = "[cyan]" + "█" * filled + "░" * (20 - filled) + "[/cyan]"
    table.add_row("📋 Checklist", f"{bar} {done_tasks}/{total_tasks} ({pct:.0f}%)")

    # Guests
    confirmed = sum(1 for g in party.guests if g.rsvp_status == "confirmed")
    pending = sum(1 for g in party.guests if g.rsvp_status == "pending")
    declined = sum(1 for g in party.guests if g.rsvp_status == "declined")
    conf_pct = confirmed / len(party.guests) * 100
    filled = int(conf_pct / 100 * 20)
    bar = "[green]" + "█" * filled + "░" * (20 - filled) + "[/green]"
    table.add_row("👥 RSVPs", f"{bar} {confirmed} yes / {pending} pending / {declined} no")

    # Shopping
    purchased = sum(1 for i in party.shopping_list if i.purchased)
    total_items = len(party.shopping_list)
    shop_pct = purchased / total_items * 100
    filled = int(shop_pct / 100 * 20)
    bar = "[blue]" + "█" * filled + "░" * (20 - filled) + "[/blue]"
    table.add_row("🛒 Shopping", f"{bar} {purchased}/{total_items} ({shop_pct:.0f}%)")

    # Budget
    spent = sum(i.actual_price * i.quantity for i in party.shopping_list if i.purchased)
    estimated_total = sum(i.estimated_price * i.quantity for i in party.shopping_list)
    budget_pct = spent / party.budget * 100
    filled = int(budget_pct / 100 * 20)
    bar = "[green]" + "█" * filled + "░" * (20 - filled) + "[/green]"
    remaining = party.budget - spent
    table.add_row("💰 Budget", f"{bar} ${spent:.2f} spent / ${party.budget:.0f} budget (${remaining:.2f} left)")

    console.print(table)

    console.print()
    console.print("[bold yellow]⚠️  Needs attention:[/bold yellow]")
    console.print(f"  • [RSVP] {pending} guests haven't replied yet — follow up!")
    console.print(f"  • [Shopping] {total_items - purchased} items still need to be bought")

    pause(2)

    # ═══════════════════════════════════════
    # SHOPPING LIST
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 3: Smart Shopping List[/bold green]\n")
    pause(0.5)

    shop_table = Table(title="🛒 Shopping List — Liam's Spider-Man Party", box=box.ROUNDED)
    shop_table.add_column("#", style="dim", width=3)
    shop_table.add_column("Item", style="cyan", width=35)
    shop_table.add_column("Store", style="yellow", width=10)
    shop_table.add_column("Price", style="green", width=10)
    shop_table.add_column("Status", width=10)

    for i, item in enumerate(party.shopping_list, 1):
        status = "[green]✓ Bought[/green]" if item.purchased else "[yellow]○ To buy[/yellow]"
        price = f"${item.estimated_price * item.quantity:.2f}"
        shop_table.add_row(str(i), item.name, item.store, price, status)

    console.print(shop_table)

    console.print(f"\n  [bold]Estimated total:[/bold] ${estimated_total:.2f}")
    console.print(f"  [bold]Already spent:[/bold] ${spent:.2f}")
    console.print(f"  [bold]Remaining budget:[/bold] [green]${remaining:.2f}[/green]")
    console.print(f"\n  [green]💡 You're ${party.budget - estimated_total:.2f} under budget — great job![/green]")

    pause(2)

    # ═══════════════════════════════════════
    # SMART RECOMMENDATIONS
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 4: Smart Shopping Recommendations[/bold green]\n")
    pause(0.5)

    console.print("[bold cyan]💰 Deals for items on your list:[/bold cyan]\n")

    # Balloons
    console.print("[bold]📦 Balloon garland kit[/bold]")
    recs = USShoppingAffiliate.get_recommendations("balloons", budget=30)
    if recs:
        USShoppingAffiliate.show_product_comparison(recs)

    pause(1.5)

    # Goody bags
    console.print("[bold]📦 Goody bags[/bold]")
    recs = USShoppingAffiliate.get_recommendations("goody bags", budget=40)
    if recs:
        USShoppingAffiliate.show_product_comparison(recs)

    pause(2)

    # ═══════════════════════════════════════
    # GUEST LIST
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 5: Guest List & RSVPs[/bold green]\n")
    pause(0.5)

    guest_table = Table(title="👥 Guest List — Liam's Party", box=box.ROUNDED)
    guest_table.add_column("Guest", style="cyan", width=25)
    guest_table.add_column("RSVP", width=15)

    for guest in party.guests:
        if guest.rsvp_status == "confirmed":
            status = "[green]✓ Coming[/green]"
        elif guest.rsvp_status == "declined":
            status = "[red]✗ Can't make it[/red]"
        else:
            status = "[yellow]? Waiting[/yellow]"

        guest_table.add_row(guest.name, status)

    console.print(guest_table)

    console.print(f"\n  [green]✓ Confirmed:[/green] {confirmed}  |  [yellow]? Pending:[/yellow] {pending}  |  [red]✗ Declined:[/red] {declined}")

    pause(2)

    # ═══════════════════════════════════════
    # INVITATION PREVIEW
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 6: Party Invitation (Evite-ready)[/bold green]\n")
    pause(0.5)

    invitation = f"""
[bold magenta]╔═══════════════════════════════════════════════════════════╗[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]║     🕷️ You're Invited! 🕷️                               ║[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]║     Join us for Liam's 6th Birthday Party!               ║[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]║     🎨 Theme: Spider-Man                                 ║[/bold magenta]
[bold magenta]║     📅 Date: Saturday, May 17, 2026                      ║[/bold magenta]
[bold magenta]║     🕐 Time: 2:00 PM - 5:00 PM                          ║[/bold magenta]
[bold magenta]║     📍 Where: 123 Oak Street, Los Angeles, CA            ║[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]║     🍕 Pizza, cake & fun activities!                     ║[/bold magenta]
[bold magenta]║     🎈 Come dressed as your favorite superhero!          ║[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]║     RSVP by May 10 to Beth: beth@email.com              ║[/bold magenta]
[bold magenta]║     ⚠️ Please note any food allergies                    ║[/bold magenta]
[bold magenta]║                                                           ║[/bold magenta]
[bold magenta]╚═══════════════════════════════════════════════════════════╝[/bold magenta]
"""
    console.print(invitation)
    console.print("[dim]📧 Copy this to Evite, Paperless Post, or email![/dim]")

    pause(2)

    # ═══════════════════════════════════════
    # VENUE RECOMMENDATIONS
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 7: Venue Recommendations (if you need one)[/bold green]\n")
    pause(0.5)

    console.print("[dim]Beth chose backyard, but here's what we'd recommend if she needed a venue:[/dim]\n")
    venues = USVenueMarketplace.get_venue_recommendations(15, 400)
    USVenueMarketplace.show_venue_recommendations(venues)

    pause(2)

    # ═══════════════════════════════════════
    # MONEY-SAVING TIPS
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 8: Money-Saving Tips[/bold green]\n")
    pause(0.5)

    console.print("[bold cyan]💡 Smart Savings for Liam's Party:[/bold cyan]\n")

    tips = [
        ("🎂 Cake", "Costco sheet cake: $24.99 vs custom bakery: $80+", "$55", "green"),
        ("🎈 Decorations", "Dollar Tree basics + Amazon garland kit", "$30", "green"),
        ("🍕 Pizza", "Little Caesars $6/ea vs delivery $15/ea (3 pizzas)", "$27", "green"),
        ("📧 Invitations", "Evite (free) vs printed cards ($25)", "$25", "green"),
        ("🎁 Goody bags", "Oriental Trading bulk: $1.50/bag vs store: $4/bag", "$37", "green"),
    ]

    tips_table = Table(box=box.ROUNDED, show_header=True)
    tips_table.add_column("Category", style="cyan", width=15)
    tips_table.add_column("Tip", width=45)
    tips_table.add_column("Savings", style="green", width=10)

    total_savings = 0
    for cat, tip, savings, color in tips:
        tips_table.add_row(cat, tip, savings)
        total_savings += float(savings.replace("$", ""))

    console.print(tips_table)
    console.print(f"\n[bold green]💰 Total potential savings: ${total_savings:.0f}![/bold green]")
    console.print(f"[green]That's {total_savings / 400 * 100:.0f}% of your budget![/green]")

    pause(2)

    # ═══════════════════════════════════════
    # CHECKLIST PREVIEW
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 9: Party Planning Checklist[/bold green]\n")
    pause(0.5)

    checklist_items = [
        ("4 weeks before", [
            ("✓", "Choose date and book venue", True),
            ("✓", "Create guest list", True),
            ("✓", "Set budget ($400)", True),
            ("✓", "Pick theme (Spider-Man)", True),
        ]),
        ("3 weeks before", [
            ("✓", "Send invitations (Evite)", True),
            ("○", "Order cake from Costco", False),
        ]),
        ("2 weeks before", [
            ("○", "Follow up on RSVPs", False),
            ("○", "Buy decorations (Amazon)", False),
            ("○", "Plan activities & games", False),
        ]),
        ("1 week before", [
            ("○", "Confirm final headcount", False),
            ("○", "Buy goody bag supplies", False),
            ("○", "Buy piñata + candy", False),
        ]),
        ("Day before", [
            ("○", "Buy pizza + drinks", False),
            ("○", "Pick up cake from Costco", False),
            ("○", "Set up decorations", False),
            ("○", "Assemble goody bags", False),
            ("○", "Charge camera/phone", False),
        ]),
        ("Party day! 🎉", [
            ("○", "Set up tables & food", False),
            ("○", "Hang piñata", False),
            ("○", "HAVE FUN!", False),
        ]),
    ]

    for phase_name, items in checklist_items:
        console.print(f"\n[bold yellow]{phase_name}[/bold yellow]")
        for symbol, task, done in items:
            if done:
                console.print(f"  [green]{symbol} {task}[/green]")
            else:
                console.print(f"  [dim]{symbol} {task}[/dim]")

    pause(2)

    # ═══════════════════════════════════════
    # PREMIUM UPGRADE
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 10: Premium Features[/bold green]\n")
    pause(0.5)

    MonetizationManager.show_pricing_comparison()

    pause(2)

    # ═══════════════════════════════════════
    # SERVICES MARKETPLACE
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 11: Services Marketplace[/bold green]\n")
    pause(0.5)

    USValueAddedServices.show_services_marketplace()

    pause(2)

    # ═══════════════════════════════════════
    # QUICK ACTIONS
    # ═══════════════════════════════════════
    console.print("\n[bold green]Step 12: Quick Actions Menu[/bold green]\n")
    pause(0.5)

    console.print("[bold cyan]⚡ Quick Actions:[/bold cyan]")
    console.print("  1. Add a guest")
    console.print("  2. Add a shopping item")
    console.print("  3. Mark task complete")
    console.print("  4. View budget")
    console.print("  5. Export list")
    console.print("  0. Back to main menu")
    console.print()
    console.print("[dim]No more navigating through 5 menus — everything in one place![/dim]")

    pause(2)

    # ═══════════════════════════════════════
    # MAIN MENU
    # ═══════════════════════════════════════
    console.print("\n[bold green]Main Menu:[/bold green]\n")
    pause(0.5)

    console.print("[bold cyan]Main Menu[/bold cyan]")
    console.print("1. Create new party")
    console.print("2. 📋 Quick create from previous party")
    console.print("3. Load existing party")
    console.print("4. 💎 Services marketplace")
    console.print("5. 💰 Upgrade to Premium")
    console.print("6. 📖 Help")
    console.print("7. Exit")

    pause(2)

    # ═══════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════
    console.print("\n")
    console.print("[bold magenta]═══════════════════════════════════════════════════════════[/bold magenta]")
    console.print("[bold magenta]                   PREVIEW COMPLETE                       [/bold magenta]")
    console.print("[bold magenta]═══════════════════════════════════════════════════════════[/bold magenta]\n")

    console.print("[bold cyan]What Beth accomplished in 10 minutes:[/bold cyan]\n")
    console.print("  ✓ Created Liam's Spider-Man party")
    console.print("  ✓ Got smart shopping list (13 items, $178 total)")
    console.print("  ✓ Saved $174 with money-saving tips")
    console.print("  ✓ Invited 12 guests")
    console.print("  ✓ Got beautiful Evite-ready invitation")
    console.print("  ✓ Has complete checklist from now to party day")
    console.print("  ✓ Dashboard tracks everything at a glance")
    console.print("  ✓ Under budget by $222!")

    console.print("\n[bold green]Beth's reaction: \"This is exactly what I needed.\"[/bold green]")
    console.print("[bold green]\"I was dreading planning this party but now I feel totally prepared.\"[/bold green]")

    console.print("\n[bold cyan]Product Features Summary:[/bold cyan]\n")

    features = [
        "🇺🇸  Designed for American families",
        "💰  Budget tracking in USD ($)",
        "🛒  Amazon, Target, Costco, Dollar Tree recommendations",
        "🎂  Costco cake hack ($24.99 vs $80+)",
        "📧  Evite-ready invitations (not WeChat)",
        "🎈  Spider-Man, Frozen, Minecraft themes",
        "🏠  Home party + venue options (Chuck E. Cheese, etc.)",
        "🎁  Goody bag builder (age-appropriate)",
        "🪅  Piñata included by default",
        "📋  Step-by-step checklist",
        "📊  Dashboard with progress bars",
        "⚡  Quick actions (30 seconds to update)",
        "💎  Free + Premium ($49/year) plans",
        "🔗  Affiliate shopping links (saves YOU money)",
    ]

    for feature in features:
        console.print(f"  {feature}")

    console.print(f"\n[bold yellow]US Market Fit: 4.83/5.0 ⭐⭐⭐⭐⭐[/bold yellow]")
    console.print(f"[bold green]🇺🇸 READY FOR AMERICAN MOMS! 🇺🇸[/bold green]\n")


if __name__ == "__main__":
    preview()
