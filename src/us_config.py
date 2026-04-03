"""
US Market Configuration
All settings specific to American birthday party planning
"""

# Currency and Locale
CURRENCY = "USD"
CURRENCY_SYMBOL = "$"
LOCALE = "en_US"

# Default Budget Ranges (in USD)
BUDGET_RANGES = {
    "budget": (100, 200),
    "mid_range": (300, 500),
    "premium": (600, 1500),
    "luxury": (2000, 5000)
}

DEFAULT_BUDGET = 400  # Average US party budget

# Average costs per guest
COST_PER_GUEST = {
    "budget": 10,
    "mid_range": 25,
    "premium": 50,
    "luxury": 100
}

# Popular Party Themes by Age
THEMES_BY_AGE = {
    (3, 5): [
        "Disney Princess",
        "Frozen",
        "Paw Patrol",
        "Dinosaurs",
        "Unicorns",
        "Daniel Tiger",
        "Bluey",
        "Cocomelon"
    ],
    (6, 8): [
        "Superhero (Marvel)",
        "Spider-Man",
        "Batman",
        "LEGO",
        "Minecraft",
        "Pokemon",
        "Sports",
        "Rainbow/Butterfly"
    ],
    (9, 12): [
        "Fortnite",
        "Roblox",
        "Gaming",
        "Sports",
        "Science/STEM",
        "Outdoor Adventure",
        "Movie Theme",
        "Music/Dance"
    ]
}

# Venue Types
VENUE_TYPES = {
    "home": {
        "name": "Home Party",
        "avg_cost": 150,
        "percentage": 60,
        "pros": ["Cost-effective", "Personal", "Flexible timing"],
        "cons": ["Cleanup", "Weather-dependent", "Space limits"]
    },
    "chuck_e_cheese": {
        "name": "Chuck E. Cheese",
        "avg_cost_per_child": 20,
        "base_package": 200,
        "popular": True
    },
    "trampoline_park": {
        "name": "Trampoline Park (Sky Zone, Urban Air)",
        "avg_cost_per_child": 25,
        "base_package": 300,
        "popular": True
    },
    "bowling": {
        "name": "Bowling Alley",
        "avg_cost_per_child": 18,
        "base_package": 250
    },
    "public_park": {
        "name": "Public Park",
        "avg_cost": 50,  # Permit fee
        "weather_dependent": True
    }
}

# Food Preferences (American defaults)
FOOD_DEFAULTS = {
    "main": "Pizza",
    "cake": "Birthday cake or cupcakes",
    "drinks": "Juice boxes, soda",
    "snacks": "Chips, fruit, veggies with dip",
    "dessert_extra": "Ice cream"
}

# Dietary Restrictions (Common in US)
COMMON_DIETARY_RESTRICTIONS = [
    "Peanut allergy",
    "Tree nut allergy",
    "Dairy-free",
    "Gluten-free",
    "Vegetarian",
    "Vegan",
    "Egg allergy",
    "Shellfish allergy"
]

# Shopping Categories (US-specific)
SHOPPING_CATEGORIES = {
    "decorations": {
        "items": ["Balloons", "Banner", "Tablecloths", "Centerpieces", "Confetti"],
        "avg_cost": 50,
        "stores": ["Amazon", "Party City", "Target"]
    },
    "tableware": {
        "items": ["Plates", "Cups", "Napkins", "Utensils", "Serving platters"],
        "avg_cost": 30,
        "stores": ["Amazon", "Target", "Walmart"]
    },
    "food": {
        "items": ["Pizza", "Cake", "Juice boxes", "Snacks", "Ice cream"],
        "avg_cost": 100,
        "stores": ["Costco", "Local pizzeria", "Grocery store"]
    },
    "activities": {
        "items": ["Piñata", "Party games", "Craft supplies", "Prizes"],
        "avg_cost": 40,
        "stores": ["Amazon", "Party City", "Target"]
    },
    "goody_bags": {
        "items": ["Bags", "Candy", "Small toys", "Stickers", "Bubbles"],
        "avg_cost_per_bag": 3,
        "stores": ["Dollar Tree", "Amazon", "Oriental Trading"]
    },
    "miscellaneous": {
        "items": ["Candles", "Lighter", "Trash bags", "Paper towels", "Thank you cards"],
        "avg_cost": 25,
        "stores": ["Target", "Walmart", "CVS"]
    }
}

# Popular US Party Supply Stores
PARTY_STORES = {
    "amazon": {
        "name": "Amazon",
        "pros": ["Prime shipping", "Wide selection", "Reviews"],
        "best_for": "Everything",
        "url": "https://amazon.com"
    },
    "party_city": {
        "name": "Party City",
        "pros": ["Specialized selection", "Helium balloons", "Themed packages"],
        "best_for": "Decorations, themed items",
        "url": "https://partycity.com"
    },
    "target": {
        "name": "Target",
        "pros": ["Stylish designs", "Good quality", "Convenient"],
        "best_for": "Tableware, decorations",
        "url": "https://target.com"
    },
    "walmart": {
        "name": "Walmart",
        "pros": ["Low prices", "One-stop shop"],
        "best_for": "Budget shopping",
        "url": "https://walmart.com"
    },
    "dollar_tree": {
        "name": "Dollar Tree",
        "pros": ["$1.25 items", "Great for goody bags"],
        "best_for": "Goody bag fillers, basic decorations",
        "url": "https://dollartree.com"
    },
    "costco": {
        "name": "Costco",
        "pros": ["Bulk pricing", "Amazing cakes $20-30"],
        "best_for": "Cake, bulk snacks",
        "url": "https://costco.com"
    },
    "oriental_trading": {
        "name": "Oriental Trading",
        "pros": ["Bulk party favors", "Low prices"],
        "best_for": "Goody bag items in bulk",
        "url": "https://orientaltrading.com"
    }
}

# Invitation Platforms (US)
INVITATION_PLATFORMS = {
    "evite": {
        "name": "Evite",
        "free": True,
        "popular": True,
        "features": ["RSVP tracking", "Guest messaging", "Templates"],
        "url": "https://evite.com"
    },
    "paperless_post": {
        "name": "Paperless Post",
        "free": "Limited",
        "popular": True,
        "features": ["Elegant designs", "RSVP tracking", "Premium options"],
        "url": "https://paperlesspost.com"
    },
    "email": {
        "name": "Email",
        "free": True,
        "features": ["Direct communication", "Personal"]
    },
    "facebook_events": {
        "name": "Facebook Events",
        "free": True,
        "features": ["Social integration", "RSVP tracking"]
    }
}

# American Party Timeline (days before party)
PARTY_TIMELINE = {
    30: "Choose date, book venue, create guest list",
    21: "Send invitations",
    14: "Order cake, plan activities, buy decorations",
    7: "Follow up on RSVPs, finalize headcount, shop for supplies",
    3: "Buy food, prepare goody bags, confirm final details",
    1: "Setup, last-minute shopping",
    0: "PARTY DAY!"
}

# Goody Bag Recommendations by Age
GOODY_BAG_ITEMS = {
    (3, 5): [
        "Bubbles",
        "Stickers",
        "Small toy car/doll",
        "Crayons",
        "Play-Doh",
        "Candy (age-appropriate)",
        "Temporary tattoos"
    ],
    (6, 8): [
        "Slime/putty",
        "Trading cards",
        "Small puzzle",
        "Bouncy ball",
        "Candy",
        "Pencils/erasers",
        "Mini notebook"
    ],
    (9, 12): [
        "Candy",
        "Phone accessories (pop socket)",
        "Lip gloss",
        "Sports cards",
        "Gift card ($5 iTunes/Amazon)",
        "Fidget toys",
        "Nail polish"
    ]
}

# Budget-Saving Tips (US-specific)
SAVING_TIPS = {
    "cake": "Costco sheet cakes are $20-30 vs. $60-150 custom",
    "decorations": "Dollar Tree has great basic decorations for $1.25 each",
    "goody_bags": "Oriental Trading bulk prices (50 items for $10)",
    "venue": "Public park parties can save $300+",
    "food": "Little Caesars pizza ($6 each) vs. delivery ($15+)",
    "invitations": "Evite is free vs. $20-40 for printed",
    "timing": "Saturday afternoon is cheaper than weekend morning at venues"
}

# Weather-Dependent Party Backup
WEATHER_BACKUP_IDEAS = [
    "Rent a tent/canopy ($50-150)",
    "Move party indoors (garage, basement)",
    "Book venue as backup (call ahead about weather policy)",
    "Rain date option (include on invitation)",
    "Indoor-friendly activities prepared"
]

# Affiliate Programs (US Market)
AFFILIATE_PROGRAMS = {
    "amazon_associates": {
        "commission_rate": 0.03,  # 3% average
        "name": "Amazon Associates",
        "signup_url": "https://affiliate-program.amazon.com"
    },
    "target_affiliate": {
        "commission_rate": 0.08,  # 8%
        "name": "Target Affiliate (Impact/Rakuten)",
        "signup_url": "https://impact.com"
    },
    "walmart_affiliate": {
        "commission_rate": 0.04,  # 4%
        "name": "Walmart Affiliate (Impact)",
        "signup_url": "https://impact.com"
    },
    "party_city_affiliate": {
        "commission_rate": 0.05,  # 5% estimate
        "name": "Party City Affiliate",
        "signup_url": "https://partycity.com/affiliate"
    }
}

# American Units
UNITS = {
    "distance": "feet",
    "weight": "pounds",
    "liquid": "gallons",
    "temperature": "fahrenheit"
}
