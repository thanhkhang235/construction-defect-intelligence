from __future__ import annotations


CATEGORY_KEYWORDS = {
    "Structural": [
        "structural",
        "foundation",
        "brickwork",
        "masonry",
        "concrete",
        "wall tie",
        "roof structure",
        "roof sheathing",
        "ceiling joist",
        "basement/crawl space walls",
    ],
    "Roofing": [
        "roof",
        "gutter",
        "downpipe",
        "flashing",
        "chimney",
        "eaves",
        "soffit",
        "fascia",
        "scupper",
    ],
    "Water & Moisture": [
        "water",
        "moisture",
        "damp",
        "leak",
        "condensation",
        "drainage",
        "wet area",
        "basement",
        "vapor",
    ],
    "Electrical": [
        "electrical",
        "electric",
        "wiring",
        "lighting",
        "down light",
        "panel",
        "switch",
        "socket",
    ],
    "Plumbing": [
        "plumbing",
        "water supply",
        "pipe",
        "waste",
        "sewer",
        "toilet",
        "bathroom",
        "hot water",
    ],
    "Fire & Safety": [
        "fire",
        "safety",
        "smoke",
        "asbestos",
        "hazard",
        "compliance",
        "clearance",
        "guard",
        "handrail",
    ],
    "Interior Finishes": [
        "interior",
        "ceiling",
        "plaster",
        "floor",
        "flooring",
        "tiling",
        "cabinet",
        "decorative",
        "finishes",
        "walls & ceiling",
    ],
    "Exterior Envelope": [
        "exterior",
        "cladding",
        "siding",
        "window",
        "door",
        "deck",
        "balcony",
        "fence",
        "landscaping",
    ],
    "Heating & Ventilation": [
        "heating",
        "cooling",
        "hvac",
        "ventilation",
        "flue",
        "fireplace",
        "insulation",
        "energy efficiency",
    ],
    "Access & Inspection Limitations": [
        "access",
        "accessibility",
        "inspection",
        "report",
        "condition",
        "general",
    ],
    "Maintenance": [
        "maintenance",
        "deferred cost",
        "repair",
        "wear",
    ],
}

DEFAULT_CATEGORY = "Other"
CANONICAL_CATEGORIES = sorted([*CATEGORY_KEYWORDS.keys(), DEFAULT_CATEGORY])


def normalize_category(category: str | None) -> str:
    normalized = " ".join((category or "").lower().split())
    if not normalized:
        return DEFAULT_CATEGORY

    for canonical_category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return canonical_category

    return DEFAULT_CATEGORY


def get_canonical_categories() -> list[str]:
    return CANONICAL_CATEGORIES
