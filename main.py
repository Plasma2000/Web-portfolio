import flet as ft
import flet_video as fv
import base64
import os
import time
import threading
import math
from pathlib import Path


def img_b64(path: str) -> str:
    ext = Path(path).suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


HERO_B64  = img_b64("Background_1.jpeg")
LEAF_B64  = img_b64("Background_2.jpeg")
ABOUT_B64 = img_b64("About_me.jpeg")

LOGO_B64       = img_b64("Mineshield_logo.jpg")
TEAM1_B64      = img_b64("Mineshield_2.jpeg")
TEAM2_B64      = img_b64("Mineshield_3.jpeg")
EVIDENCE1_B64  = img_b64("Evidence_1.png")
EVIDENCE2_B64  = img_b64("Evidence_2.png")
EVIDENCE3_B64  = img_b64("Evidence_3.png")

CREAM      = "#f5f0e8"
DARK       = "#2c2416"
GOLD       = "#b8975a"
GOLD_LT    = "#d4b47a"
MUTED      = "#8a7a65"
WHITE      = "#ffffff"
LEAF_GREEN = "#4a6741"


def txt(value, size=14, color=DARK, weight=ft.FontWeight.W_300,
        italic=False, align=ft.TextAlign.LEFT):
    return ft.Text(
        value, size=size, color=color,
        weight=weight, italic=italic,
        text_align=align, font_family="Georgia",
    )


def small_label(value):
    return ft.Text(value, size=11, color=GOLD, weight=ft.FontWeight.W_400,
                   font_family="Arial")


def gold_line():
    return ft.Container(width=60, height=1, bgcolor=GOLD_LT)


# NAV
def nav_bar(section_views: list, page: ft.Page, on_navigate=None):
    section_names = ["Home", "About", "MATLAB Hub", "MineShield", "Project Timeline", "Technical Blog"]

    def go(e, idx):
        if on_navigate:
            on_navigate(e, idx)
            return
        for i, s in enumerate(section_views):
            s.visible = (i == idx)
        page.update()

    tabs = [
        ft.TextButton(
            s,
            on_click=lambda e, i=i: go(e, i),
            style=ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: WHITE, ft.ControlState.HOVERED: GOLD_LT},
                overlay_color="#22b8975a",
                padding=ft.Padding(left=6, right=6, top=4, bottom=4),
                shape=ft.RoundedRectangleBorder(radius=4),
            ),
        )
        for i, s in enumerate(section_names)
    ]

    w = page.width or 800
    if w < 700:
        inner = ft.Column([
            ft.Text("TEOPOLINA NEGONGA", size=11, color=GOLD_LT,
                    weight=ft.FontWeight.W_300, font_family="Georgia",
                    text_align=ft.TextAlign.CENTER),
            ft.Row(tabs, spacing=0, scroll=ft.ScrollMode.AUTO, wrap=False),
        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        v_pad = 8
    else:
        inner = ft.Row([
            ft.Text("TEOPOLINA NEGONGA", size=14, color=GOLD_LT,
                    weight=ft.FontWeight.W_300, font_family="Georgia"),
            ft.Row(tabs, spacing=0),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        v_pad = 14

    return ft.Container(
        content=inner,
        bgcolor="#CC2c2416",
        padding=ft.Padding(left=16, right=16, top=v_pad, bottom=v_pad),
        blur=ft.Blur(sigma_x=10, sigma_y=10),
    )


# BACKGROUND  
def leaf_section(content, height=700, page=None):
    w = (page.width or 800) if page else 800
    h_pad = 16 if w < 500 else (40 if w < 700 else 80)
    v_pad = 36 if w < 700 else 70
    return ft.Container(
        content=ft.Container(
            content=content,
            padding=ft.Padding(left=h_pad, right=h_pad, top=v_pad, bottom=v_pad),
        ),
        bgcolor=CREAM,
        image=ft.DecorationImage(src=LEAF_B64, fit=ft.BoxFit.COVER, opacity=0.18),
        expand=True,
    )


# HOME
def home_section(page_ref=None):
    w = (page_ref.width or 800) if page_ref else 800
    mobile = w < 700
    small  = w < 420
    hero_h = 400 if small else (480 if mobile else 775)
    hero_img = ft.Image(src=HERO_B64, fit=ft.BoxFit.COVER, width=9999, height=hero_h)
    overlay = ft.Container(expand=True, bgcolor="#BB1a1008")

    roles = [
        "E L E C T R I C A L   E N G I N E E R I N G   S T U D E N T",
        "Q A   &   T E S T I N G   L E A D",
        "M A T L A B   E N T H U S I A S T",
        "I N N O V A T O R   &   P R O B L E M   S O L V E R",
    ]
    role_text = ft.Text(
        roles[0],
        size=11 if small else 13,
        color=CREAM,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_700,
        italic=True,
        font_family="Arial",
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        opacity=1,
    )

    def stat_chip(number, label):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(number, size=26, color=GOLD_LT,
                            weight=ft.FontWeight.W_900, font_family="Arial",
                            text_align=ft.TextAlign.CENTER),
                    ft.Text(label, size=9, color="#CCf5f0e8",
                            text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_300),
                ],
                spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(left=24, right=24, top=12, bottom=12),
        )

    stats_row = ft.Row(
        [],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    name_block = ft.Column(
        [
            ft.Text(
                "T E O P O L I N A",
                size=30 if small else (48 if mobile else 100),
                color=WHITE,
                weight=ft.FontWeight.W_900,
                text_align=ft.TextAlign.CENTER,
                font_family="Arial",
            ),
            ft.Text(
                "N E G O N G A",
                size=26 if small else (40 if mobile else 90),
                color=WHITE,
                weight=ft.FontWeight.W_900,
                text_align=ft.TextAlign.CENTER,
                font_family="Arial",
                offset=ft.Offset(0, -0.2),
            ),
            ft.Container(height=12),
            role_text,
            ft.Container(height=6),
            ft.Text(
                "University of Namibia",
                size=12,
                color=GOLD,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_400,
                italic=True,
                font_family="Georgia",
                offset=ft.Offset(0, -0.8 if mobile else -2.3),
            ),
            ft.Container(height=20),
            ft.Column(
                [
                    ft.Text("↓", size=18, color=GOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("explore", size=9, color="#88f5f0e8",
                            text_align=ft.TextAlign.CENTER, italic=True),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.END,
        spacing=0,
    )

    hero_container = ft.Container(
        key="sec0",
        content=ft.Stack([
            hero_img,
            overlay,
            ft.Container(content=name_block, alignment=ft.Alignment(x=0, y=0),
                         expand=True, height=hero_h - 75),
        ]),
        height=hero_h,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    def _cycle(page):
        idx = 0
        while True:
            time.sleep(2.8)
            try:
                role_text.opacity = 0
                role_text.update()
                time.sleep(0.45)
                idx = (idx + 1) % len(roles)
                role_text.value = roles[idx]
                role_text.opacity = 1
                role_text.update()
            except Exception:
                break

    hero_container._cycle = _cycle
    return hero_container


# ABOUT
def about_section(page=None):
    w = (page.width or 800) if page else 800
    mobile = w < 700
    photo = ft.Container(
        content=ft.Image(src=ABOUT_B64, fit=ft.BoxFit.COVER),
        width=None if mobile else 420,
        height=220 if mobile else 800,
        expand=False,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    heading = ft.Column(
        [
            ft.Container(height=30 if mobile else 90),
            ft.Text(
                "Who I Am",
                size=11, color=DARK, weight=ft.FontWeight.W_700,
                font_family="Arial", text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=8),
            ft.Text(
                "ABOUT ME",
                size=34 if mobile else 52, color=GOLD, weight=ft.FontWeight.W_700,
                font_family="Georgia", text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=20),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    paragraphs = ft.Column(
        [
            ft.Text(
                "My name is Teopolina Negonga, an aspiring Electrical Engineering student "
                "with a passion for innovation, problem-solving, and technology. I was born "
                "and raised in Oshakati, where I developed a strong curiosity for how things "
                "work and a determination to use technology to create meaningful solutions.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
            ft.Container(height=12),
            ft.Text(
                "I completed my primary education at Erundu Combined School and later attended "
                "Oshigambo High School for my secondary education. Throughout my academic journey, "
                "I have consistently demonstrated a strong interest in mathematics, science, and "
                "analytical problem-solving, which inspired me to pursue a career in engineering.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
            ft.Container(height=12),
            ft.Text(
                "I am currently studying for a Bachelor of Electrical Engineering (Honours) at "
                "the University of Namibia. As an engineering student, I enjoy tackling complex "
                "challenges, learning new technologies, and applying theoretical knowledge to "
                "practical situations. My studies have strengthened my technical, analytical, and "
                "critical-thinking skills while preparing me to contribute to the advancement of "
                "modern engineering solutions.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
            ft.Container(height=12),
            ft.Text(
                "Beyond academics, I have gained valuable experience working collaboratively in "
                "teams, participating in projects, coordinating events, and taking on leadership "
                "responsibilities. These experiences have enhanced my communication, teamwork, "
                "organisational, and project management skills. In my free time, I enjoy creating "
                "media content, photography, videography, travelling, and exploring new places. "
                "These hobbies allow me to express my creativity, capture meaningful moments, and "
                "develop my storytelling and visual communication skills.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
            ft.Container(height=12),
            ft.Text(
                "One of the projects I have worked on in 2026 is MineShield, a mobile application "
                "developed alongside my group members to promote and improve the safety of "
                "individuals working in mining environments. The application focuses on enhancing "
                "awareness, communication, and safety measures within mines. More information about "
                "this project and my contributions to the project can be found throughout this web "
                "portfolio.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
            ft.Container(height=12),
            ft.Text(
                "My goal is to become a skilled electrical engineer who contributes innovative "
                "solutions to real-world challenges while creating technologies that improve lives, "
                "strengthen industries, and support sustainable development.",
                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
            ),
        ],
        spacing=0,
    )

    scrollable_text = (
        paragraphs if mobile else
        ft.Column([paragraphs], scroll=ft.ScrollMode.AUTO, expand=True)
    )

    # Animated skill bars
    skills = [
        ("Electrical Engineering", 0.82),
        ("MATLAB & Simulink", 0.78),
        ("Python & C", 0.72),
        ("Quality Assurance", 0.88),
        ("Team Leadership", 0.85),
    ]

    skill_bars = []
    bar_fills = []
    for skill_name, level in skills:
        bar_w = 180 if mobile else 240
        fill = ft.Container(
            width=0, height=8, bgcolor=GOLD, border_radius=4,
            animate_size=ft.Animation(900, ft.AnimationCurve.EASE_OUT),
        )
        bar_fills.append((fill, level))
        pct_text = ft.Text(f"{int(level*100)}%", size=10, color=MUTED, weight=ft.FontWeight.W_400)
        bar_row = ft.Column([
            ft.Row([
                ft.Text(skill_name, size=11, color=DARK, weight=ft.FontWeight.W_400),
                ft.Container(expand=True),
                pct_text,
            ], spacing=0, width=bar_w),
            ft.Container(
                content=ft.Stack([
                    ft.Container(width=bar_w, height=8, bgcolor="#22b8975a", border_radius=4),
                    fill,
                ]),
                width=bar_w,
            ),
        ], spacing=4)
        skill_bars.append(bar_row)

    skills_widget = ft.Column(
        [
            ft.Container(height=16),
            ft.Text("SKILLS", size=10, color=GOLD, weight=ft.FontWeight.W_700,
                    font_family="Arial"),
            ft.Container(height=10),
            *skill_bars,
        ],
        spacing=8,
    )

    bp = 20 if mobile else 48
    bio_container = ft.Container(
        content=ft.Column([heading, scrollable_text, skills_widget], spacing=0, expand=not mobile),
        padding=ft.Padding(left=bp, right=bp, top=0, bottom=40),
        expand=not mobile,
        bgcolor=CREAM,
    )

    if mobile:
        layout = ft.Column([photo, bio_container], spacing=0)
    else:
        layout = ft.Row([photo, bio_container],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                        spacing=0, expand=True)

    about_container = ft.Container(
        key="sec1",
        content=layout,
        height=None if mobile else 900,
        clip_behavior=None if mobile else ft.ClipBehavior.HARD_EDGE,
        bgcolor=CREAM,
        image=ft.DecorationImage(src=LEAF_B64, fit=ft.BoxFit.COVER, opacity=0.18),
    )
    about_container._bar_fills = bar_fills
    return about_container


# PROJECT TIMELINE
def timeline_section(page=None):
    w = (page.width or 800) if page else 800
    mobile = w < 700
    weeks = [
        ("1-2", "Test Plan Creation & Environment Setup",
         "Created the project test plan and configured the testing environment "
         "for the Mineshield Guard application."),
        ("3-4", "Test Cases for FR-001 to FR-015",
         "Wrote detailed test cases covering functional requirements FR-001 "
         "through FR-015 for the core application modules."),
        ("5-6", "Unit Testing for Auth + Hazards & Bug Tracking",
         "Performed unit testing on the authentication and hazard detection "
         "modules. Set up and maintained the bug tracking spreadsheet."),
        ("7-8", "Regression Testing on Develop Branch",
         "Ran full regression test suite against the develop branch to verify "
         "that new changes did not break existing functionality."),
        ("9-10", "Cross-Version Testing & Edge Cases",
         "Tested the application across Android versions 13, 15, and 16. "
         "Identified and documented edge cases for further review."),
        ("Final Week", "TEST_CASES.md, BUG_REPORT.md & Final Regression Testing",
         "Compiled and submitted TEST_CASES, BUG_REPORT.md and TEST_COVERAGE.md. Conducted "
         "final regression testing to confirm application stability."),
    ]

    items = []
    expanded_state = {}

    for idx_w, (wk, title, desc) in enumerate(weeks):
        desc_text = ft.Text(
            desc, size=12, color="#99f5f0e8", weight=ft.FontWeight.W_300,
            visible=False,
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            opacity=0,
        )
        chevron = ft.Text("▶", size=11, color=GOLD)
        expanded_state[idx_w] = False

        def make_toggle(i=idx_w, dt=desc_text, ch=chevron):
            def toggle(e):
                expanded_state[i] = not expanded_state[i]
                if expanded_state[i]:
                    dt.visible = True
                    dt.opacity = 1
                    ch.value = "▼"
                else:
                    dt.opacity = 0
                    dt.visible = False
                    ch.value = "▶"
                dt.update()
                ch.update()
            return toggle

        dot = ft.Container(
            width=12, height=12, bgcolor=GOLD, border_radius=6,
            margin=ft.Margin(left=-6, right=16, top=8, bottom=0),
            shadow=ft.BoxShadow(blur_radius=8, color="#66b8975a", offset=ft.Offset(0, 0)),
        )
        week_label = ft.Text(f"Week {wk}", size=12, color=GOLD, weight=ft.FontWeight.W_400)
        block = ft.Column(
            [
                ft.Row([week_label, ft.Container(expand=True), chevron], spacing=0),
                txt(title, size=16, color=CREAM, weight=ft.FontWeight.W_400),
                ft.Container(height=4),
                desc_text,
            ],
            spacing=4, expand=True,
        )
        row_container = ft.Container(
            content=ft.Row([dot, block], vertical_alignment=ft.CrossAxisAlignment.START),
            on_click=make_toggle(),
            padding=ft.Padding(left=0, right=0, top=8, bottom=8),
            border_radius=4,
            ink=True,
        )
        items.append(row_container)
        items.append(ft.Container(height=16))

    body = ft.Column(
        [
            small_label("My Journey"),
            ft.Container(height=6),
            txt("PROJECT TIMELINE", size=28 if mobile else 42, color=CREAM, weight=ft.FontWeight.W_900),
            ft.Container(height=8),
            ft.Text(
                "Click any milestone to expand details",
                size=11, color="#66f5f0e8", italic=True,
                text_align=ft.TextAlign.LEFT,
            ),
            ft.Container(height=32),
            ft.Column(items, spacing=0),
        ],
        spacing=0,
    )

    tl_hp = 20 if mobile else (60 if w < 900 else 140)
    return ft.Container(
        key="sec2",
        content=ft.Container(
            content=body,
            padding=ft.Padding(left=tl_hp, right=tl_hp, top=70, bottom=70),
            bgcolor=DARK,
        ),
    )


# MATLAB
MATLAB_COURSES = [
    ("MATLAB Onramp",                         "MATLAB Onramp",                         "https://drive.google.com/file/d/1d_wUZ0kOFj_u8Qtm7Edx1SGPY-QPGfvR/view?usp=sharing"),
    ("Calculations with Vectors and Matrices", "Calculations with Vectors and Matrices", "https://drive.google.com/file/d/1kl1wNAFhk3Xyy5D2h0qQJk-y2dRsxuAg/view?usp=drive_link"),
    ("Make and Manipulate Matrices",           "Make and Manipulate Matrices",           "https://drive.google.com/file/d/1Kh6OzRDX4lk1M8F-iRIC-Jp2z7yJatYK/view?usp=drive_link"),
    ("Circuit Simulation Onramp",              "Circuit Simulation Onramp",              "https://drive.google.com/file/d/1ssCjZ-jgi59OSrGWqJjpAZ0JENUlboaR/view?usp=drive_link"),
    ("Explore Data with MATLAB Plots",         "Explore Data with MATLAB Plots",         "https://drive.google.com/file/d/1Nw4VGNHmfQIqFeWooZsWcvFQPVzrGRDg/view?usp=drive_link"),
    ("Solve Systems of First-Order ODEs",      "Solve Systems of First-Order ODEs",      "https://drive.google.com/file/d/1CgDB30XWWoadejzCXH8Lx8-1oLWCciO_/view?usp=drive_link"),
    ("Simulink Onramp",                        "Simulink Onramp",                        "https://drive.google.com/file/d/1fj3qTCgaQY8Cra4Ph9KJl5zl0jOpLkqF/view?usp=drive_link"),
]


CARD_W = 210
CARD_H = 320
IMG_H  = 160

def matlab_card(title, img_name, cert_url):
    img_path = f"{img_name}.png"
    try:
        img_src = img_b64(img_path)
    except Exception:
        img_src = ""

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Image(
                        src=img_src,
                        fit=ft.BoxFit.COVER,
                        width=CARD_W,
                        height=IMG_H,
                    ) if img_src else ft.Container(bgcolor=CREAM, width=CARD_W, height=IMG_H),
                    width=CARD_W,
                    height=IMG_H,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    border_radius=ft.BorderRadius(
                        top_left=105, top_right=105, bottom_left=0, bottom_right=0),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(height=16),
                            ft.Container(
                                content=ft.Text(
                                    title, size=13, color=DARK,
                                    weight=ft.FontWeight.W_700, font_family="Arial",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                height=52,
                                alignment=ft.Alignment(x=0, y=0),
                            ),
                            ft.Container(height=8),
                            ft.Container(
                                content=ft.Text("✓  Completed", size=10, color="#71A571", weight=ft.FontWeight.W_900,),
                                padding=ft.Padding(left=10, right=10, top=4, bottom=4),
                                border_radius=10,
                            ),
                            ft.Container(height=10),
                            ft.TextButton(
                                content=ft.Text("VIEW CERTIFICATE →", size=12, weight=ft.FontWeight.W_700 ),
                                url=cert_url,
                                style=ft.ButtonStyle(
                                    color={
                                        ft.ControlState.DEFAULT: GOLD,
                                        ft.ControlState.HOVERED: GOLD_LT,
                                    },
                                    overlay_color=ft.Colors.TRANSPARENT,
                                    padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                                ),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    padding=ft.Padding(left=20, right=20, top=0, bottom=16),
                    height=CARD_H - IMG_H,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=CARD_W,
        height=CARD_H,
        bgcolor=WHITE,
        border_radius=ft.BorderRadius(top_left=108, top_right=108, bottom_left=4, bottom_right=4),
        shadow=ft.BoxShadow(blur_radius=20, color="#1a000000", offset=ft.Offset(0, 6)),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )


def matlab_section(page=None):
    w = (page.width or 800) if page else 800
    mobile = w < 700
    cards = [matlab_card(title, img_name, url) for title, img_name, url in MATLAB_COURSES]
    if mobile:
        row1 = ft.Row(cards, alignment=ft.MainAxisAlignment.CENTER, spacing=12, wrap=True)
        row2 = ft.Container(height=0)
    else:
        row1 = ft.Row(cards[:4], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        row2 = ft.Row(cards[4:], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # --- Interactive Ohm's Law Calculator ---
    calc_voltage = ft.TextField(
        label="Voltage V (volts)", width=160,
        text_size=13, border_color=GOLD, focused_border_color=GOLD_LT,
        label_style=ft.TextStyle(color=MUTED, size=11),
        text_style=ft.TextStyle(color=DARK, size=13),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    calc_current = ft.TextField(
        label="Current I (amps)", width=160,
        text_size=13, border_color=GOLD, focused_border_color=GOLD_LT,
        label_style=ft.TextStyle(color=MUTED, size=11),
        text_style=ft.TextStyle(color=DARK, size=13),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    calc_resistance = ft.TextField(
        label="Resistance R (ohms)", width=160,
        text_size=13, border_color=GOLD, focused_border_color=GOLD_LT,
        label_style=ft.TextStyle(color=MUTED, size=11),
        text_style=ft.TextStyle(color=DARK, size=13),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    calc_result = ft.Text(
        "Fill in any two fields →",
        size=13, color=MUTED, italic=True,
        text_align=ft.TextAlign.CENTER,
    )
    calc_power = ft.Text("", size=11, color=LEAF_GREEN, text_align=ft.TextAlign.CENTER)

    def do_calc(e):
        def safe(tf):
            try:
                v = float(tf.value.strip())
                return v if v != 0 else None
            except Exception:
                return None
        V = safe(calc_voltage)
        I = safe(calc_current)
        R = safe(calc_resistance)
        filled = [x for x in [V, I, R] if x is not None]
        if len(filled) < 2:
            calc_result.value = "Fill in any two fields →"
            calc_result.color = MUTED
            calc_power.value = ""
        elif V is None:
            V2 = I * R
            calc_result.value = f"V = I × R  =  {I} × {R}  =  {V2:.4g} V"
            calc_result.color = DARK
            calc_power.value = f"Power P = I²R = {I**2 * R:.4g} W"
        elif I is None:
            if R == 0:
                calc_result.value = "R cannot be zero"
                calc_result.color = "#c0392b"
                calc_power.value = ""
            else:
                I2 = V / R
                calc_result.value = f"I = V ÷ R  =  {V} ÷ {R}  =  {I2:.4g} A"
                calc_result.color = DARK
                calc_power.value = f"Power P = V²/R = {V**2 / R:.4g} W"
        elif R is None:
            if I == 0:
                calc_result.value = "I cannot be zero"
                calc_result.color = "#c0392b"
                calc_power.value = ""
            else:
                R2 = V / I
                calc_result.value = f"R = V ÷ I  =  {V} ÷ {I}  =  {R2:.4g} Ω"
                calc_result.color = DARK
                calc_power.value = f"Power P = V×I = {V * I:.4g} W"
        else:
            calc_result.value = "Clear one field to calculate"
            calc_result.color = MUTED
            calc_power.value = ""
        calc_result.update()
        calc_power.update()

    def clear_calc(e):
        calc_voltage.value = ""
        calc_current.value = ""
        calc_resistance.value = ""
        calc_result.value = "Fill in any two fields →"
        calc_result.color = MUTED
        calc_power.value = ""
        calc_voltage.update()
        calc_current.update()
        calc_resistance.update()
        calc_result.update()
        calc_power.update()

    calc_widget = ft.Container(
        content=ft.Column(
            [
                ft.Text("⚡ LIVE OHM'S LAW CALCULATOR", size=11, color=GOLD,
                        weight=ft.FontWeight.W_900, font_family="Arial",
                        text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Inspired by my MATLAB App Designer project — try it yourself!",
                    size=11, color=MUTED, italic=True, text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=16),
                ft.Row(
                    [calc_voltage, calc_current, calc_resistance],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    wrap=True,
                    run_spacing=12,
                ),
                ft.Container(height=14),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Calculate",
                            on_click=do_calc,
                            style=ft.ButtonStyle(
                                bgcolor={ft.ControlState.DEFAULT: GOLD,
                                         ft.ControlState.HOVERED: GOLD_LT},
                                color={ft.ControlState.DEFAULT: WHITE},
                                shape=ft.RoundedRectangleBorder(radius=4),
                            ),
                        ),
                        ft.OutlinedButton(
                            "Clear",
                            on_click=clear_calc,
                            style=ft.ButtonStyle(
                                color={ft.ControlState.DEFAULT: MUTED,
                                        ft.ControlState.HOVERED: DARK},
                                side={ft.ControlState.DEFAULT: ft.BorderSide(1, MUTED)},
                                shape=ft.RoundedRectangleBorder(radius=4),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
                ft.Container(height=12),
                calc_result,
                calc_power,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        ),
        bgcolor=WHITE,
        border_radius=8,
        border=ft.Border.all(1, "#33b8975a"),
        shadow=ft.BoxShadow(blur_radius=20, color="#14000000", offset=ft.Offset(0, 6)),
        padding=ft.Padding(left=20, right=20, top=28, bottom=28),
        width=640,
    )

    calc_widget = ft.Container(
        content=calc_widget,
        alignment=ft.Alignment(x=0, y=0),
        expand=True,
    )

    body = ft.Column(
        [
            ft.Container(height=20),
            ft.Text(
                "MathWorks Learning",
                size=13, color=DARK, weight=ft.FontWeight.W_700,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=14),
            txt("MATLAB ACHIEVEMENT HUB", size=30 if mobile else 48, color=GOLD,
                weight=ft.FontWeight.W_700, align=ft.TextAlign.CENTER),
            ft.Container(height=30),
            row1,
            ft.Container(height=24),
            row2,
            ft.Container(height=48),
            calc_widget,
            ft.Container(height=40),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        key="sec3",
        content=leaf_section(body, height=1200, page=page),
    )


# TECHNICAL BLOG
BLOG_CARD_W  = 420
SIDE_CARD_H  = 340   # left and right — tight to content
MID_CARD_H   = 500   # middle — extends equally above and below side cards


def math_formula_block(lines, pad):
    """
    All formulas on ONE horizontal line, separated by gold dots.
    Fractions show a solid visible dark division line between numerator and denominator.
    """
    def fraction_widget(label, numer, denom=None):
        if denom:
            line_width = max(max(len(numer), len(denom)) * 8, 30)
            frac = ft.Column(
                [
                    ft.Text(numer, size=12, color=DARK,
                            weight=ft.FontWeight.W_500, font_family="Georgia",
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=3),
                    ft.Container(width=line_width, height=2, bgcolor=DARK),
                    ft.Container(height=3),
                    ft.Text(denom, size=12, color=DARK,
                            weight=ft.FontWeight.W_500, font_family="Georgia",
                            text_align=ft.TextAlign.CENTER),
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            )
        else:
            frac = ft.Text(numer, size=13, color=DARK,
                           weight=ft.FontWeight.W_500, font_family="Georgia")

        return ft.Row(
            [
                ft.Text(label + " =", size=13, color=DARK,
                        weight=ft.FontWeight.W_700, font_family="Georgia"),
                ft.Container(width=7),
                frac,
            ],
            spacing=0,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    items = []
    for i, entry in enumerate(lines):
        items.append(fraction_widget(*entry))
        if i < len(lines) - 1:
            items.append(
                ft.Container(
                    content=ft.Text("·", size=18, color=GOLD,
                                    weight=ft.FontWeight.W_700),
                    padding=ft.Padding(left=12, right=12, top=0, bottom=0),
                )
            )

    return ft.Container(
        content=ft.Row(
            items,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            tight=True,
            wrap=True,
        ),
        bgcolor=CREAM,
        border=ft.Border(left=ft.BorderSide(3, GOLD)),
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
        margin=ft.Margin(left=pad, right=pad, top=0, bottom=pad),
    )


def blog_card(tag, title, body_text, math_lines=None, video_url="https://www.youtube.com",
              show_watch=False, small=False, card_height=None, mobile=False):
    tag_size   = 9  if small else 10
    title_size = 13 if small else 16
    body_size  = 10 if small else 12
    pad        = 16 if small else 22
    top_bar    = 3  if small else 4

    top_section = ft.Column(
        [
            ft.Text(tag, size=tag_size, color=GOLD, weight=ft.FontWeight.W_700,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=6),
            txt(title, size=title_size, color=DARK, weight=ft.FontWeight.W_700,
                align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.Text(body_text, size=body_size, color=MUTED, weight=ft.FontWeight.W_300),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    bottom_items = []
    if math_lines:
        bottom_items.append(math_formula_block(math_lines, pad))
    if show_watch:
        bottom_items.append(
            ft.Container(
                content=fv.Video(
                    playlist=[fv.VideoMedia("/Reflection video.mp4")],
                    autoplay=False, muted=False, show_controls=True, aspect_ratio=16/9,
                ),
                margin=ft.Margin(left=pad, right=pad, top=5, bottom=pad),
                height=220 if mobile else 260,
            )
        )

    # On mobile: no expand, no fixed height — card sizes to content
    # On desktop: expand fills the fixed card_height so all cards in a Row align
    inner = ft.Column(
        [
            ft.Container(
                content=top_section,
                padding=ft.Padding(left=pad, right=pad, top=pad, bottom=10),
            ),
            ft.Column(bottom_items, spacing=0),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
        expand=not mobile,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    height=top_bar, bgcolor=GOLD,
                    border_radius=ft.BorderRadius(top_left=4, top_right=4,
                                                  bottom_left=0, bottom_right=0),
                ),
                ft.Container(content=inner, expand=not mobile),
            ],
            spacing=0,
            expand=not mobile,
        ),
        bgcolor=WHITE,
        border_radius=4,
        border=ft.Border.all(1, "#22b8975a"),
        shadow=ft.BoxShadow(blur_radius=16, color="#14000000", offset=ft.Offset(0, 4)),
        width=BLOG_CARD_W if not mobile else None,
        height=card_height if not mobile else None,
    )


def blog_section(page=None):
    w = (page.width or 800) if page else 800
    mobile = w < 700
    # Ohm's Law formulas — proper fraction style
    ohms_law = [
        ("V", "I × R",  None),
        ("I", "V",      "R"),
        ("R", "V",      "I"),
        ("P", "I² × R", None),
    ]

    # Beam calculator formulas — fraction style
    beam = [
        ("M", "w × L²",          "2"),
        ("V", "w × L",           "2"),
        ("δ", "5 × w × L⁴",     "384 × E × I"),
    ]

    left_card = blog_card(
        "MATLAB",
        "MY JOURNEY WITH MATLAB",
        "This was my first time hearing and using MATLAB. I learned to write scripts, use matrices, "
        "and apply loops and conditionals. In my App Designer assignment, I built an Ohm's Law "
        "Calculator with input fields, a dropdown for DC/AC circuits, a calculate button, a reset "
        "button, and a plot. The formulas I used were V=I×R, I=V/R, R=V/I, and P=I²×R. "
        "Through the online MathWorks courses, I also learned how to simulate circuits using "
        "Simulink, which is very useful for my journey as an electrical engineering student. "
        "I completed 7 self-paced courses and earned certificates in MATLAB Fundamentals, "
        "Simulink Basics, and Circuit Simulation. I also learned that MATLAB is an interpreted "
        "language, unlike C which is compiled. This semester proved that programming is about "
        "solving engineering problems, one function at a time.",
        math_lines=ohms_law,
        show_watch=False,
        small=True,
        card_height=None if mobile else SIDE_CARD_H,
        mobile=mobile,
    )

    middle_card = blog_card(
        "MineShield · Testing and QA Lead",
        "MY JOURNEY THROUGH THE MINESHIELD APP",
        "As Testing and QA Lead for a 19-person team, I wrote tests, found 10 bugs, and helped "
        "ensure that every safety feature worked before submission. Mining safety depends on "
        "software that works — and I made sure it did.\n\n"
        "Watch the video for my full reflection and how my role contributed to the project and the real world.",
        show_watch=True,
        small=False,
        card_height=None if mobile else MID_CARD_H,
        mobile=mobile,
    )

    right_card = blog_card(
        "Python · C · JavaScript",
        "MY JOURNEY WITH OTHER LANGUAGES",
        "Beyond MATLAB, I learned Python, C, and JavaScript through my assignments and take-home "
        "test. In my banking system assignment, I built a Python program with deposit, withdraw, "
        "transfer, and balance check features, using a while loop to keep the menu running until "
        "exit. During my take-home test, I wrote a student grade analyser using functions like "
        "get_average() and get_grade() with if-elif-else decision structures. In the same test, "
        "I wrote a C program for temperature conversion using arrays, loops, and functions like "
        "to_fahrenheit(), find_max(), and find_average(), marking temperatures above 30°C as HOT. "
        "I also built a simply supported beam calculator in JavaScript using formulas "
        "M=(w×L²)/2, V=w×L/2, and δ=(5×w×L⁴)/(384×E×I), with input validation to handle errors. "
        "Each assignment taught me that once you understand variables, loops, conditionals, and "
        "functions, you can adapt to any language.",
        math_lines=beam,
        show_watch=False,
        small=True,
        card_height=None if mobile else SIDE_CARD_H,
        mobile=mobile,
    )

    if mobile:
        cards = ft.Column(
            [left_card, middle_card, right_card],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    else:
        cards = ft.Row(
            [left_card, middle_card, right_card],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=28,
            wrap=False,
        )

    body = ft.Column(
        [
            ft.Container(height=40),
            txt("TECHNICAL BLOG", size=32 if mobile else 60, color=GOLD, weight=ft.FontWeight.W_900),
            ft.Container(height=40),
            cards,
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        key="sec4",
        content=leaf_section(body, height=800, page=page),
    )


# MINESHIELD
def mineshield_section(page=None):
    w = (page.width or 800) if page else 800
    mobile = w < 700
    # --- Full-width hero banner (logo image + text overlay, inspo style) ---
    ms_hero_h = 280 if mobile else 520
    hero_img = ft.Image(
        src=LOGO_B64,
        fit=ft.BoxFit.CONTAIN,
        width=9999,
        height=ms_hero_h,
    )
    hero_overlay = ft.Container(expand=True, bgcolor="#99000000")

    hero_text = ft.Column(
        [
            ft.Container(height=30 if mobile else 80),
            ft.Text(
                "2 0 2 6   P R O J E C T",
                size=34 if mobile else 86,
                color=WHITE,
                weight=ft.FontWeight.W_900,
                text_align=ft.TextAlign.CENTER,
                font_family="Arial",
            ),
            ft.Container(height=-45),
            ft.Text(
                "↓  Scroll down for more information",
                size=12,
                color="#CCffffff",
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_900,
                font_family="Arial",
                italic=True,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    logo = ft.Container(
        content=ft.Stack([
            hero_img,
            hero_overlay,
            ft.Container(
                content=hero_text,
                alignment=ft.Alignment(x=0, y=0),
                expand=True,
                height=ms_hero_h,
            ),
        ]),
        height=ms_hero_h,
        bgcolor=WHITE,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # --- Feature cards (no icons, uniform size, gold border, dark bold title, aligned rows) ---
    CARD_W = 210
    CARD_H = 130

    def feature_card(title, desc):
        c = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(title, size=13, color=DARK, weight=ft.FontWeight.W_700,
                                        font_family="Arial", text_align=ft.TextAlign.CENTER),
                        height=36,
                        alignment=ft.Alignment(x=0, y=0),
                    ),
                    ft.Container(
                        content=ft.Text(desc, size=11, color=MUTED, weight=ft.FontWeight.W_300,
                                        text_align=ft.TextAlign.CENTER),
                        alignment=ft.Alignment(x=0, y=-1),
                    ),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.START,
            ),
            width=CARD_W,
            height=CARD_H,
            padding=ft.Padding(left=18, right=18, top=5, bottom=16),
            bgcolor=WHITE,
            border=ft.Border.all(1.5, GOLD),
            border_radius=4,
            shadow=ft.BoxShadow(blur_radius=10, color="#14000000", offset=ft.Offset(0, 3)),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            ink=True,
        )
        def on_hover(e):
            if e.data == "true":
                c.bgcolor = "#fff8ee"
                c.shadow = ft.BoxShadow(blur_radius=22, color="#33b8975a", offset=ft.Offset(0, 6))
            else:
                c.bgcolor = WHITE
                c.shadow = ft.BoxShadow(blur_radius=10, color="#14000000", offset=ft.Offset(0, 3))
            c.update()
        c.on_hover = on_hover
        return c

    features = ft.Row(
        [
            feature_card("Real-Time Safety Monitoring",
                "Live map with colour-coded risk zones: Green = Safe, Yellow = Warning, Red = Danger."),
            feature_card("Fall Detection & SOS",
                "Accelerometer-based fall detection triggers an automatic SOS if the worker is unresponsive."),
            feature_card("Hazard Reporting",
                "Workers report hazards with photos and GPS location data instantly from their device."),
            feature_card("Noise Monitoring",
                "Continuous noise level tracking alerts workers when sound exceeds safe thresholds."),
            feature_card("Analytics Dashboard",
                "Supervisors view safety trends and incident history through a live analytics dashboard."),
            feature_card("Visitor Mode",
                "Read-only access for site visitors to stay informed without editing live safety data."),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        wrap=True,
    )

    # --- About section ---
    about_block = ft.Column(
        [
            ft.Container(height=1),
            ft.Text(
                "MineShield is a real-time safety monitoring mobile application developed for "
                "mining environments, designed to transform standard Android devices into intelligent "
                "personal safety tools. The app enables workers to report hazards with photos and "
                "location data, automatically detects falls using the phone's accelerometer (triggering "
                "an SOS if the worker is unresponsive), and provides supervisors with a live map "
                "displaying colour-coded risk zones. Additional features include one-tap SOS broadcasting "
                "with last known GPS location, noise level monitoring, an analytics dashboard for safety "
                "trends, and a read-only visitor mode. Built with React Native and Firebase, MineShield "
                "ensures faster emergency response times and improved situational awareness across all "
                "operational roles.",
                size=13, color=MUTED, weight=ft.FontWeight.W_300,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=16),
            ft.TextButton(
                "View Repository on GitHub →",
                url="https://github.com/raunanehale06-png/UNAM-I3691CP-Group-16-Mineshield",
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.DEFAULT: GOLD,
                        ft.ControlState.HOVERED: GOLD_LT,
                    },
                    overlay_color=ft.Colors.TRANSPARENT,
                    padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                ),
            ),
            ft.Container(height=40),
            features,
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- Team photos (side by side) ---
    ph_w = None if mobile else 400
    ph_h = 200 if mobile else 290

    def photo_frame(src, caption):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Image(src=src, fit=ft.BoxFit.COVER, width=ph_w, height=ph_h),
                    width=ph_w, height=ph_h, expand=mobile,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    border_radius=4,
                    border=ft.Border.all(1, "#33b8975a"),
                    shadow=ft.BoxShadow(blur_radius=16, color="#1a000000", offset=ft.Offset(0, 6)),
                ),
                ft.Container(height=8),
                ft.Text(caption, size=11, color=MUTED, italic=True,
                        text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=mobile,
        )

    if mobile:
        team_photos = ft.Column(
            [
                photo_frame(TEAM1_B64, "Team working session — building MineShield together"),
                photo_frame(TEAM2_B64, "Group 16"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    else:
        team_photos = ft.Row(
            [
                photo_frame(TEAM1_B64, "Team working session — building MineShield together"),
                photo_frame(TEAM2_B64, "Group 16"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=28,
        )

    # --- My role & reflection ---
    reflection_block = ft.Container(
        content=ft.Column(
            [
                ft.Text("MY ROLE · TESTING & QUALITY ASSURANCE LEAD",
                        size=11, color=GOLD, weight=ft.FontWeight.W_900,
                        font_family="Arial", text_align=ft.TextAlign.CENTER),
                ft.Container(height=16),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Looking back at this project from Phase 1 to Phase 3, I realise how much my role as "
                                "Testing & QA Lead grew alongside the app itself. When we started in Phase 1, I was "
                                "honestly overwhelmed — 19 team members, 15 functional requirements, and three different "
                                "Android devices to test on. But I sat down with the SRS, mapped every single requirement "
                                "to a test case, and built my testing plan from the ground up.",
                                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                            ),
                            ft.Container(height=12),
                            ft.Text(
                                "Phase 2 was where the real work happened. As my teammates built features like hazard "
                                "reporting, fall detection, and SOS alerts, I was right there testing each one as soon "
                                "as it was ready. I found 10 bugs along the way, and I will never forget the panic of "
                                "discovering that the app crashed on Android 16 every time a worker tried to upload a "
                                "hazard photo. That was one of the critical bugs — if it had gone unnoticed, miners "
                                "using newer phones could not have documented loose rock or gas leaks. I reported it "
                                "immediately, and watching the developer fix it felt like a small victory for mining safety.",
                                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                            ),
                            ft.Container(height=12),
                            ft.Text(
                                "By Phase 3, all the code was merged, and I ran regression tests to make sure nothing "
                                "had broken. Everything passed. My six commits to the repository reflect this entire "
                                "journey. My unit tests (auth.test.js and hazard.test.js) make sure only authorised "
                                "workers can log in and that every hazard report is stored correctly. My end-to-end tests "
                                "(workflow.test.js) simulate real mining scenarios — a worker finding a hazard, a supervisor "
                                "resolving it, a visitor staying informed. I did not build the buttons or the maps, but I "
                                "made sure they work when a miner's life depends on them. That is what I am most proud of.",
                                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                            ),
                            ft.Container(height=12),
                            ft.Text(
                                "My primary contribution to the MineShield Mining Safety module was ensuring "
                                "the reliability of its core safety-critical features. I wrote and executed "
                                "test cases covering the gas detection alerts, fall detection SOS, hazard "
                                "reporting, and emergency contact system — identifying 10 bugs before "
                                "submission. In a real mining environment, a software failure in any of "
                                "these features could result in loss of life. My QA work directly ensured "
                                "that the Mining module functioned correctly under edge cases such as empty "
                                "inputs, invalid GPS data, and unsupported Android versions. Without this "
                                "testing, the app could not be trusted in a production mining context.",
                                size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.Padding(left=14 if mobile else 32, right=14 if mobile else 32, top=28, bottom=28),
                    bgcolor=WHITE,
                    border=ft.Border(left=ft.BorderSide(3, GOLD)),
                    border_radius=ft.BorderRadius(top_left=0, top_right=4, bottom_left=0, bottom_right=4),
                    shadow=ft.BoxShadow(blur_radius=12, color="#14000000", offset=ft.Offset(0, 4)),
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=8 if mobile else 40, right=8 if mobile else 40, top=0, bottom=0),
    )

    # --- Assigned files table ---
    assigned_files = [
        ("1", "tests/unit/auth.test.js",       "Code"),
        ("2", "tests/unit/hazard.test.js",      "Code"),
        ("3", "tests/e2e/workflow.test.js",      "Code"),
        ("4", "docs/TEST_CASES.md",              "Doc"),
        ("5", "docs/BUG_REPORT.md",              "Doc"),
        ("6", "docs/TEST_COVERAGE.md",           "Doc"),
    ]

    def table_header_cell(label, flex):
        return ft.Container(
            content=ft.Text(label, size=11, color=WHITE,
                            weight=ft.FontWeight.W_600, font_family="Arial"),
            padding=ft.Padding(left=14, right=14, top=10, bottom=10),
            expand=flex,
        )

    def table_row(no, path, ftype, is_even):
        bg = "#f9f6f0" if is_even else WHITE
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text(no, size=11, color=MUTED),
                        padding=ft.Padding(left=14, right=14, top=9, bottom=9),
                        expand=1,
                    ),
                    ft.Container(
                        content=ft.Text(path, size=11, color=DARK,
                                        font_family="Courier New"),
                        padding=ft.Padding(left=14, right=14, top=9, bottom=9),
                        expand=5,
                    ),
                    ft.Container(
                        content=ft.Container(
                            content=ft.Text(ftype, size=10, color=GOLD),
                            padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                            border_radius=0,
                        ),
                        padding=ft.Padding(left=14, right=14, top=6, bottom=6),
                        expand=2,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=bg,
            border=ft.Border(bottom=ft.BorderSide(1, "#eae4da")),
        )

    header_row = ft.Container(
        content=ft.Row(
            [
                table_header_cell("No.", 1),
                table_header_cell("File Path", 5),
                table_header_cell("Type", 2),
            ],
            spacing=0,
        ),
        bgcolor=DARK,
        border_radius=ft.BorderRadius(top_left=4, top_right=4, bottom_left=0, bottom_right=0),
    )

    rows = [table_row(no, path, ftype, i % 2 == 0)
            for i, (no, path, ftype) in enumerate(assigned_files)]

    footer_row = ft.Container(
        content=ft.Row(
            [
                ft.Container(width=8),
                ft.Text("ALL 6 FILES COMMITED",
                        size=12, color=GOLD, weight=ft.FontWeight.W_900, text_align=ft.TextAlign.CENTER),
            ],
            spacing=0,
        ),
        bgcolor=CREAM,
        border=ft.Border(
            left=ft.BorderSide(1, "#ccdecc"),
            right=ft.BorderSide(1, "#ccdecc"),
            bottom=ft.BorderSide(1, "#ccdecc"),
        ),
        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=4, bottom_right=4),
        padding=ft.Padding(left=14, right=14, top=10, bottom=10),
    )

    files_table = ft.Container(
        content=ft.Column(
            [header_row] + rows + [footer_row],
            spacing=0,
        ),
        border=ft.Border.all(1, "#33b8975a"),
        border_radius=4,
        shadow=ft.BoxShadow(blur_radius=12, color="#14000000", offset=ft.Offset(0, 4)),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        width=None,
        expand=True,
    )

    assigned_block = ft.Column(
        [
            ft.Text("ASSIGNED", size=11, color=GOLD, weight=ft.FontWeight.W_600,
                    font_family="Arial", text_align=ft.TextAlign.CENTER),
            ft.Container(height=4),
            ft.Text("My 6 committed files across test code and documentation",
                    size=12, color=MUTED, weight=ft.FontWeight.W_300,
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            files_table,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # --- Evidence images (side by side) ---
    ev_w = None if mobile else 480
    ev_h = 180 if mobile else 300

    def evidence_frame(src, caption, w=None, h=None):
        fw = w or ev_w
        fh = h or ev_h
        return ft.Column(
            [
                ft.Container(
                    content=ft.Image(src=src, fit=ft.BoxFit.CONTAIN, width=fw, height=fh),
                    width=fw, height=fh, expand=mobile,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    border_radius=4,
                    border=ft.Border.all(1, "#33b8975a"),
                    bgcolor=WHITE,
                    shadow=ft.BoxShadow(blur_radius=16, color="#1a000000", offset=ft.Offset(0, 6)),
                ),
                ft.Container(height=8),
                ft.Text(caption, size=11, color=MUTED, italic=True,
                        text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=mobile,
        )

    if mobile:
        evidence_row1 = ft.Column(
            [
                evidence_frame(EVIDENCE1_B64, "GitHub Insights — contributor activity across the project period"),
                evidence_frame(EVIDENCE2_B64, "GitHub commit history — verified commits on main branch"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    else:
        evidence_row1 = ft.Row(
            [
                evidence_frame(EVIDENCE1_B64, "GitHub Insights — contributor activity across the project period"),
                evidence_frame(EVIDENCE2_B64, "GitHub commit history — verified commits on main branch"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=28,
        )

    body = ft.Column(
        [
            about_block,
            ft.Container(height=56),
            gold_line(),
            ft.Container(height=40),
            ft.Text("THE TEAM", size=11, color=GOLD, weight=ft.FontWeight.W_900,
                    font_family="Arial", text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            team_photos,
            ft.Container(height=56),
            gold_line(),
            ft.Container(height=40),
            reflection_block,
            ft.Container(height=56),
            gold_line(),
            ft.Container(height=40),
            assigned_block,
            ft.Container(height=56),
            gold_line(),
            ft.Container(height=40),
            ft.Text("CONTRIBUTION EVIDENCE", size=11, color=GOLD, weight=ft.FontWeight.W_900,
                    font_family="Arial", text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.Text(
                "Screenshots from the GitHub repository demonstrating my commits and activity throughout the project (My Github Username: Plasma2000)",
                size=12, color=MUTED, weight=ft.FontWeight.W_300,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=24),
            evidence_row1,
            ft.Container(height=32),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("PULL REQUEST LOG AND WORKFLOW", size=10, color=GOLD,
                                        weight=ft.FontWeight.W_900, font_family="Arial",
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(
                                    "The 9 pull requests in our repository were opened by the group leader "
                                    "and one other member early in the project, when the team still intended "
                                    "to follow a formal PR workflow. As the project scaled and deadlines "
                                    "tightened across all 19 members, our GitHub manager made the decision "
                                    "to switch to direct commits on main to keep contributions moving. "
                                    "From that point, all coordination happened through WhatsApp and "
                                    "face-to-face working sessions. My 6 commits reflect this agreed "
                                    "workflow — each one intentional and tied to a specific QA deliverable.",
                                    size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.Padding(left=28, right=28, top=26, bottom=26),
                        bgcolor=WHITE,
                        border=ft.Border(left=ft.BorderSide(3, GOLD)),
                        border_radius=ft.BorderRadius(top_left=0, top_right=4, bottom_left=0, bottom_right=4),
                        shadow=ft.BoxShadow(blur_radius=12, color="#14000000", offset=ft.Offset(0, 4)),
                        width=None,
                        height=None,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("CODE REVIEW ACTIVITY", size=10, color=GOLD,
                                        weight=ft.FontWeight.W_900, font_family="Arial",
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(
                                    "As QA Lead, code review was central to my role. I reviewed teammate "
                                    "implementations against the functional requirements, identifying and "
                                    "documenting 10 bugs before final submission — covering edge cases across "
                                    "multiple modules and Android versions. Every finding is formally "
                                    "recorded in docs/BUG_REPORT.md in the repository.",
                                    size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.Padding(left=28, right=28, top=26, bottom=26),
                        bgcolor=WHITE,
                        border=ft.Border(left=ft.BorderSide(3, GOLD)),
                        border_radius=ft.BorderRadius(top_left=0, top_right=4, bottom_left=0, bottom_right=4),
                        shadow=ft.BoxShadow(blur_radius=12, color="#14000000", offset=ft.Offset(0, 4)),
                        width=None,
                        height=None,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("PROFESSIONAL REFLECTION", size=10, color=GOLD,
                                        weight=ft.FontWeight.W_900, font_family="Arial",
                                        text_align=ft.TextAlign.CENTER),
                                ft.Container(height=10),
                                ft.Text(
                                    "Managing QA across a 19-member team taught me that documentation is "
                                    "your strongest evidence. My 6 commits, TEST_CASES.md, BUG_REPORT.md, "
                                    "and TEST_COVERAGE.md create a clear, verifiable record of my "
                                    "contribution. In future projects I will enforce PR-based reviews from "
                                    "day one — structured process protects both quality and accountability.",
                                    size=13, color="#5a4e3d", weight=ft.FontWeight.W_300,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        padding=ft.Padding(left=28, right=28, top=26, bottom=26),
                        bgcolor=WHITE,
                        border=ft.Border(left=ft.BorderSide(3, GOLD)),
                        border_radius=ft.BorderRadius(top_left=0, top_right=4, bottom_left=0, bottom_right=4),
                        shadow=ft.BoxShadow(blur_radius=12, color="#14000000", offset=ft.Offset(0, 4)),
                        width=None,
                        height=None,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
                wrap=True,
            ),
            ft.Container(height=40),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        key="sec_mineshield",
        content=ft.Column(
            [
                logo,
                leaf_section(body, page=page),
            ],
            spacing=0,
        ),
    )





# FOOTER 
def footer():
    return ft.Container(
        content=ft.Column(
            [
                gold_line(),
                ft.Container(height=28),
                ft.Text("LET'S CONNECT", size=10, color=GOLD,
                        weight=ft.FontWeight.W_700, font_family="Arial"),
                ft.Container(height=12),
                ft.TextButton(
                    "negongateopolina@gmail.com",
                    url="mailto:teopolinanegonga@gmail.com",
                    style=ft.ButtonStyle(
                        color={ft.ControlState.DEFAULT: "#99f5f0e8",
                               ft.ControlState.HOVERED: GOLD_LT},
                        overlay_color=ft.Colors.TRANSPARENT,
                        padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                    ),
                ),
                ft.TextButton(
                    "💼  github.com/Plasma2000",
                    url="https://github.com/Plasma2000",
                    style=ft.ButtonStyle(
                        color={ft.ControlState.DEFAULT: "#99f5f0e8",
                               ft.ControlState.HOVERED: GOLD_LT},
                        overlay_color=ft.Colors.TRANSPARENT,
                        padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                    ),
                ),
                ft.Container(height=20),
                ft.Text("© 2026  Teopolina Negonga", size=11, color="#66f5f0e8"),
                ft.Text("Electrical Engineering · University of Namibia",
                        size=10, color="#44f5f0e8"),
                ft.Container(height=8),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
        ),
        bgcolor="#1a1208",
        padding=ft.Padding(left=0, right=0, top=10, bottom=15),
        alignment=ft.Alignment(x=0, y=0),
    )


# MAIN
def main(page: ft.Page):
    page.title = "Teopolina Negonga | Portfolio"
    page.bgcolor = CREAM
    page.padding = 0
    page.theme = ft.Theme(font_family="Arial")

    def scrollable(content):
        return ft.Column([content], scroll=ft.ScrollMode.ALWAYS, expand=True)

    current_idx = [0]

    def build_all():
        home_s  = home_section(page_ref=page)
        about_s = about_section(page=page)
        secs = [
            ft.Container(content=scrollable(home_s),  visible=(current_idx[0] == 0), expand=True),
            ft.Container(content=scrollable(about_s),  visible=(current_idx[0] == 1), expand=True),
            ft.Container(content=scrollable(matlab_section(page=page)),                                          visible=(current_idx[0] == 2), expand=True),
            ft.Container(content=scrollable(mineshield_section(page=page)),                                      visible=(current_idx[0] == 3), expand=True),
            ft.Container(content=scrollable(timeline_section(page=page)),                                        visible=(current_idx[0] == 4), expand=True),
            ft.Container(content=scrollable(ft.Column([blog_section(page=page), footer()], spacing=0)),          visible=(current_idx[0] == 5), expand=True),
        ]
        return home_s, about_s, secs

    home_sec, about_sec, sections = build_all()
    _bar_fills = about_sec._bar_fills

    nav_wrap  = ft.Container(top=0, left=0, right=0)
    secs_col  = ft.Column(sections, spacing=0, expand=True)

    def nav_with_skills(e, idx):
        current_idx[0] = idx
        for i, s in enumerate(sections):
            s.visible = (i == idx)
        page.update()
        if idx == 1:
            bar_w = 180 if (page.width or 800) < 700 else 240
            def animate():
                time.sleep(0.2)
                for fill, level in _bar_fills:
                    fill.width = int(bar_w * level)
                    try: fill.update()
                    except Exception: pass
            threading.Thread(target=animate, daemon=True).start()

    last_w = [page.width or 0]

    def on_resize(e):
        nonlocal home_sec, about_sec, sections, _bar_fills
        new_w = page.width or 0
        # only rebuild when crossing the 700 px breakpoint
        was_mobile = last_w[0] < 700
        now_mobile = new_w < 700
        last_w[0] = new_w
        if was_mobile == now_mobile:
            return
        home_sec, about_sec, sections = build_all()
        _bar_fills = about_sec._bar_fills
        secs_col.controls = sections
        nav_wrap.content = nav_bar(sections, page, on_navigate=nav_with_skills)
        try:
            nav_wrap.update()
            secs_col.update()
        except Exception:
            pass
        t = threading.Thread(target=home_sec._cycle, args=(page,), daemon=True)
        t.start()

    page.on_resized = on_resize

    nav_wrap.content = nav_bar(sections, page, on_navigate=nav_with_skills)
    page.overlay.append(nav_wrap)
    page.add(secs_col)

    t = threading.Thread(target=home_sec._cycle, args=(page,), daemon=True)
    t.start()


ft.app(main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")
