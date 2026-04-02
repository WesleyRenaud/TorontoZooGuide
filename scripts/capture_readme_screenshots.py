from __future__ import annotations

import base64
import json
import shutil
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

import requests
import websocket

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'screenshots'
OUT.mkdir(parents=True, exist_ok=True)
BASE = 'http://localhost:8000'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DEBUG_PORT = 9222
USER_DATA_DIR = ROOT / '.tmp-chrome-readme'


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=20)
        self._id = 0

    def send(self, method: str, params: dict | None = None):
        self._id += 1
        msg = {'id': self._id, 'method': method, 'params': params or {}}
        self.ws.send(json.dumps(msg))
        while True:
            raw = self.ws.recv()
            data = json.loads(raw)
            if data.get('id') == self._id:
                if 'error' in data:
                    raise RuntimeError(data['error'])
                return data.get('result', {})

    def close(self):
        self.ws.close()


def wait_for_debug_endpoint(timeout=10):
    url = f'http://127.0.0.1:{DEBUG_PORT}/json/version'
    start = time.time()
    while time.time() - start < timeout:
        try:
            return requests.get(url, timeout=1).json()
        except Exception:
            time.sleep(0.2)
    raise RuntimeError('Chrome remote debugging endpoint did not come up')


def new_tab(url: str):
    endpoint = f'http://127.0.0.1:{DEBUG_PORT}/json/new?{quote(url, safe=":/?=&")}'
    res = requests.put(endpoint, timeout=5)
    res.raise_for_status()
    return res.json()['webSocketDebuggerUrl']


def js(cdp: CDP, expression: str):
    return cdp.send('Runtime.evaluate', {
        'expression': expression,
        'awaitPromise': True,
        'returnByValue': True,
    })


def wait(seconds=1.0):
    time.sleep(seconds)


def screenshot(cdp: CDP, name: str):
    data = cdp.send('Page.captureScreenshot', {'format': 'png', 'fromSurface': True})['data']
    path = OUT / name
    path.write_bytes(base64.b64decode(data))
    print(path)


def wait_for_selector(cdp: CDP, selector: str, timeout=15):
    deadline = time.time() + timeout
    expr = f"Boolean(document.querySelector({selector!r}))"
    while time.time() < deadline:
        try:
            result = js(cdp, expr)
            if result.get('result', {}).get('value'):
                return
        except Exception:
            pass
        time.sleep(0.2)
    raise RuntimeError(f'Selector not found: {selector}')


def click(cdp: CDP, selector: str):
    expr = f"""
(() => {{
  const el = document.querySelector({selector!r});
  if (!el) return false;
  el.click();
  return true;
}})()
"""
    result = js(cdp, expr)
    if not result.get('result', {}).get('value'):
        raise RuntimeError(f'Could not click selector: {selector}')


def click_button_by_text(cdp: CDP, text: str):
    expr = f"""
(() => {{
  const buttons = Array.from(document.querySelectorAll('button'));
  const target = buttons.find((btn) => btn.textContent.trim().includes({text!r}));
  if (!target) return false;
  target.click();
  return true;
}})()
"""
    result = js(cdp, expr)
    if not result.get('result', {}).get('value'):
        raise RuntimeError(f'Could not click button with text: {text}')


def set_itinerary(cdp: CDP):
    expr = """
(() => fetch('/set-itinerary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    date: '2026-06-20',
    animals: [
      { id: 'Black Tree Monitor||Australasia Pavilion', species: 'Black Tree Monitor', exhibit: 'Australasia Pavilion', imageSrc: '../images/animals/australasia-pavilion/black-tree-monitor.png' },
      { id: 'Komodo Dragon||Australasia Pavilion', species: 'Komodo Dragon', exhibit: 'Australasia Pavilion', imageSrc: '../images/animals/australasia-pavilion/komodo-dragon.png' }
    ],
    attractions: [
      { id: 'Zoomobile', name: 'Zoomobile', subtitle: 'Extra Charge', freeWithAdmission: false, seasonal: false, infoLink: 'https://www.torontozoo.com/tickets/zoomobile', imageSrc: '../images/attractions/zoomobile.png' }
    ],
    guardiansTalks: [
      { id: 'Komodo Dragon', name: 'Komodo Dragon', location: 'Australasia Pavilion', timeOfDay: '1:30 PM', imageSrc: '../images/guardians-talks/komodo-dragon.png' }
    ],
    wildEncounters: [
      { id: 'Kangaroo', name: 'Kangaroo', meetingSpot: 'Wild Encounter - Eurasia Meeting Spot', timeOfDay: '11:00 AM', link: 'https://www.torontozoo.com/tickets/wekangaroo', imageSrc: '../images/wild-encounters/kangaroo.png' }
    ],
    isActive: true
  })
}).then(r => r.json()).then(() => true))()
"""
    js(cdp, expr)


def main():
    if USER_DATA_DIR.exists():
        shutil.rmtree(USER_DATA_DIR)
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

    chrome = subprocess.Popen([
        CHROME,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--remote-debugging-port={DEBUG_PORT}',
        '--remote-allow-origins=*',
        f'--user-data-dir={USER_DATA_DIR}',
        '--window-size=1440,1100',
        'about:blank',
    ])

    cdp = None
    try:
        wait_for_debug_endpoint()
        ws_url = new_tab('about:blank')
        cdp = CDP(ws_url)
        cdp.send('Page.enable')
        cdp.send('Runtime.enable')

        # Map page
        cdp.send('Page.navigate', {'url': f'{BASE}/map.html'})
        wait_for_selector(cdp, '#zooMapMount')
        wait_for_selector(cdp, '.marker')
        wait(1.5)
        screenshot(cdp, 'map-page.png')

        # Animals region list
        cdp.send('Page.navigate', {'url': f'{BASE}/animals.html'})
        wait_for_selector(cdp, '.list-button')
        wait(1.0)
        screenshot(cdp, 'animals-regions.png')

        # Animals detail
        click_button_by_text(cdp, 'Australasia')
        wait_for_selector(cdp, '.back-button')
        wait(0.8)
        click_button_by_text(cdp, 'Australasia Pavilion')
        wait_for_selector(cdp, '.back-button')
        wait(0.8)
        click_button_by_text(cdp, 'Black Tree Monitor')
        wait_for_selector(cdp, '.animal-species-name')
        js(cdp, 'window.scrollTo(0, 0); true;')
        wait(1.2)
        screenshot(cdp, 'animals-detail.png')

        # Itinerary builder
        cdp.send('Page.navigate', {'url': f'{BASE}/itinerary.html'})
        wait_for_selector(cdp, '.itin-overlay .itin-card')
        wait(1.2)
        screenshot(cdp, 'itinerary-builder.png')

        # Itinerary saved state
        set_itinerary(cdp)
        cdp.send('Page.navigate', {'url': f'{BASE}/itinerary.html'})
        wait_for_selector(cdp, '.itin-panel-actions-wrap')
        wait_for_selector(cdp, '.itin-panel-date')
        wait(1.8)
        screenshot(cdp, 'itinerary-saved.png')
    finally:
        if cdp is not None:
            cdp.close()
        chrome.terminate()
        try:
            chrome.wait(timeout=5)
        except Exception:
            chrome.kill()
        if USER_DATA_DIR.exists():
            shutil.rmtree(USER_DATA_DIR)


if __name__ == '__main__':
    main()
