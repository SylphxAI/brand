"""The three Sylphx visual directions (Phase A, 2026-09-28): tokens, type, marks, icons, motion.

Each direction is a complete identity system. build.py renders it onto real
pages (home, a product page, a docs page, the console home, a console
resource page) at desktop and mobile width, in dark and light.
"""

from __future__ import annotations

import math

# ── Marks (512 grid; "{c}" is the mark colour, "{c2}" the second tone) ──────


def mark_slipstream() -> str:
    """A solid block split by an S-shaped gap of air."""
    size, r, cx = 360, 96, 256
    x0 = cx - size / 2
    lift = size * 0.2
    h = size / 2 + 20
    wave = f"M{cx - h} {cx + lift}C{cx - 30} {cx + lift} {cx + 30} {cx - lift} {cx + h} {cx - lift}"
    return (
        '<defs><mask id="slip" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="512">'
        '<rect width="512" height="512" fill="#fff"/>'
        f'<path d="{wave}" fill="none" stroke="#000" stroke-width="46"/></mask></defs>'
        f'<rect x="{x0}" y="{x0}" width="{size}" height="{size}" rx="{r}" fill="{{c}}" mask="url(#slip)"/>'
    )


def _crescent(cx: float, cy: float, r_out: float, dx: float, dy: float, r_in: float) -> str:
    """Outer circle minus an offset inner circle (even-odd), as one path."""

    def circ(x: float, y: float, r: float) -> str:
        return f"M{x - r:.2f} {y:.2f}a{r:.2f} {r:.2f} 0 1 0 {2 * r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2 * r:.2f} 0Z"

    return circ(cx, cy, r_out) + circ(cx + dx, cy + dy, r_in)


def mark_gust() -> str:
    """Three tapered strokes fanned like a wing: the sylph, a spirit of the air."""
    parts = []
    # Each blade is a thin crescent: an arc swept from lower left to upper right.
    for i, (scale, tone) in enumerate(((1.0, "{c}"), (0.78, "{c2}"), (0.56, "{c}"))):
        r = 210 * scale
        cx, cy = 150 + (1 - scale) * 40, 380 - (1 - scale) * 20
        d = _crescent(cx, cy, r, 34 * scale, 40 * scale, r * 0.93)
        parts.append(
            f'<clipPath id="q{i}"><rect x="{cx}" y="{cy - r - 4}" width="{r + 8}" height="{r + 4}"/></clipPath>'
            f'<path fill="{tone}" fill-rule="evenodd" clip-path="url(#q{i})" d="{d}"/>'
        )
    return '<g transform="translate(22 -30)">' + "".join(parts) + "</g>"


def mark_knot() -> str:
    """Two currents that cross and weave into an x: the x of Sylphx."""
    h, w, cx = 150, 70, 256
    a = f"M{cx - h} {cx - h}C{cx + 40} {cx - h} {cx - 40} {cx + h} {cx + h} {cx + h}"
    b = f"M{cx + h} {cx - h}C{cx - 40} {cx - h} {cx + 40} {cx + h} {cx - h} {cx + h}"
    gap = 28
    return (
        '<defs><mask id="weave" maskUnits="userSpaceOnUse" x="0" y="0" width="512" height="512">'
        '<rect width="512" height="512" fill="#fff"/>'
        f'<path d="{b}" fill="none" stroke="#000" stroke-width="{w + 2 * gap}" stroke-linecap="butt"/></mask></defs>'
        f'<path d="{a}" fill="none" stroke="{{c}}" stroke-width="{w}" stroke-linecap="butt" mask="url(#weave)"/>'
        f'<path d="{b}" fill="none" stroke="{{c2}}" stroke-width="{w}" stroke-linecap="butt"/>'
    )


# ── Icons (24 grid, drawn as strokes; the style decides width, caps, duotone) ─

ICONS = {
    "overview": "M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z",
    "deploy": "M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12v9M12 12L4 7.5",
    "database": "M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3zM4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
    "key": "M14.5 9.5a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0zM13.2 12.7L20 19.5M17 16.5l2-2M15 14.5l1.5-1.5",
    "logs": "M5 5h14M5 9.7h10M5 14.3h14M5 19h8",
    "workflow": "M5 4h5v5H5zM14 15h5v5h-5zM7.5 9v3.5a2 2 0 0 0 2 2H14",
    "users": "M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 4.5a3.5 3.5 0 0 1 0 6.5M18 14.3c1.8.9 3 2.7 3 5.7",
    "settings": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM12 2.5v3M12 18.5v3M21.5 12h-3M5.5 12h-3M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1M18.7 18.7l-2.1-2.1M7.4 7.4L5.3 5.3",
    "search": "M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM20 20l-4-4",
    "bolt": "M13 3L5 13.5h6L10 21l8-10.5h-6z",
}


# ── Directions ──────────────────────────────────────────────────────────────

DIRECTIONS = {
    "a-signal": {
        "name": "Signal",
        "tagline": "Instrument precision: graphite, one amber signal, nothing extra.",
        "mark": mark_slipstream,
        "mark_colours": ("accent", "accent"),
        "font_sans": "Geist Sans",
        "font_display": "Geist Sans",
        "font_mono": "Geist Mono",
        "display_weight": 600,
        "display_tracking": "-0.04em",
        "display_style": "normal",
        "radius": "6px",
        "radius_lg": "10px",
        "density": "compact",
        "icon": {"width": 1.5, "cap": "square", "join": "miter", "duotone": False},
        "console": "sidebar",
        "hero": "split",
        "motion": [
            "120–180 ms, ease-out (0.2, 0, 0, 1); nothing bounces.",
            "Only opacity and 4 px translation; layout never animates.",
            "Live data changes flash the amber signal for 600 ms, then settle.",
        ],
        "takes": "Vercel and Linear: restraint, density, hairlines, keyboard-first speed.",
        "rejects": "Their colourless anonymity: one warm signal colour makes it ours; no gradients or glass.",
        "dark": {
            "bg": "#0C0B0A", "surface": "#141312", "surface2": "#1B1A18", "raised": "#211F1D",
            "border": "#2A2826", "border2": "#3A3734", "text": "#F5F3F0", "text2": "#A8A29E",
            "text3": "#77716C", "accent": "#F59E0B", "accent_text": "#FBBF24", "on_accent": "#1C1917",
            "accent_soft": "rgba(245,158,11,0.12)", "ok": "#4ADE80", "warn": "#FBBF24", "err": "#F87171",
            "info": "#60A5FA", "field": "#1C1917", "code_bg": "#0F0E0D",
        },
        "light": {
            "bg": "#FAFAF9", "surface": "#FFFFFF", "surface2": "#F4F3F1", "raised": "#FFFFFF",
            "border": "#E7E5E2", "border2": "#D6D3CF", "text": "#1C1917", "text2": "#57534E",
            "text3": "#87817B", "accent": "#D97706", "accent_text": "#B45309", "on_accent": "#FFFFFF",
            "accent_soft": "rgba(217,119,6,0.10)", "ok": "#16A34A", "warn": "#B45309", "err": "#DC2626",
            "info": "#2563EB", "field": "#1C1917", "code_bg": "#1C1917",
        },
    },
    "b-atmosphere": {
        "name": "Atmosphere",
        "tagline": "The air a sylph lives in: deep sky, light, and colour that moves.",
        "mark": mark_gust,
        "mark_colours": ("accent", "accent2"),
        "font_sans": "Instrument Sans",
        "font_display": "Instrument Serif",
        "font_mono": "JetBrains Mono",
        "display_weight": 400,
        "display_tracking": "-0.02em",
        "display_style": "normal",
        "radius": "12px",
        "radius_lg": "20px",
        "density": "airy",
        "icon": {"width": 1.75, "cap": "round", "join": "round", "duotone": True},
        "console": "floating",
        "hero": "centered",
        "motion": [
            "240–320 ms, soft ease-out (0.16, 1, 0.3, 1); panels drift in 8 px.",
            "Background light slowly shifts with scroll (reduced-motion: static).",
            "Progress and live states breathe: a 2.4 s glow, never a spinner.",
        ],
        "takes": "Stripe and Clerk: colour and light as the brand, warm editorial type on the marketing side.",
        "rejects": "Decoration inside the product: the console stays calm and flat; gradients live on the site only.",
        "dark": {
            "bg": "#070A18", "surface": "#0D1228", "surface2": "#131A36", "raised": "#18204A",
            "border": "#222B55", "border2": "#303A6B", "text": "#EEF1FF", "text2": "#A7AFD6",
            "text3": "#737CA6", "accent": "#7C8CFF", "accent2": "#38D2F5", "accent_text": "#A5B1FF",
            "on_accent": "#070A18", "accent_soft": "rgba(124,140,255,0.14)", "ok": "#34D399",
            "warn": "#FBBF24", "err": "#FB7185", "info": "#38D2F5", "field": "#0D1228", "code_bg": "#0A0E22",
        },
        "light": {
            "bg": "#F6F7FF", "surface": "#FFFFFF", "surface2": "#EEF1FE", "raised": "#FFFFFF",
            "border": "#DDE2F6", "border2": "#C8CFEE", "text": "#0B1030", "text2": "#4B5382",
            "text3": "#7C84AB", "accent": "#4F5DFF", "accent2": "#0EA5E9", "accent_text": "#3F4BE0",
            "on_accent": "#FFFFFF", "accent_soft": "rgba(79,93,255,0.09)", "ok": "#059669",
            "warn": "#B45309", "err": "#E11D48", "info": "#0284C7", "field": "#0D1228", "code_bg": "#0D1228",
        },
    },
    "c-engineered": {
        "name": "Engineered",
        "tagline": "A precise technical document: paper, ink, grid, cobalt.",
        "mark": mark_knot,
        "mark_colours": ("accent", "text"),
        "font_sans": "IBM Plex Sans",
        "font_display": "IBM Plex Sans",
        "font_mono": "IBM Plex Mono",
        "display_weight": 500,
        "display_tracking": "-0.03em",
        "display_style": "normal",
        "radius": "2px",
        "radius_lg": "3px",
        "density": "dense",
        "icon": {"width": 1.75, "cap": "butt", "join": "miter", "duotone": False},
        "console": "rail",
        "hero": "grid",
        "motion": [
            "150 ms, linear-out; state changes step, like instruments.",
            "Numbers roll on change; tables update a row at a time.",
            "No decorative motion at all; focus rings snap, never fade.",
        ],
        "takes": "Railway and Resend: technical honesty, mono labels, visible structure and grid.",
        "rejects": "Dark-only hacker styling: light paper is the default and reads like a specification.",
        "dark": {
            "bg": "#121110", "surface": "#191816", "surface2": "#201F1C", "raised": "#26241F",
            "border": "#302E29", "border2": "#44413A", "text": "#F2EEE6", "text2": "#ABA59A",
            "text3": "#7D776D", "accent": "#6B86FF", "accent_text": "#93A7FF", "on_accent": "#0B0E24",
            "accent_soft": "rgba(107,134,255,0.13)", "ok": "#4ADE80", "warn": "#FACC15", "err": "#F87171",
            "info": "#6B86FF", "field": "#15130F", "code_bg": "#0E0D0B",
        },
        "light": {
            "bg": "#F4F1EA", "surface": "#FFFDF8", "surface2": "#ECE8DE", "raised": "#FFFFFF",
            "border": "#D9D3C5", "border2": "#BFB8A8", "text": "#15130F", "text2": "#55504A",
            "text3": "#827C71", "accent": "#2448F5", "accent_text": "#1E3BD0", "on_accent": "#FFFFFF",
            "accent_soft": "rgba(36,72,245,0.08)", "ok": "#15803D", "warn": "#A16207", "err": "#B91C1C",
            "info": "#2448F5", "field": "#15130F", "code_bg": "#15130F",
        },
    },
}


def mark_svg(direction: dict, theme: dict, size: int = 64, on_field: bool = False) -> str:
    c1, c2 = direction["mark_colours"]
    col1 = theme[c1] if c1 in theme else c1
    col2 = theme.get(c2, col1)
    if on_field:  # on the dark app-icon field the ink tone must become light
        col2 = "#F2EEE6" if c2 == "text" else col2
    body = direction["mark"]().replace("{c}", col1).replace("{c2}", col2)
    return f'<svg viewBox="0 0 512 512" width="{size}" height="{size}" aria-hidden="true">{body}</svg>'


def icon_svg(direction: dict, name: str, size: int = 18, colour: str = "currentColor", tone: str = "") -> str:
    st = direction["icon"]
    d = ICONS[name]
    duo = ""
    if st["duotone"] and tone:
        duo = f'<path d="{d}" fill="{tone}" stroke="none" opacity="0.28"/>'
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{colour}" '
        f'stroke-width="{st["width"]}" stroke-linecap="{st["cap"]}" stroke-linejoin="{st["join"]}" aria-hidden="true">'
        f'{duo}<path d="{d}"/></svg>'
    )


def _unused() -> float:  # keep math imported for mark tweaks
    return math.pi
