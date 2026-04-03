#!/usr/bin/env python3
"""
Birthday Party Planner - Web Version (US Market)
Flask-based web application for localhost preview
"""
import os
import sys
import json
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from us_config import *
from us_monetization import SubscriptionTier

app = Flask(__name__)

# ─── Demo Data ───────────────────────────────────────────

DEMO_PARTY = {
    "child_name": "Liam",
    "child_age": 6,
    "party_date": (datetime.now() + timedelta(days=44)).strftime("%Y-%m-%d"),
    "party_time": "2:00 PM",
    "venue": "Backyard",
    "venue_address": "123 Oak Street, Los Angeles, CA 90001",
    "budget": 400.00,
    "theme": "Spider-Man",
    "guest_count_expected": 15,
    "guests": [
        {"name": "Emma Johnson", "email": "emma.parent@email.com", "rsvp": "confirmed", "dietary": ""},
        {"name": "Noah Williams", "email": "noah.parent@email.com", "rsvp": "confirmed", "dietary": "Peanut allergy"},
        {"name": "Olivia Brown", "email": "olivia.parent@email.com", "rsvp": "confirmed", "dietary": ""},
        {"name": "James Davis", "email": "james.parent@email.com", "rsvp": "confirmed", "dietary": "Gluten-free"},
        {"name": "Sophia Miller", "email": "sophia.parent@email.com", "rsvp": "confirmed", "dietary": ""},
        {"name": "Benjamin Wilson", "email": "ben.parent@email.com", "rsvp": "confirmed", "dietary": ""},
        {"name": "Ava Moore", "email": "ava.parent@email.com", "rsvp": "confirmed", "dietary": ""},
        {"name": "Lucas Taylor", "email": "lucas.parent@email.com", "rsvp": "pending", "dietary": ""},
        {"name": "Mia Anderson", "email": "mia.parent@email.com", "rsvp": "pending", "dietary": ""},
        {"name": "Henry Thomas", "email": "henry.parent@email.com", "rsvp": "pending", "dietary": ""},
        {"name": "Charlotte Jackson", "email": "", "rsvp": "pending", "dietary": ""},
        {"name": "Alexander White", "email": "alex.parent@email.com", "rsvp": "declined", "dietary": ""},
    ],
    "shopping_list": [
        {"name": "Spider-Man cake (Costco)", "category": "Food", "qty": 1, "price": 24.99, "store": "Costco", "bought": True, "actual": 22.99},
        {"name": "Pizza (3 large)", "category": "Food", "qty": 3, "price": 8.99, "store": "Little Caesars", "bought": True, "actual": 6.49},
        {"name": "Juice boxes (24-pack)", "category": "Food", "qty": 2, "price": 6.49, "store": "Costco", "bought": True, "actual": 5.99},
        {"name": "Spider-Man plates & napkins set", "category": "Tableware", "qty": 1, "price": 19.99, "store": "Amazon", "bought": True, "actual": 19.99},
        {"name": "Balloon garland kit (red & blue)", "category": "Decorations", "qty": 1, "price": 15.99, "store": "Amazon", "bought": False, "actual": 0},
        {"name": "Spider-Man banner", "category": "Decorations", "qty": 1, "price": 8.99, "store": "Amazon", "bought": False, "actual": 0},
        {"name": "Spider-Man piñata", "category": "Activities", "qty": 1, "price": 16.99, "store": "Amazon", "bought": False, "actual": 0},
        {"name": "Piñata candy (2 lbs)", "category": "Activities", "qty": 1, "price": 12.99, "store": "Target", "bought": False, "actual": 0},
        {"name": "Goody bags pre-filled (15-pack)", "category": "Goody Bags", "qty": 1, "price": 24.99, "store": "Amazon", "bought": False, "actual": 0},
        {"name": "Bubbles (12-pack party favors)", "category": "Goody Bags", "qty": 1, "price": 9.99, "store": "Dollar Tree", "bought": False, "actual": 0},
        {"name": "Paper cups (50ct)", "category": "Tableware", "qty": 1, "price": 4.99, "store": "Target", "bought": False, "actual": 0},
        {"name": "Plastic utensils", "category": "Tableware", "qty": 1, "price": 3.99, "store": "Target", "bought": False, "actual": 0},
        {"name": "Thank you cards (15-pack)", "category": "Misc", "qty": 1, "price": 7.99, "store": "Target", "bought": False, "actual": 0},
    ],
    "checklist": [
        {"phase": "4 weeks before", "tasks": [
            {"task": "Choose date and book venue", "done": True, "important": True},
            {"task": "Create guest list", "done": True, "important": True},
            {"task": "Set budget ($400)", "done": True, "important": True},
            {"task": "Pick theme (Spider-Man)", "done": True, "important": False},
        ]},
        {"phase": "3 weeks before", "tasks": [
            {"task": "Send invitations via Evite", "done": True, "important": True},
            {"task": "Order cake from Costco", "done": False, "important": True},
        ]},
        {"phase": "2 weeks before", "tasks": [
            {"task": "Follow up on RSVPs", "done": False, "important": True},
            {"task": "Buy decorations on Amazon", "done": False, "important": False},
            {"task": "Plan activities & games", "done": False, "important": False},
        ]},
        {"phase": "1 week before", "tasks": [
            {"task": "Confirm final headcount", "done": False, "important": True},
            {"task": "Buy goody bag supplies", "done": False, "important": False},
            {"task": "Buy piñata + candy", "done": False, "important": False},
        ]},
        {"phase": "Day before", "tasks": [
            {"task": "Order pizza", "done": False, "important": True},
            {"task": "Pick up cake from Costco", "done": False, "important": True},
            {"task": "Set up decorations", "done": False, "important": False},
            {"task": "Assemble goody bags", "done": False, "important": False},
            {"task": "Charge camera/phone", "done": False, "important": False},
        ]},
        {"phase": "Party day! 🎉", "tasks": [
            {"task": "Set up tables & food area", "done": False, "important": True},
            {"task": "Hang piñata", "done": False, "important": False},
            {"task": "HAVE FUN!", "done": False, "important": True},
        ]},
    ],
    "saving_tips": [
        {"category": "🎂 Cake", "tip": "Costco sheet cake: $24.99 vs custom bakery: $80+", "savings": 55},
        {"category": "🎈 Decorations", "tip": "Dollar Tree basics + Amazon garland kit", "savings": 30},
        {"category": "🍕 Pizza", "tip": "Little Caesars $6/ea vs delivery $15/ea", "savings": 27},
        {"category": "📧 Invitations", "tip": "Evite (free!) vs printed cards ($25)", "savings": 25},
        {"category": "🎁 Goody bags", "tip": "Oriental Trading bulk: $1.50/bag vs store: $4/bag", "savings": 37},
    ]
}


# ─── Template ────────────────────────────────────────────

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎉 Birthday Party Planner</title>
    <style>
        :root {
            --primary: #6C5CE7;
            --primary-light: #A29BFE;
            --accent: #FD79A8;
            --success: #00B894;
            --warning: #FDCB6E;
            --danger: #E17055;
            --dark: #2D3436;
            --gray: #636E72;
            --light: #F8F9FA;
            --white: #FFFFFF;
            --shadow: 0 2px 15px rgba(0,0,0,0.08);
            --radius: 16px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #F8F9FA 0%, #E8E6F0 100%);
            color: var(--dark);
            min-height: 100vh;
        }

        /* ── Navigation ── */
        .navbar {
            background: var(--white);
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .navbar .logo {
            font-size: 24px;
            font-weight: 800;
            color: var(--primary);
        }
        .navbar nav a {
            margin-left: 24px;
            text-decoration: none;
            color: var(--gray);
            font-weight: 500;
            transition: color 0.2s;
        }
        .navbar nav a:hover, .navbar nav a.active { color: var(--primary); }
        .navbar .premium-btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
        }

        /* ── Main Content ── */
        .container { max-width: 1200px; margin: 0 auto; padding: 24px; }

        /* ── Hero Section ── */
        .hero {
            background: linear-gradient(135deg, var(--primary) 0%, #8B5CF6 50%, var(--accent) 100%);
            color: white;
            border-radius: var(--radius);
            padding: 48px;
            margin-bottom: 24px;
            text-align: center;
        }
        .hero h1 { font-size: 36px; margin-bottom: 8px; }
        .hero .subtitle { opacity: 0.9; font-size: 18px; margin-bottom: 24px; }
        .hero .countdown {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 12px 32px;
            border-radius: 30px;
            font-size: 24px;
            font-weight: 700;
            backdrop-filter: blur(10px);
        }

        /* ── Cards ── */
        .card {
            background: var(--white);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 24px;
            margin-bottom: 20px;
        }
        .card h2 {
            font-size: 20px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ── Stats Grid ── */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: var(--white);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 20px;
        }
        .stat-card .label { color: var(--gray); font-size: 14px; margin-bottom: 4px; }
        .stat-card .value { font-size: 28px; font-weight: 700; }
        .stat-card .sub { color: var(--gray); font-size: 13px; margin-top: 4px; }

        /* ── Progress Bar ── */
        .progress-bar {
            height: 10px;
            background: #EDF2F7;
            border-radius: 5px;
            overflow: hidden;
            margin: 8px 0;
        }
        .progress-bar .fill {
            height: 100%;
            border-radius: 5px;
            transition: width 0.6s ease;
        }
        .fill-green { background: var(--success); }
        .fill-blue { background: #4299E1; }
        .fill-purple { background: var(--primary); }
        .fill-pink { background: var(--accent); }

        /* ── Guest List ── */
        .guest-list { width: 100%; border-collapse: collapse; }
        .guest-list th {
            text-align: left;
            padding: 12px;
            border-bottom: 2px solid #EDF2F7;
            color: var(--gray);
            font-size: 13px;
            text-transform: uppercase;
        }
        .guest-list td {
            padding: 12px;
            border-bottom: 1px solid #EDF2F7;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-green { background: #C6F6D5; color: #22543D; }
        .badge-yellow { background: #FEFCBF; color: #744210; }
        .badge-red { background: #FED7D7; color: #822727; }
        .badge-blue { background: #BEE3F8; color: #2A4365; }

        /* ── Shopping List ── */
        .shop-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #EDF2F7;
        }
        .shop-item:last-child { border-bottom: none; }
        .shop-check {
            width: 24px; height: 24px;
            border-radius: 50%;
            border: 2px solid #CBD5E0;
            margin-right: 12px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .shop-check.done {
            background: var(--success);
            border-color: var(--success);
            color: white;
            font-size: 14px;
        }
        .shop-name { flex: 1; }
        .shop-name.done-text { text-decoration: line-through; color: var(--gray); }
        .shop-store {
            font-size: 12px;
            color: var(--gray);
            margin-right: 16px;
        }
        .shop-price { font-weight: 600; min-width: 60px; text-align: right; }

        /* ── Checklist ── */
        .checklist-phase { margin-bottom: 20px; }
        .phase-title {
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 8px;
            font-size: 16px;
        }
        .check-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            gap: 10px;
        }
        .check-icon { font-size: 18px; width: 24px; text-align: center; }
        .check-text.done { text-decoration: line-through; color: var(--gray); }

        /* ── Invitation ── */
        .invitation-card {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
            border-radius: var(--radius);
            padding: 40px;
            text-align: center;
            margin: 20px 0;
        }
        .invitation-card h3 { font-size: 28px; margin-bottom: 16px; }
        .invitation-card p { font-size: 16px; margin-bottom: 8px; opacity: 0.95; }
        .invitation-card .detail { font-size: 18px; margin-bottom: 6px; }
        .invitation-card .rsvp-note {
            margin-top: 20px;
            background: rgba(255,255,255,0.15);
            padding: 12px 24px;
            border-radius: 10px;
            font-size: 14px;
        }

        /* ── Tips ── */
        .tip-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 0;
            border-bottom: 1px solid #EDF2F7;
        }
        .tip-item:last-child { border-bottom: none; }
        .tip-cat { font-weight: 600; min-width: 140px; }
        .tip-text { flex: 1; color: var(--gray); margin: 0 16px; }
        .tip-savings {
            background: #C6F6D5;
            color: #22543D;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 700;
            white-space: nowrap;
        }

        /* ── Pricing ── */
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .price-card {
            border: 2px solid #EDF2F7;
            border-radius: var(--radius);
            padding: 32px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .price-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(0,0,0,0.12); }
        .price-card.featured { border-color: var(--primary); position: relative; }
        .price-card.featured::before {
            content: "MOST POPULAR";
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary);
            color: white;
            padding: 4px 16px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .price-card h3 { font-size: 22px; margin-bottom: 8px; }
        .price-card .price { font-size: 36px; font-weight: 800; color: var(--primary); }
        .price-card .price span { font-size: 16px; font-weight: 400; color: var(--gray); }
        .price-card ul { list-style: none; margin: 20px 0; text-align: left; }
        .price-card ul li { padding: 8px 0; border-bottom: 1px solid #EDF2F7; font-size: 14px; }
        .price-card ul li::before { content: "✓ "; color: var(--success); font-weight: 700; }
        .cta-btn {
            display: inline-block;
            padding: 12px 32px;
            border-radius: 25px;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            border: none;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .cta-btn:hover { transform: scale(1.05); }
        .cta-primary { background: var(--primary); color: white; }
        .cta-outline { background: white; color: var(--primary); border: 2px solid var(--primary); }

        /* ── Sections ── */
        .section-title {
            font-size: 14px;
            text-transform: uppercase;
            color: var(--gray);
            letter-spacing: 1px;
            margin-bottom: 16px;
        }

        .two-col {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            padding: 40px;
            color: var(--gray);
            font-size: 14px;
        }

        /* ── Responsive ── */
        @media (max-width: 768px) {
            .container { padding: 12px; }
            .hero { padding: 24px; }
            .hero h1 { font-size: 24px; }
            .two-col { grid-template-columns: 1fr; }
            .navbar nav { display: none; }
            .stats-grid { grid-template-columns: 1fr 1fr; }
        }
    </style>
</head>
<body>

<!-- ── NAVBAR ── -->
<div class="navbar">
    <div class="logo">🎉 Party Planner</div>
    <nav>
        <a href="#dashboard" class="active">Dashboard</a>
        <a href="#guests">Guests</a>
        <a href="#shopping">Shopping</a>
        <a href="#checklist">Checklist</a>
        <a href="#invitation">Invitation</a>
        <a href="#pricing">Pricing</a>
    </nav>
    <a href="#pricing" class="premium-btn">✨ Go Premium</a>
</div>

<div class="container">

<!-- ── HERO ── -->
<div class="hero" id="dashboard">
    <h1>🕷️ {{ party.child_name }}'s {{ party.child_age }}th Birthday Party</h1>
    <div class="subtitle">{{ party.theme }} Theme &bull; {{ party.venue }}, {{ party.venue_address }}</div>
    <div class="countdown">⏰ {{ days_until }} days to go!</div>
</div>

<!-- ── STATS ── -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="label">👥 Guests</div>
        <div class="value">{{ confirmed }}<span style="font-size:16px;color:var(--gray)"> / {{ total_guests }}</span></div>
        <div class="progress-bar"><div class="fill fill-green" style="width:{{ (confirmed/total_guests*100)|round }}%"></div></div>
        <div class="sub">{{ confirmed }} confirmed &bull; {{ pending }} pending &bull; {{ declined }} declined</div>
    </div>
    <div class="stat-card">
        <div class="label">🛒 Shopping</div>
        <div class="value">{{ bought_items }}<span style="font-size:16px;color:var(--gray)"> / {{ total_items }}</span></div>
        <div class="progress-bar"><div class="fill fill-blue" style="width:{{ (bought_items/total_items*100)|round }}%"></div></div>
        <div class="sub">{{ total_items - bought_items }} items left to buy</div>
    </div>
    <div class="stat-card">
        <div class="label">💰 Budget</div>
        <div class="value">${{ "%.2f"|format(spent) }}<span style="font-size:16px;color:var(--gray)"> / ${{ "%.0f"|format(party.budget) }}</span></div>
        <div class="progress-bar"><div class="fill fill-purple" style="width:{{ (spent/party.budget*100)|round }}%"></div></div>
        <div class="sub" style="color:var(--success)">${{ "%.2f"|format(party.budget - spent) }} remaining — under budget! 🎉</div>
    </div>
    <div class="stat-card">
        <div class="label">📋 Checklist</div>
        <div class="value">{{ tasks_done }}<span style="font-size:16px;color:var(--gray)"> / {{ total_tasks }}</span></div>
        <div class="progress-bar"><div class="fill fill-pink" style="width:{{ (tasks_done/total_tasks*100)|round }}%"></div></div>
        <div class="sub">{{ total_tasks - tasks_done }} tasks remaining</div>
    </div>
</div>

<!-- ── ALERTS ── -->
{% if pending > 0 %}
<div class="card" style="border-left: 4px solid var(--warning); background: #FFFDF0;">
    <strong>⚠️ Needs Attention:</strong>
    {{ pending }} guest(s) haven't RSVP'd yet — consider a friendly follow-up!
    {% for g in party.guests %}{% if g.rsvp == "pending" and g.email %} &bull; {{ g.name }}{% endif %}{% endfor %}
</div>
{% endif %}

<!-- ── TWO COLUMN: GUESTS + SHOPPING ── -->
<div class="two-col">

<!-- GUEST LIST -->
<div class="card" id="guests">
    <h2>👥 Guest List</h2>
    <table class="guest-list">
        <thead>
            <tr><th>Name</th><th>RSVP</th><th>Dietary</th></tr>
        </thead>
        <tbody>
            {% for g in party.guests %}
            <tr>
                <td><strong>{{ g.name }}</strong><br><span style="font-size:12px;color:var(--gray)">{{ g.email }}</span></td>
                <td>
                    {% if g.rsvp == "confirmed" %}<span class="badge badge-green">✓ Coming</span>
                    {% elif g.rsvp == "declined" %}<span class="badge badge-red">✗ Can't make it</span>
                    {% else %}<span class="badge badge-yellow">? Pending</span>{% endif %}
                </td>
                <td>{% if g.dietary %}<span class="badge badge-blue">{{ g.dietary }}</span>{% else %}<span style="color:#ccc">—</span>{% endif %}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- SHOPPING LIST -->
<div class="card" id="shopping">
    <h2>🛒 Shopping List</h2>
    {% for item in party.shopping_list %}
    <div class="shop-item">
        <div class="shop-check {{ 'done' if item.bought else '' }}">{{ '✓' if item.bought else '' }}</div>
        <div class="shop-name {{ 'done-text' if item.bought else '' }}">
            {{ item.name }}
        </div>
        <div class="shop-store">{{ item.store }}</div>
        <div class="shop-price">${{ "%.2f"|format(item.price * item.qty) }}</div>
    </div>
    {% endfor %}
    <div style="margin-top:16px; padding-top:16px; border-top:2px solid #EDF2F7; display:flex; justify-content:space-between">
        <span>Estimated total:</span>
        <strong>${{ "%.2f"|format(estimated_total) }}</strong>
    </div>
</div>
</div>

<!-- ── MONEY SAVING TIPS ── -->
<div class="card">
    <h2>💡 Money-Saving Tips</h2>
    {% for tip in party.saving_tips %}
    <div class="tip-item">
        <div class="tip-cat">{{ tip.category }}</div>
        <div class="tip-text">{{ tip.tip }}</div>
        <div class="tip-savings">Save ${{ tip.savings }}</div>
    </div>
    {% endfor %}
    <div style="margin-top:16px; padding-top:16px; border-top:2px solid #EDF2F7; text-align:right">
        <strong style="color:var(--success); font-size:18px">💰 Total potential savings: ${{ total_savings }}!</strong>
    </div>
</div>

<!-- ── INVITATION ── -->
<div id="invitation">
    <div class="section-title">📧 Party Invitation (Evite-ready)</div>
    <div class="invitation-card">
        <p style="font-size:40px; margin-bottom:16px">🕷️</p>
        <h3>You're Invited!</h3>
        <p style="font-size:22px; margin-bottom:20px">Join us for <strong>{{ party.child_name }}'s {{ party.child_age }}th Birthday Party!</strong></p>
        <div class="detail">🎨 Theme: {{ party.theme }}</div>
        <div class="detail">📅 {{ party_date_formatted }}</div>
        <div class="detail">🕐 {{ party.party_time }} – 5:00 PM</div>
        <div class="detail">📍 {{ party.venue_address }}</div>
        <div class="detail">🍕 Pizza, cake & fun activities!</div>
        <p style="margin-top:16px; font-size:18px">🦸 Come dressed as your favorite superhero!</p>
        <div class="rsvp-note">
            📧 RSVP by email &bull; ⚠️ Please let us know about any food allergies
        </div>
    </div>
</div>

<!-- ── CHECKLIST ── -->
<div class="card" id="checklist">
    <h2>📋 Party Planning Checklist</h2>
    {% for phase in party.checklist %}
    <div class="checklist-phase">
        <div class="phase-title">{{ phase.phase }}</div>
        {% for item in phase.tasks %}
        <div class="check-item">
            <div class="check-icon">{{ '✅' if item.done else '⬜' }}</div>
            <div class="check-text {{ 'done' if item.done else '' }}">
                {{ item.task }}
                {% if item.important and not item.done %}<span class="badge badge-yellow" style="margin-left:8px">Important</span>{% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
</div>

<!-- ── PRICING ── -->
<div id="pricing">
    <div class="section-title">💎 Choose Your Plan</div>
    <div class="pricing-grid">
        <div class="price-card">
            <h3>Free</h3>
            <div class="price">$0</div>
            <ul>
                <li>1 active party</li>
                <li>Up to 30 guests</li>
                <li>Basic shopping list</li>
                <li>Text export</li>
                <li>3 invitation templates</li>
            </ul>
            <div class="cta-btn cta-outline">Current Plan</div>
        </div>
        <div class="price-card featured">
            <h3>Premium</h3>
            <div class="price">$49<span>/year</span></div>
            <ul>
                <li>Unlimited parties</li>
                <li>Up to 100 guests</li>
                <li>PDF & Excel export</li>
                <li>30+ invitation templates</li>
                <li>Shopping deal alerts</li>
                <li>Ad-free experience</li>
                <li>Priority support</li>
            </ul>
            <div class="cta-btn cta-primary">Upgrade Now</div>
        </div>
        <div class="price-card">
            <h3>Party Pro</h3>
            <div class="price">$199<span>/year</span></div>
            <ul>
                <li>Everything in Premium</li>
                <li>Unlimited guests</li>
                <li>Multi-user collaboration</li>
                <li>Vendor network access</li>
                <li>Dedicated account manager</li>
                <li>API access</li>
            </ul>
            <div class="cta-btn cta-outline">Contact Sales</div>
        </div>
    </div>
    <p style="text-align:center; margin-top:16px; color:var(--gray)">
        💡 Premium pays for itself: save $50+ per party in shopping deals alone!
    </p>
</div>

</div>

<!-- ── FOOTER ── -->
<div class="footer">
    <p>🎉 Birthday Party Planner &bull; Made with ❤️ for busy parents</p>
    <p style="margin-top:8px">Plan better parties. Save time. Save money.</p>
</div>

</body>
</html>
"""


# ─── Routes ──────────────────────────────────────────────

class DotDict(dict):
    """Allow dict.key access for Jinja templates"""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

def to_dot(d):
    if isinstance(d, dict):
        return DotDict({k: to_dot(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [to_dot(i) for i in d]
    return d


@app.route("/")
def index():
    party = to_dot(DEMO_PARTY)

    # Calculate stats
    confirmed = sum(1 for g in party.guests if g.rsvp == "confirmed")
    pending = sum(1 for g in party.guests if g.rsvp == "pending")
    declined = sum(1 for g in party.guests if g.rsvp == "declined")
    total_guests = len(party.guests)

    bought_items = sum(1 for i in party.shopping_list if i.bought)
    total_items = len(party.shopping_list)

    spent = sum(i.actual * i.qty for i in party.shopping_list if i.bought)
    estimated_total = sum(i.price * i.qty for i in party.shopping_list)

    total_tasks = sum(len(p.tasks) for p in party.checklist)
    tasks_done = sum(sum(1 for i in p.tasks if i.done) for p in party.checklist)

    total_savings = sum(t.savings for t in party.saving_tips)

    # Days until party
    try:
        party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
        days_until = (party_dt - datetime.now()).days
    except:
        days_until = 44

    # Format date
    try:
        party_dt = datetime.strptime(party.party_date, "%Y-%m-%d")
        party_date_formatted = party_dt.strftime("Saturday, %B %d, %Y")
    except:
        party_date_formatted = party.party_date

    return render_template_string(
        HTML_TEMPLATE,
        party=party,
        confirmed=confirmed,
        pending=pending,
        declined=declined,
        total_guests=total_guests,
        bought_items=bought_items,
        total_items=total_items,
        spent=spent,
        estimated_total=estimated_total,
        total_tasks=total_tasks,
        tasks_done=tasks_done,
        total_savings=total_savings,
        days_until=days_until,
        party_date_formatted=party_date_formatted,
    )


if __name__ == "__main__":
    print("\n🎉 Birthday Party Planner — US Edition")
    print("=" * 50)
    print("🌐 Open in your browser: http://localhost:5000")
    print("=" * 50)
    print("\nPress Ctrl+C to stop the server\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
