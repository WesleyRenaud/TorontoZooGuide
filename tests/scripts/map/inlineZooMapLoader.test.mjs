import assert from 'node:assert/strict';
import test from 'node:test';

import { InlineZooMapLoader } from '../../../scripts/map/inlineZooMapLoader.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetZooMapMountAndMountedSvg_TestDom_ExpectNodesOrNull', () => {
   assert.equal(InlineZooMapLoader.getZooMapMount(), null);

   const mount = document.createElement('div');
   mount.id = 'zooMapMount';
   const svg = document.createElement('svg');
   mount.querySelector = (selector) => (selector === 'svg' ? svg : null);

   const originalGet = document.getElementById;
   document.getElementById = (id) => (id === 'zooMapMount' ? mount : null);

   try {
      assert.equal(InlineZooMapLoader.getZooMapMount(), mount);
      assert.equal(InlineZooMapLoader.getMountedSvg(mount), svg);
   } finally {
      document.getElementById = originalGet;
   }
});

test('Test_ConfigureInlineSvg_TestAttributes_ExpectSized', () => {
   const svg = document.createElement('svg');
   const configured = InlineZooMapLoader.configureInlineSvg(svg);
   assert.equal(configured.getAttribute('width'), '100%');
   assert.equal(configured.getAttribute('height'), '100%');
   assert.equal(configured.getAttribute('preserveAspectRatio'), 'xMidYMid slice');
});

test('Test_FetchZooMapSvgText_TestFetch_ExpectCachedText', async () => {
   const originalFetch = globalThis.fetch;
   const originalCache = InlineZooMapLoader.cachedSvgTextPromise;
   let calls = 0;
   globalThis.fetch = async (url) => {
      calls += 1;
      assert.equal(url, InlineZooMapLoader.ZOO_MAP_SVG_URL);
      return {
         ok: true,
         text: async () => '<svg></svg>',
      };
   };
   InlineZooMapLoader.cachedSvgTextPromise = null;

   try {
      assert.equal(await InlineZooMapLoader.fetchZooMapSvgText(), '<svg></svg>');
      assert.equal(await InlineZooMapLoader.fetchZooMapSvgText(), '<svg></svg>');
      assert.equal(calls, 1);
   } finally {
      globalThis.fetch = originalFetch;
      InlineZooMapLoader.cachedSvgTextPromise = originalCache;
   }
});

test('Test_MountInlineSvg_TestMount_ExpectInnerHtmlAndSvg', async () => {
   const originalFetch = InlineZooMapLoader.fetchZooMapSvgText;
   InlineZooMapLoader.fetchZooMapSvgText = async () => '<svg id="map"></svg>';
   const mount = document.createElement('div');
   mount.querySelector = (selector) => (
      selector === 'svg' ? { id: 'map' } : null
   );

   try {
      const svg = await InlineZooMapLoader.mountInlineSvg(mount);
      assert.equal(mount.innerHTML, '<svg id="map"></svg>');
      assert.equal(svg.id, 'map');
   } finally {
      InlineZooMapLoader.fetchZooMapSvgText = originalFetch;
   }
});

test('Test_FetchZooMapSvgText_TestFailedResponse_ExpectClearsCacheAndThrows', async () => {
   const originalFetch = globalThis.fetch;
   const originalCache = InlineZooMapLoader.cachedSvgTextPromise;
   InlineZooMapLoader.cachedSvgTextPromise = null;
   globalThis.fetch = async () => ({
      ok: false,
      status: 500,
      text: async () => '',
   });

   try {
      await assert.rejects(() => InlineZooMapLoader.fetchZooMapSvgText());
      assert.equal(InlineZooMapLoader.cachedSvgTextPromise, null);
   } finally {
      globalThis.fetch = originalFetch;
      InlineZooMapLoader.cachedSvgTextPromise = originalCache;
   }
});
