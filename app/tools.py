'''Functions that can be called by OpenAI tools.
'''

import json
import serpapi # type: ignore
from playwright.async_api import async_playwright

from app.settings import settings

async def download_webpage(url: str) -> str:
    '''Download a webpage and return the HTML.
    '''
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f'wss://chrome.browserless.io?token={settings.browserless_token}')
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        await browser.close()

    return html


def get_search_results(keywords):
    results = serpapi.search(
        q=keywords,
        engine="google",
        hl="en",
        gl="us",
        api_key=settings.serpapi_api_key
    )
    # Must convert to String for compatibility with OpenAI API
    return json.dumps(results['organic_results'])


if __name__ == '__main__':
    # Tests
    # html = download_webpage('https://quasar.dev/vue-components/select/')
    # print(html)
    import asyncio

    async def main():
        html = await download_webpage('https://quasar.dev/vue-components/select/')
        print(html)

    asyncio.run(main())