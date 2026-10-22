# Soumy Raghuvanshi — Midnight Cyan Editorial Developer Portfolio

A developer portfolio crafted with an editorial design system, typography-led hierarchy, and interactive motion.

---

## 🎨 Design System: Midnight Cyan / Ice Black

- **Main Background:** `#0B0D0E` (pitch obsidian black)
- **Secondary Surface:** `#111418`
- **Elevated Cards:** `#161B22`
- **Primary Text:** `#F0F6FC` (crisp ice off-white)
- **Secondary Text:** `#9BA9B8` (cool muted slate)
- **Muted Text:** `#64748B` (slate gray)
- **Primary Accent:** `#38BDF8` (electric cyan / sky blue)
- **Secondary Accent:** `#00F0FF` (hyper laser cyan)
- **Subtle Borders:** `#1E293B`
- **Hover Borders:** `#334155`

### Typography Hierarchy
- **Hero Title & Masthead:** [Playfair Display](https://fonts.google.com/specimen/Playfair+Display) (luxury editorial serif with metallic luminescence)
- **Section Headings & Display:** [Outfit](https://fonts.google.com/specimen/Outfit) (smooth, contemporary geometric minimalism)
- **Body & Core Sans:** [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans)
- **Editorial Emphasis:** [Newsreader](https://fonts.google.com/specimen/Newsreader) (editorial serif italic)
- **Metadata, Tags & Dates:** [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono)

---

## 🚀 Key Sections & Features

1. **Interactive Navigation & Scroll Suite**
   - **Floating Interactive Side Rail Navigator:** Desktop quick-jump rail dock on the right edge with glowing section pips, tooltips, and real-time vertical tracking progress line.
   - **Interactive Circular Scroll Dial:** Floating circular SVG progress meter at bottom-right displaying live scroll percentage (`0%` -> `100%`) that transforms into an upward glide button on hover to smoothly return to top.
   - **Live Top Nav Meter:** Compact depth gauge inside the header showing real-time reading progress.
   - **Directional Smart Auto-Docking Nav:** Fluidly hides on fast downward scroll and instantly slides in on upward scroll with frosted Midnight Cyan glassmorphism.
   - **Scroll-Driven Reveal System:** High-performance `IntersectionObserver` that orchestrates silky upward glide entries for cards, headings, and panels as they enter the viewport.
   - **Hero Parallax & Explore Down:** Subtle 3D portrait frame parallax with an interactive "Explore Down" smooth glider.
   - **Interactive Custom Cursor Suite:** Two-part GPU-accelerated cursor (instant precision dot + fluid lerp follower ring) that contextually morphs on hover into an expanded interactive aura, a `"VIEW"` / `"EXPLORE"` glass lens over project and gallery cards, and emits tactile ripple shockwaves on click. Automatically disabled on touch screens.
   - Brand monogram `[SR]` with live status indicator (`Available · 2026`).
   - Built-in Web Audio API synthesized ambient drone with animated equalizer bars.
   - Mobile-responsive slide-out drawer.

2. **2-Column Split Hero with Cinematic Solo Dance Video Backdrop**
   - **Eye-Catching Solo Dance Video Backdrop:** Ambient full-screen solo performance video smoothly playing in the background behind the hero with custom Midnight Cyan scrims, directional text-readability gradients, and cyan particle grid mesh.
   - **Interactive Video Control Dock:** Floating control pill with live status badge (`● Solo Dance`), audio mute/unmute toggle (`🔊 Sound On`), video play/pause, and an instant local file tester (`📁 Test My Video`).
   - **Fullscreen Theater Mode:** Click `⛶ Theater View` to temporarily dim editorial text and watch the solo dance choreography in full brightness with sound.
   - **Local Video Placement:** Simply save your video file as `assets/solo-dance.mp4` (or `assets/dance-solo.mp4`) to load automatically on startup.
   - Fluid responsive typography: `SOUMY RAGHUVANSHI` with interactive letter hover transitions.
   - Live availability badge for Summer 2026 software engineering internships.
   - Editorial portrait frame with studio registration crosshairs.
   - **Interactive Photo Upload:** Click `+ Change Photo` to preview any portrait image from your local computer (automatically saved to `localStorage`).
   - **Layout Side Swapper:** Click `⇄ Swap Side` to toggle between Left and Right photo layout (persisted across sessions).

3. **01 / About**
   - Clean editorial narrative emphasizing engineering rigor, backend systems architecture, predictive machine learning, and creative discipline.

4. **02 / Skills & Technical Arsenal**
   - Interactive discipline filter tabs: `All`, `Languages`, `Backend & APIs`, `Databases & Cloud`, `AI, ML & Analytics`, `Tools & Principles`.
   - Distinct categorized cards with clean tech pills and count badges.

5. **03 / Selected Works (Projects)**
   - High-credibility engineering showcase featuring actual architecture previews:
     - **Food Business Demand Forecasting Engine** (`processed_assets/food_demand_ml.png`)
     - **Car Rental Management Backend Architecture** (`processed_assets/car_rental_architecture.png`)
   - Clickable interactive modal drawer (`Esc` or backdrop click to close) with comprehensive technical breakdown, system architecture decisions, and tech pills.

6. **04 / Moments & Discipline (Dance Dukes & Expeditions)**
   - Dance Dukes feature banner detailing performance rhythm, spatial awareness, and acrobatic lifts.
   - 3-card stage dance performance gallery with real photos and click-to-upload support.
   - Campus life, technical hackathons, and Kalsubai Peak Summit (1,646m) expedition showcase.

7. **05 / Work Experience**
   - MERN Stack Developer Intern at Parkhya Solutions Pvt. Ltd., Indore (20+ REST APIs, JWT/RBAC, Razorpay webhooks, Cloudinary CDN).

8. **06 / Perspective (Inspiration Carousel)**
   - Large editorial quote carousel with quotation glyph, smooth fade transitions, and interactive indicator dots.

9. **07 / Connect**
   - 1-click email copy card (`soumy.raghuvanshi@example.com`) with clipboard API and toast notification.
   - Direct external links to LinkedIn, GitHub, and Resume PDF.
   - Minimalist editorial footer with smooth Back to Top button.

---

## 🏃 Running Locally

Launch the portfolio using any standard local server:

### Option A: Using Python (Recommended)
```powershell
cd "c:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio"
python -m http.server 3000
```
Then visit: **`http://localhost:3000`**

### Option B: Using Node.js / npx
```powershell
cd "c:\Users\SHREE RAM\.gemini\antigravity\scratch\soumy-portfolio"
npx serve .
```

### Option C: Direct File Opening
Double-click `index.html` to open directly in any modern web browser.
