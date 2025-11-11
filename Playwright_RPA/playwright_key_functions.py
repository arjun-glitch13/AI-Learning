from playwright.async_api import async_playwright
import asyncio


async def playwright_function():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        #Navigation
        await page.goto("https://www.google.com")
        print("browser opened")
        await page.wait_for_timeout(1000)
        await browser.close()
        print("execution completed")

if __name__ == "__main__":
    asyncio.run(playwright_function())