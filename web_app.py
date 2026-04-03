#!/usr/bin/env python3
"""
Birthday Party Planner - US Market
Zero-registration flow: fill form → get shareable link → send to guests
Revenue: Amazon affiliate commissions (tag=partyplan-20)
"""
import os
import json
import base64
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ─── Theme Data ──────────────────────────────────────────

THEMES = {
    "Spider-Man": {
        "emoji": "🕷️",
        "colors": ("#E31B23", "#003399"),
        "gradient": "linear-gradient(135deg, #E31B23 0%, #003399 100%)",
        "items": [
            "Spider-Man birthday cake",
            "Spider-Man plates and napkins set",
            "Spider-Man balloon garland kit red blue",
            "Spider-Man banner decoration",
            "Spider-Man pinata",
            "Spider-Man goody bags pre-filled",
            "Spider-Man tablecloth",
            "pinata candy 2 lbs assorted",
            "bubbles party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
    "Frozen": {
        "emoji": "❄️",
        "colors": ("#A8D8EA", "#5B86E5"),
        "gradient": "linear-gradient(135deg, #A8D8EA 0%, #5B86E5 100%)",
        "items": [
            "Frozen birthday cake topper",
            "Frozen plates and napkins set",
            "Frozen balloon garland kit blue silver",
            "Frozen banner decoration",
            "Frozen pinata",
            "Frozen goody bags pre-filled",
            "snowflake tablecloth decoration",
            "pinata candy 2 lbs assorted",
            "bubbles party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
    "Unicorn": {
        "emoji": "🦄",
        "colors": ("#F9A8D4", "#C084FC"),
        "gradient": "linear-gradient(135deg, #F9A8D4 0%, #C084FC 100%)",
        "items": [
            "unicorn birthday cake topper",
            "unicorn plates and napkins set",
            "rainbow balloon garland kit",
            "unicorn banner decoration",
            "unicorn pinata",
            "unicorn goody bags pre-filled",
            "rainbow tablecloth party",
            "pinata candy 2 lbs assorted",
            "bubbles party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
    "Dinosaur": {
        "emoji": "🦕",
        "colors": ("#4ADE80", "#166534"),
        "gradient": "linear-gradient(135deg, #4ADE80 0%, #166534 100%)",
        "items": [
            "dinosaur birthday cake topper",
            "dinosaur plates and napkins set",
            "green balloon garland kit",
            "dinosaur banner decoration",
            "dinosaur pinata",
            "dinosaur goody bags pre-filled",
            "jungle green tablecloth",
            "pinata candy 2 lbs assorted",
            "dinosaur figurines party favors",
            "thank you cards kids 24 pack",
        ],
    },
    "Princess": {
        "emoji": "👸",
        "colors": ("#FCD34D", "#F472B6"),
        "gradient": "linear-gradient(135deg, #FCD34D 0%, #F472B6 100%)",
        "items": [
            "princess birthday cake topper",
            "princess plates and napkins set",
            "pink gold balloon garland kit",
            "princess banner decoration",
            "princess pinata",
            "princess goody bags pre-filled",
            "pink tablecloth party",
            "pinata candy 2 lbs assorted",
            "tiara party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
    "Paw Patrol": {
        "emoji": "🐾",
        "colors": ("#EF4444", "#3B82F6"),
        "gradient": "linear-gradient(135deg, #EF4444 0%, #3B82F6 100%)",
        "items": [
            "Paw Patrol birthday cake topper",
            "Paw Patrol plates and napkins set",
            "Paw Patrol balloon garland kit",
            "Paw Patrol banner decoration",
            "Paw Patrol pinata",
            "Paw Patrol goody bags pre-filled",
            "Paw Patrol tablecloth",
            "pinata candy 2 lbs assorted",
            "bubbles party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
    "Minecraft": {
        "emoji": "⛏️",
        "colors": ("#5D8233", "#3E2723"),
        "gradient": "linear-gradient(135deg, #5D8233 0%, #3E2723 100%)",
        "items": [
            "Minecraft birthday cake topper",
            "Minecraft plates and napkins set",
            "green black balloon garland kit",
            "Minecraft banner decoration",
            "Minecraft pinata",
            "Minecraft goody bags pre-filled",
            "green tablecloth party",
            "pinata candy 2 lbs assorted",
            "Minecraft party favors",
            "thank you cards kids 24 pack",
        ],
    },
    "Rainbow": {
        "emoji": "🌈",
        "colors": ("#F97316", "#8B5CF6"),
        "gradient": "linear-gradient(135deg, #F97316 0%, #FBBF24 33%, #4ADE80 66%, #8B5CF6 100%)",
        "items": [
            "rainbow birthday cake topper",
            "rainbow plates and napkins set",
            "rainbow balloon garland kit",
            "rainbow banner decoration",
            "colorful pinata",
            "rainbow goody bags pre-filled",
            "rainbow tablecloth party",
            "pinata candy 2 lbs assorted",
            "bubbles party favors 12 pack",
            "thank you cards kids 24 pack",
        ],
    },
}

AFFILIATE_TAG = "partyplan-20"

def amazon_url(query):
    import urllib.parse
    q = urllib.parse.quote_plus(query)
    return f"https://www.amazon.com/s?k={q}&tag={AFFILIATE_TAG}"

def encode_party(data):
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_party(b64):
    return json.loads(base64.urlsafe_b64decode(b64.encode()).decode())


# ─── Landing Page ─────────────────────────────────────────

LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Birthday Party Planner — Create in 60 Seconds</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.wrap { max-width: 560px; width: 100%; }
.logo { text-align:center; color:white; margin-bottom:32px; }
.logo h1 { font-size:36px; font-weight:900; }
.logo p { font-size:18px; opacity:0.9; margin-top:8px; }
.steps { display:flex; justify-content:center; gap:32px; margin-bottom:24px; }
.step { text-align:center; color:white; opacity:0.85; }
.step .num { width:32px; height:32px; background:rgba(255,255,255,0.3);
  border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-weight:700; margin:0 auto 4px; font-size:14px; }
.step .lbl { font-size:12px; }
.card {
  background:white;
  border-radius:20px;
  padding:36px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.card h2 { font-size:22px; margin-bottom:24px; color:#1a1a2e; }
.row { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.field { margin-bottom:16px; }
.field label { display:block; font-size:13px; font-weight:600; color:#555; margin-bottom:6px; }
.field input, .field select {
  width:100%; padding:12px 14px;
  border:2px solid #E5E7EB; border-radius:10px;
  font-size:15px; color:#1a1a2e;
  transition: border-color 0.2s;
  background: white;
}
.field input:focus, .field select:focus {
  outline:none; border-color:#667EEA;
}
.optional { font-size:11px; color:#9CA3AF; font-weight:400; }
.submit-btn {
  width:100%; padding:16px;
  background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
  color:white; border:none; border-radius:12px;
  font-size:18px; font-weight:700; cursor:pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  margin-top:8px;
}
.submit-btn:hover { transform:translateY(-2px); box-shadow:0 8px 25px rgba(102,126,234,0.4); }
.note { text-align:center; margin-top:16px; color:#9CA3AF; font-size:13px; }
.note a { color:#667EEA; }
@media (max-width: 480px) { .row { grid-template-columns:1fr; } .card { padding:24px; } }
</style>
</head>
<body>
<div class="wrap">
  <div class="logo">
    <h1>🎉 Party Planner</h1>
    <p>Plan your child's birthday in 60 seconds</p>
  </div>
  <div class="steps">
    <div class="step"><div class="num">1</div><div class="lbl">Fill form</div></div>
    <div class="step"><div class="num">2</div><div class="lbl">Get link</div></div>
    <div class="step"><div class="num">3</div><div class="lbl">Share!</div></div>
  </div>
  <div class="card">
    <h2>Create Your Party Plan</h2>
    <form method="POST" action="/create">
      <div class="row">
        <div class="field">
          <label>Child's Name</label>
          <input name="name" placeholder="Emma" required>
        </div>
        <div class="field">
          <label>Age Turning</label>
          <input name="age" type="number" min="1" max="16" placeholder="6" required>
        </div>
      </div>
      <div class="row">
        <div class="field">
          <label>Party Date</label>
          <input name="date" type="date" required>
        </div>
        <div class="field">
          <label>Start Time</label>
          <input name="time" type="time" value="14:00" required>
        </div>
      </div>
      <div class="field">
        <label>Venue / Location</label>
        <input name="venue" placeholder="Our backyard, 123 Maple St, Austin TX" required>
      </div>
      <div class="field">
        <label>Party Theme</label>
        <select name="theme" required>
          {% for t, d in themes.items() %}
          <option value="{{ t }}">{{ d.emoji }} {{ t }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="field">
        <label>Your Email <span class="optional">(optional — to save your party later)</span></label>
        <input name="email" type="email" placeholder="parent@email.com">
      </div>
      <button type="submit" class="submit-btn">Create My Party Plan →</button>
    </form>
    <div class="note">No account needed &bull; Free forever &bull; <a href="#">How it works</a></div>
  </div>
</div>
</body>
</html>"""


# ─── Host Dashboard ────────────────────────────────────────

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ name }}'s Party Plan — Birthday Party Planner</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #F3F4F6;
  color: #1F2937;
}
.navbar {
  background:white; padding:14px 24px;
  display:flex; justify-content:space-between; align-items:center;
  box-shadow:0 1px 4px rgba(0,0,0,0.08); position:sticky; top:0; z-index:10;
}
.nav-logo { font-size:20px; font-weight:800; color:#667EEA; }
.nav-new { background:#667EEA; color:white; padding:8px 18px; border-radius:20px;
  text-decoration:none; font-size:14px; font-weight:600; }
.hero {
  background: {{ gradient }};
  color:white; padding:40px 24px; text-align:center;
}
.hero h1 { font-size:32px; font-weight:900; margin-bottom:6px; }
.hero .sub { font-size:16px; opacity:0.9; margin-bottom:24px; }
.hero .countdown {
  display:inline-block; background:rgba(255,255,255,0.2);
  padding:10px 28px; border-radius:30px; font-size:22px; font-weight:700;
  backdrop-filter:blur(10px);
}
.container { max-width:900px; margin:0 auto; padding:24px; }

/* Share Box */
.share-box {
  background:white; border-radius:16px;
  box-shadow:0 2px 12px rgba(0,0,0,0.08);
  padding:24px; margin-bottom:20px;
  border:2px solid #667EEA;
}
.share-box h2 { font-size:18px; margin-bottom:4px; color:#667EEA; }
.share-box p { font-size:14px; color:#6B7280; margin-bottom:16px; }
.link-row { display:flex; gap:10px; }
.link-row input {
  flex:1; padding:12px 14px; border:2px solid #E5E7EB; border-radius:10px;
  font-size:13px; color:#374151; background:#F9FAFB;
}
.copy-btn {
  padding:12px 20px; background:#667EEA; color:white; border:none;
  border-radius:10px; font-weight:600; cursor:pointer; white-space:nowrap;
  font-size:14px;
}
.copy-btn:hover { background:#5A67D8; }
.copy-success { color:#059669; font-size:13px; margin-top:8px; display:none; }

/* Cards */
.card {
  background:white; border-radius:16px;
  box-shadow:0 2px 12px rgba(0,0,0,0.08);
  padding:24px; margin-bottom:20px;
}
.card h2 { font-size:18px; font-weight:700; margin-bottom:16px; display:flex; align-items:center; gap:8px; }

/* Party Details */
.details-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; }
.detail-item { background:#F9FAFB; border-radius:10px; padding:14px; }
.detail-item .dl { font-size:12px; color:#9CA3AF; margin-bottom:4px; }
.detail-item .dv { font-size:16px; font-weight:600; }

/* Shopping List */
.shop-item { display:flex; align-items:center; padding:14px 0; border-bottom:1px solid #F3F4F6; gap:12px; }
.shop-item:last-child { border-bottom:none; }
.shop-name { flex:1; font-size:15px; }
.amazon-btn {
  display:inline-block; background:#FF9900; color:#111; padding:7px 14px;
  border-radius:8px; text-decoration:none; font-size:13px; font-weight:700;
  white-space:nowrap; transition:background 0.2s;
}
.amazon-btn:hover { background:#E88A00; }

/* Tips */
.tip-row { display:flex; align-items:flex-start; padding:12px 0; border-bottom:1px solid #F3F4F6; gap:12px; }
.tip-row:last-child { border-bottom:none; }
.tip-icon { font-size:22px; flex-shrink:0; }
.tip-text { flex:1; font-size:14px; color:#374151; line-height:1.5; }
.tip-save { background:#D1FAE5; color:#065F46; padding:4px 10px; border-radius:8px; font-size:13px; font-weight:700; white-space:nowrap; }

/* Signup nudge */
.nudge {
  background:linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
  color:white; border-radius:16px; padding:24px; text-align:center; margin-bottom:20px;
}
.nudge h3 { font-size:18px; margin-bottom:6px; }
.nudge p { font-size:14px; opacity:0.9; margin-bottom:16px; }
.nudge-btn {
  background:white; color:#667EEA; padding:10px 28px;
  border-radius:20px; font-weight:700; text-decoration:none; font-size:15px;
}

.footer { text-align:center; padding:32px; color:#9CA3AF; font-size:13px; }
@media (max-width:600px) { .hero h1 { font-size:24px; } .link-row { flex-direction:column; } }
</style>
</head>
<body>

<div class="navbar">
  <div class="nav-logo">🎉 Party Planner</div>
  <a href="/" class="nav-new">+ New Party</a>
</div>

<div class="hero">
  <h1>{{ emoji }} {{ name }}'s {{ age }}th Birthday Party!</h1>
  <div class="sub">{{ theme }} Theme &bull; {{ venue }}</div>
  <div class="countdown">⏰ {{ days_until }} days to go!</div>
</div>

<div class="container">

  <!-- Share Link -->
  <div class="share-box">
    <h2>📬 Your Guest Invite Link</h2>
    <p>Copy and share this link with guests — they'll see a beautiful invitation and can RSVP.</p>
    <div class="link-row">
      <input type="text" id="invite-url" value="{{ invite_url }}" readonly>
      <button class="copy-btn" onclick="copyLink()">Copy Link</button>
    </div>
    <div class="copy-success" id="copy-msg">✓ Copied to clipboard!</div>
  </div>

  <!-- Party Details -->
  <div class="card">
    <h2>📋 Party Details</h2>
    <div class="details-grid">
      <div class="detail-item"><div class="dl">Date</div><div class="dv">{{ date_fmt }}</div></div>
      <div class="detail-item"><div class="dl">Time</div><div class="dv">{{ time_fmt }}</div></div>
      <div class="detail-item"><div class="dl">Venue</div><div class="dv">{{ venue }}</div></div>
      <div class="detail-item"><div class="dl">Theme</div><div class="dv">{{ emoji }} {{ theme }}</div></div>
    </div>
  </div>

  <!-- Shopping List -->
  <div class="card">
    <h2>🛒 Shopping List</h2>
    <p style="font-size:14px;color:#6B7280;margin-bottom:16px;">
      Everything you need for a {{ theme }} party. Buy on Amazon with one click.
    </p>
    {% for item in shopping %}
    <div class="shop-item">
      <div class="shop-name">{{ item.label }}</div>
      <a href="{{ item.url }}" target="_blank" class="amazon-btn">🛒 Amazon</a>
    </div>
    {% endfor %}
    <div style="margin-top:16px;padding:12px;background:#FFF7ED;border-radius:10px;font-size:13px;color:#92400E;">
      💡 <strong>Pro tip:</strong> Check Costco for cake ($25 vs $80+ at bakeries) and Dollar Tree for party favors!
    </div>
  </div>

  <!-- Money Tips -->
  <div class="card">
    <h2>💡 Money-Saving Tips</h2>
    <div class="tip-row">
      <div class="tip-icon">🎂</div>
      <div class="tip-text"><strong>Cake:</strong> Costco sheet cake $24.99 — feeds 48, looks amazing</div>
      <div class="tip-save">Save $55</div>
    </div>
    <div class="tip-row">
      <div class="tip-icon">🍕</div>
      <div class="tip-text"><strong>Food:</strong> Little Caesars $6/pizza vs delivery $15/pizza</div>
      <div class="tip-save">Save $27</div>
    </div>
    <div class="tip-row">
      <div class="tip-icon">📧</div>
      <div class="tip-text"><strong>Invites:</strong> Use this free link vs printed Evite cards ($25+)</div>
      <div class="tip-save">Save $25</div>
    </div>
    <div class="tip-row">
      <div class="tip-icon">🎁</div>
      <div class="tip-text"><strong>Goody bags:</strong> Oriental Trading bulk $1.50/bag vs store $4/bag</div>
      <div class="tip-save">Save $37</div>
    </div>
    <div style="text-align:right;margin-top:12px;font-size:16px;font-weight:700;color:#059669;">
      Total potential savings: $144 🎉
    </div>
  </div>

  <!-- Checklist -->
  <div class="card">
    <h2>✅ Party Checklist</h2>
    {% for phase, tasks in checklist %}
    <div style="margin-bottom:16px;">
      <div style="font-weight:700;color:#667EEA;margin-bottom:8px;font-size:15px;">{{ phase }}</div>
      {% for t in tasks %}
      <div style="padding:8px 0;border-bottom:1px solid #F9FAFB;display:flex;gap:10px;align-items:center;font-size:14px;">
        <span>⬜</span><span>{{ t }}</span>
      </div>
      {% endfor %}
    </div>
    {% endfor %}
  </div>

  <!-- Signup nudge -->
  <div class="nudge">
    <h3>💾 Save Your Party Plan</h3>
    <p>Create a free account to save this party, track RSVPs, and manage shopping from any device.</p>
    <a href="/#signup" class="nudge-btn">Create Free Account</a>
  </div>

</div>

<div class="footer">
  🎉 Birthday Party Planner &bull; Made for busy American parents<br>
  <span style="margin-top:4px;display:block;">Questions? We earn a small commission from Amazon links at no extra cost to you.</span>
</div>

<script>
function copyLink() {
  var el = document.getElementById('invite-url');
  el.select(); el.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(el.value).then(function() {
    document.getElementById('copy-msg').style.display = 'block';
    setTimeout(function(){ document.getElementById('copy-msg').style.display = 'none'; }, 3000);
  });
}
</script>
</body>
</html>"""


# ─── Guest Invitation ──────────────────────────────────────

INVITE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>You're Invited to {{ name }}'s Birthday Party!</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: {{ gradient }};
  min-height:100vh;
  padding: 24px;
}
.wrap { max-width:540px; margin:0 auto; }
.card {
  background:white; border-radius:20px;
  box-shadow:0 20px 60px rgba(0,0,0,0.25);
  overflow:hidden; margin-bottom:20px;
}
.invite-header {
  background: {{ gradient }};
  color:white; padding:48px 32px; text-align:center;
}
.invite-header .big-emoji { font-size:64px; margin-bottom:12px; }
.invite-header h1 { font-size:28px; font-weight:900; margin-bottom:8px; }
.invite-header .subtitle { font-size:17px; opacity:0.9; }
.invite-body { padding:32px; }
.detail-row { display:flex; align-items:flex-start; gap:14px; padding:14px 0; border-bottom:1px solid #F3F4F6; }
.detail-row:last-child { border-bottom:none; }
.detail-icon { font-size:22px; flex-shrink:0; width:32px; text-align:center; }
.detail-text .dl { font-size:12px; color:#9CA3AF; margin-bottom:2px; }
.detail-text .dv { font-size:16px; font-weight:600; color:#1F2937; }
.rsvp-section { padding:32px; background:#F9FAFB; text-align:center; }
.rsvp-section h3 { font-size:20px; font-weight:700; margin-bottom:8px; }
.rsvp-section p { color:#6B7280; font-size:14px; margin-bottom:20px; }
.rsvp-buttons { display:flex; gap:12px; justify-content:center; }
.rsvp-yes {
  flex:1; max-width:180px; padding:14px 20px;
  background:linear-gradient(135deg, #10B981 0%, #059669 100%);
  color:white; border-radius:12px; text-decoration:none;
  font-weight:700; font-size:16px; text-align:center;
  transition:transform 0.2s;
}
.rsvp-no {
  flex:1; max-width:180px; padding:14px 20px;
  background:#F3F4F6; color:#374151; border-radius:12px;
  text-decoration:none; font-weight:700; font-size:16px; text-align:center;
  transition:transform 0.2s;
}
.rsvp-yes:hover, .rsvp-no:hover { transform:scale(1.04); }
.gift-card { background:white; border-radius:20px; box-shadow:0 2px 12px rgba(0,0,0,0.1); padding:24px; margin-bottom:20px; }
.gift-card h3 { font-size:18px; font-weight:700; margin-bottom:16px; }
.gift-item { display:flex; align-items:center; padding:12px 0; border-bottom:1px solid #F9FAFB; gap:12px; }
.gift-item:last-child { border-bottom:none; }
.gift-name { flex:1; font-size:14px; }
.amazon-btn {
  background:#FF9900; color:#111; padding:7px 14px;
  border-radius:8px; text-decoration:none; font-size:12px; font-weight:700;
  white-space:nowrap;
}
.footer { text-align:center; color:rgba(255,255,255,0.7); font-size:13px; padding:16px; }
.footer a { color:white; }
@media (max-width:480px) { .invite-header { padding:32px 20px; } .invite-body { padding:20px; } .rsvp-section { padding:24px 20px; } }
</style>
</head>
<body>
<div class="wrap">

  <!-- Invitation Card -->
  <div class="card">
    <div class="invite-header">
      <div class="big-emoji">{{ emoji }}</div>
      <h1>You're Invited!</h1>
      <div class="subtitle">Join us for <strong>{{ name }}'s {{ age }}{{ suffix }} Birthday!</strong></div>
    </div>
    <div class="invite-body">
      <div class="detail-row">
        <div class="detail-icon">🎨</div>
        <div class="detail-text"><div class="dl">Theme</div><div class="dv">{{ emoji }} {{ theme }}</div></div>
      </div>
      <div class="detail-row">
        <div class="detail-icon">📅</div>
        <div class="detail-text"><div class="dl">Date</div><div class="dv">{{ date_fmt }}</div></div>
      </div>
      <div class="detail-row">
        <div class="detail-icon">🕐</div>
        <div class="detail-text"><div class="dl">Time</div><div class="dv">{{ time_fmt }}</div></div>
      </div>
      <div class="detail-row">
        <div class="detail-icon">📍</div>
        <div class="detail-text"><div class="dl">Location</div><div class="dv">{{ venue }}</div></div>
      </div>
    </div>
    <div class="rsvp-section">
      <h3>Will you be there? 🎉</h3>
      <p>Please let us know so we can plan for you!</p>
      <div class="rsvp-buttons">
        <a href="{{ rsvp_yes }}" class="rsvp-yes">✓ Yes, I'm coming!</a>
        <a href="{{ rsvp_no }}" class="rsvp-no">✗ Can't make it</a>
      </div>
    </div>
  </div>

  <!-- Gift Ideas -->
  <div class="gift-card">
    <h3>🎁 Gift Ideas for {{ name }}</h3>
    {% for gift in gifts %}
    <div class="gift-item">
      <div class="gift-name">{{ gift.label }}</div>
      <a href="{{ gift.url }}" target="_blank" class="amazon-btn">🛒 Amazon</a>
    </div>
    {% endfor %}
  </div>

</div>

<div class="footer">
  🎉 <a href="/">Create your own free party plan</a> &bull; Birthday Party Planner
</div>
</body>
</html>"""


# ─── Routes ───────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(LANDING_HTML, themes=THEMES)


@app.route("/create", methods=["POST"])
def create():
    data = {
        "name": request.form.get("name", "").strip(),
        "age": int(request.form.get("age", 6)),
        "date": request.form.get("date", ""),
        "time": request.form.get("time", "14:00"),
        "venue": request.form.get("venue", "").strip(),
        "theme": request.form.get("theme", "Spider-Man"),
        "email": request.form.get("email", "").strip(),
    }
    b64 = encode_party(data)
    return redirect(f"/party/{b64}")


@app.route("/party/<b64>")
def party(b64):
    try:
        data = decode_party(b64)
    except Exception:
        return redirect("/")

    theme_key = data.get("theme", "Spider-Man")
    theme = THEMES.get(theme_key, THEMES["Spider-Man"])

    # Shopping list with affiliate links
    shopping = [
        {"label": item.replace(theme_key + " ", "").replace(theme_key.lower() + " ", "").title() if item.startswith(theme_key.lower()) else item.title(),
         "url": amazon_url(item)}
        for item in theme["items"]
    ]

    # Checklist
    checklist = [
        ("4 Weeks Before", [
            "Choose and book venue",
            "Finalize guest list",
            "Send out invitations (share the invite link!)",
        ]),
        ("3 Weeks Before", [
            "Order cake (try Costco — $25, feeds 48!)",
            "Order supplies on Amazon",
            "Plan activities and games",
        ]),
        ("1 Week Before", [
            "Confirm RSVPs and headcount",
            "Buy goody bag fillers (Dollar Tree!)",
            "Buy pinata and candy",
            "Order pizza (Little Caesars — best value!)",
        ]),
        ("Day Before", [
            "Pick up cake",
            "Set up decorations",
            "Assemble goody bags",
            "Charge phone/camera for pictures",
        ]),
        ("Party Day!", [
            "Set up food and drinks",
            "Hang pinata",
            "HAVE FUN! 🎉",
        ]),
    ]

    # Invite URL
    invite_b64 = encode_party(data)
    base_url = request.host_url.rstrip("/")
    invite_url = f"{base_url}/invite/{invite_b64}"

    # Date/time formatting
    date_fmt = data["date"]
    try:
        dt = datetime.strptime(data["date"], "%Y-%m-%d")
        date_fmt = dt.strftime("%A, %B %d, %Y")
        days_until = (dt - datetime.now()).days
    except Exception:
        days_until = "?"

    time_fmt = data["time"]
    try:
        t = datetime.strptime(data["time"], "%H:%M")
        time_fmt = t.strftime("%-I:%M %p")
    except Exception:
        pass

    return render_template_string(
        DASHBOARD_HTML,
        name=data["name"],
        age=data["age"],
        theme=theme_key,
        emoji=theme["emoji"],
        gradient=theme["gradient"],
        venue=data["venue"],
        date_fmt=date_fmt,
        time_fmt=time_fmt,
        days_until=days_until,
        invite_url=invite_url,
        shopping=shopping,
        checklist=checklist,
    )


@app.route("/invite/<b64>")
def invite(b64):
    try:
        data = decode_party(b64)
    except Exception:
        return redirect("/")

    theme_key = data.get("theme", "Spider-Man")
    theme = THEMES.get(theme_key, THEMES["Spider-Man"])

    # Age suffix
    age = data["age"]
    suffix = "th"
    if age % 100 not in (11, 12, 13):
        if age % 10 == 1: suffix = "st"
        elif age % 10 == 2: suffix = "nd"
        elif age % 10 == 3: suffix = "rd"

    # Date/time
    date_fmt = data["date"]
    try:
        dt = datetime.strptime(data["date"], "%Y-%m-%d")
        date_fmt = dt.strftime("%A, %B %d, %Y")
    except Exception:
        pass

    time_fmt = data["time"]
    try:
        t = datetime.strptime(data["time"], "%H:%M")
        time_fmt = t.strftime("%-I:%M %p")
    except Exception:
        pass

    # RSVP mailto links
    email = data.get("email", "")
    subject = f"RSVP - {data['name']}'s Birthday Party"
    rsvp_yes = f"mailto:{email}?subject={subject}&body=Yes, we will be there!" if email else "#"
    rsvp_no = f"mailto:{email}?subject={subject}&body=Sorry, we can't make it." if email else "#"

    # Gift ideas
    gift_queries = [
        f"{theme_key} action figure toy",
        f"{theme_key} board game kids",
        f"LEGO set age {age}",
        f"kids art craft kit",
        f"kids book set age {age}",
    ]
    gifts = [{"label": q.title(), "url": amazon_url(q)} for q in gift_queries]

    return render_template_string(
        INVITE_HTML,
        name=data["name"],
        age=age,
        suffix=suffix,
        theme=theme_key,
        emoji=theme["emoji"],
        gradient=theme["gradient"],
        venue=data["venue"],
        date_fmt=date_fmt,
        time_fmt=time_fmt,
        rsvp_yes=rsvp_yes,
        rsvp_no=rsvp_no,
        gifts=gifts,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
