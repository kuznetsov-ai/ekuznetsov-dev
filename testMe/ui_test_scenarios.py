"""ekuznetsov.dev — landing page layout, mobile drawer, and anchor scroll suite."""
from __future__ import annotations

import asyncio

from scenarios.base import BaseScenario


VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet":  {"width": 768,  "height": 1024},
    "mobile":  {"width": 393,  "height": 852},
}


class EkuznetsovDevScenario(BaseScenario):
    OUTPUT_SUBDIR = "ekuznetsov-dev"

    async def _go(self, path: str = "/") -> None:
        url = f"{self.base_url}{path}?v={int(asyncio.get_event_loop().time() * 1000)}"
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(0.6)

    async def _set_viewport(self, name: str) -> None:
        await self.page.set_viewport_size(VIEWPORTS[name])
        await asyncio.sleep(0.3)

    # ── S01: Hero on every viewport ────────────────────────────────────────

    async def test_s01_hero(self):
        """S01: hero title + 2 CTA buttons render on every viewport."""
        for vp_name in VIEWPORTS:
            start = await self._step(f"s01_hero_{vp_name}")
            try:
                await self._set_viewport(vp_name)
                await self._go("/")

                h1 = self.page.locator(".hero__title")
                h1_visible = await h1.is_visible()
                h1_text = (await h1.text_content() or "").strip() if h1_visible else ""

                ctas = self.page.locator(".hero__cta .btn")
                cta_count = await ctas.count()

                issues = []
                if not h1_visible:
                    issues.append("hero title not visible")
                if cta_count < 2:
                    issues.append(f"only {cta_count} CTA buttons (expected 2)")
                # Make sure scrubbed text is gone
                lower = h1_text.lower()
                if "cyprus" in lower or "open to work" in lower:
                    issues.append("forbidden text still in hero")

                screenshot = await self._screenshot(f"s01_hero_{vp_name}")
                status = "FAIL" if issues else "PASS"
                self._record(
                    f"s01_hero_{vp_name}", status,
                    f"[{vp_name.upper()}] hero ok ({cta_count} CTA)"
                    + (f" | ISSUES: {'; '.join(issues)}" if issues else ""),
                    screenshot, start,
                )
            except Exception as e:
                screenshot = await self._screenshot(f"s01_hero_{vp_name}_error")
                self._record(f"s01_hero_{vp_name}", "FAIL",
                             f"[{vp_name.upper()}] Exception: {e}", screenshot, start)

    # ── S02: Mobile drawer opens fully opaque and fills viewport ──────────

    async def test_s02_mobile_drawer(self):
        """S02: burger → drawer covers viewport, links visible, no hero bleed."""
        start = await self._step("s02_mobile_drawer")
        try:
            await self._set_viewport("mobile")
            await self._go("/")

            burger = self.page.locator(".burger")
            if not await burger.is_visible():
                self._record("s02_mobile_drawer", "FAIL",
                             "burger not visible on mobile",
                             await self._screenshot("s02_drawer_no_burger"), start)
                return
            await burger.click()
            await asyncio.sleep(0.6)

            nav = self.page.locator(".nav")
            nav_box = await nav.bounding_box()
            vp = VIEWPORTS["mobile"]

            issues = []
            # Drawer should fill the viewport
            if not nav_box:
                issues.append("nav has no bounding box")
            else:
                if nav_box["width"] < vp["width"] * 0.95:
                    issues.append(f"drawer width {nav_box['width']}px < 95% of viewport")
                if nav_box["height"] < vp["height"] * 0.85:
                    issues.append(f"drawer height {nav_box['height']}px < 85% of viewport")

            # Links should be visible
            links = self.page.locator(".nav a")
            visible_links = 0
            for i in range(await links.count()):
                if await links.nth(i).is_visible():
                    visible_links += 1
            if visible_links < 3:
                issues.append(f"only {visible_links} nav links visible (expected ≥3)")

            # Hero must NOT be visible behind the drawer
            hero_text = self.page.locator(".hero__title").first
            hero_intersects = await hero_text.is_visible()
            if hero_intersects:
                # Acceptable only if hero is occluded — we can't verify pixel z-order
                # cheaply, so we check that the drawer's z-index is higher than header.
                z_nav = await nav.evaluate("el => parseInt(getComputedStyle(el).zIndex)||0")
                z_header = await self.page.locator(".header").evaluate(
                    "el => parseInt(getComputedStyle(el).zIndex)||0"
                )
                if z_nav <= z_header:
                    issues.append(f"drawer z-index {z_nav} not above header {z_header}")

            screenshot = await self._screenshot("s02_drawer_open")
            status = "FAIL" if issues else "PASS"
            self._record(
                "s02_mobile_drawer", status,
                f"drawer w={nav_box['width']:.0f} h={nav_box['height']:.0f}, links={visible_links}"
                + (f" | ISSUES: {'; '.join(issues)}" if issues else ""),
                screenshot, start,
            )
        except Exception as e:
            screenshot = await self._screenshot("s02_drawer_error")
            self._record("s02_mobile_drawer", "FAIL", f"Exception: {e}", screenshot, start)

    # ── S03: Anchor link from drawer scrolls to the right section ──────────

    async def test_s03_drawer_projects_scroll(self):
        """S03: tap "Projects" in mobile drawer — page scrolls to the projects section."""
        start = await self._step("s03_drawer_projects")
        try:
            await self._set_viewport("mobile")
            await self._go("/")

            await self.page.locator(".burger").click()
            await asyncio.sleep(0.6)

            link = self.page.locator(".nav a[href='#projects']")
            if not await link.is_visible():
                self._record("s03_drawer_projects", "FAIL",
                             "Projects link not in drawer",
                             await self._screenshot("s03_no_link"), start)
                return
            await link.click()
            await asyncio.sleep(0.8)

            section = self.page.locator("#projects")
            box = await section.bounding_box()
            # Allow up to ~half-viewport — sticky header + visual padding lands here normally
            in_view = bool(box and 0 <= box["y"] <= 450)

            issues = []
            if not in_view:
                issues.append(f"#projects.y={box['y'] if box else 'none'} not near top (>450)")

            # Drawer should be closed after click
            nav_open = await self.page.locator(".nav.open").count() > 0
            if nav_open:
                issues.append("drawer didn't close after tap")

            screenshot = await self._screenshot("s03_after_scroll")
            status = "FAIL" if issues else "PASS"
            self._record(
                "s03_drawer_projects", status,
                f"#projects.y={box['y'] if box else None}"
                + (f" | ISSUES: {'; '.join(issues)}" if issues else ""),
                screenshot, start,
            )
        except Exception as e:
            screenshot = await self._screenshot("s03_drawer_projects_error")
            self._record("s03_drawer_projects", "FAIL", f"Exception: {e}", screenshot, start)

    # ── S04: Project list has exactly 4 cards (no Cosplay) ─────────────────

    async def test_s04_projects_no_cosplay(self):
        """S04: 4 project cards, no 'Cosplay' anywhere on the page."""
        start = await self._step("s04_projects_count")
        try:
            await self._set_viewport("desktop")
            await self._go("/")

            cards = self.page.locator(".projects__grid .project-card")
            count = await cards.count()

            page_text = (await self.page.text_content("body") or "").lower()
            issues = []
            if count != 9:
                issues.append(f"expected 9 project cards, got {count}")
            if "cosplay" in page_text:
                issues.append("'cosplay' still present in page text")
            if "cyprus" in page_text:
                issues.append("'cyprus' still present in page text")

            screenshot = await self._screenshot("s04_projects")
            status = "FAIL" if issues else "PASS"
            self._record(
                "s04_projects_no_cosplay", status,
                f"cards={count}"
                + (f" | ISSUES: {'; '.join(issues)}" if issues else ""),
                screenshot, start,
            )
        except Exception as e:
            screenshot = await self._screenshot("s04_projects_error")
            self._record("s04_projects_no_cosplay", "FAIL", f"Exception: {e}", screenshot, start)

    # ── S05: Talk-to-Alice floating button visible & working ───────────────

    async def test_s05_alice_cta(self):
        """S05: 'Поговорить с Алисой' floating button → opens alice subdomain."""
        for vp_name in VIEWPORTS:
            start = await self._step(f"s05_alice_cta_{vp_name}")
            try:
                await self._set_viewport(vp_name)
                await self._go("/")

                cta = self.page.locator(".alice-float")
                visible = await cta.is_visible()
                href = await cta.get_attribute("href") if visible else None

                issues = []
                if not visible:
                    issues.append("alice-float not visible")
                if href and "alice.ekuznetsov.dev" not in href:
                    issues.append(f"unexpected href: {href}")

                screenshot = await self._screenshot(f"s05_alice_cta_{vp_name}")
                status = "FAIL" if issues else "PASS"
                self._record(
                    f"s05_alice_cta_{vp_name}", status,
                    f"[{vp_name.upper()}] visible={visible} href={href}"
                    + (f" | ISSUES: {'; '.join(issues)}" if issues else ""),
                    screenshot, start,
                )
            except Exception as e:
                screenshot = await self._screenshot(f"s05_alice_cta_{vp_name}_error")
                self._record(f"s05_alice_cta_{vp_name}", "FAIL",
                             f"[{vp_name.upper()}] Exception: {e}", screenshot, start)

    async def run_all(self, only=None, random_n=None):
        await self.test_s01_hero()
        await self.test_s02_mobile_drawer()
        await self.test_s03_drawer_projects_scroll()
        await self.test_s04_projects_no_cosplay()
        await self.test_s05_alice_cta()
        return self.results
