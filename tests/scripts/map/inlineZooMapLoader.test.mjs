import assert from 'node:assert/strict';
import test from 'node:test';

import { InlineZooMapLoader } from '../../../scripts/map/inlineZooMapLoader.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetZooMapMount_TestMissing_ExpectNull', () => {
   const mount = InlineZooMapLoader.getZooMapMount();

   assert.equal(mount, null);
});


test('Test_GetZooMapMountAndMountedSvg_TestDom_ExpectNodes', () => {
   const mount = document.createElement('div');
   mount.id = 'zooMapMount';
   const svg = document.createElement('svg');
   mount.querySelector = (selector) => (selector === 'svg' ? svg : null);
   const originalGet = document.getElementById;
   document.getElementById = (id) => (id === mount.id ? mount : null);

   try {
      const foundMount = InlineZooMapLoader.getZooMapMount();
      const foundSvg = InlineZooMapLoader.getMountedSvg(mount);

      assert.equal(foundMount, mount);
      assert.equal(foundSvg, svg);
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
   const svgText = '<svg></svg>';
   let calls = 0;
   globalThis.fetch = async (url) => {
      calls += 1;
      assert.equal(url, InlineZooMapLoader.ZOO_MAP_SVG_URL);
      return {
         ok: true,
         text: async () => svgText,
      };
   };
   InlineZooMapLoader.cachedSvgTextPromise = null;

   try {
      const first = await InlineZooMapLoader.fetchZooMapSvgText();
      const second = await InlineZooMapLoader.fetchZooMapSvgText();

      assert.equal(first, svgText);
      assert.equal(second, svgText);
      assert.equal(calls, Position.SECOND);
   } finally {
      globalThis.fetch = originalFetch;
      InlineZooMapLoader.cachedSvgTextPromise = originalCache;
   }
});


test('Test_MountInlineSvg_TestMount_ExpectInnerHtmlAndSvg', async () => {
   const originalFetch = InlineZooMapLoader.fetchZooMapSvgText;
   const svgMarkup = '<svg id="map"></svg>';
   const mapId = 'map';
   InlineZooMapLoader.fetchZooMapSvgText = async () => svgMarkup;
   const mount = document.createElement('div');
   mount.querySelector = (selector) => (
      selector === 'svg' ? { id: mapId } : null
   );

   try {
      const svg = await InlineZooMapLoader.mountInlineSvg(mount);

      assert.equal(mount.innerHTML, svgMarkup);
      assert.equal(svg.id, mapId);
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
