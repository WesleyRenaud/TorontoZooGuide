import assert from 'node:assert/strict';
import test from 'node:test';

import { InlineZooMapLoader } from '../../../scripts/map/inlineZooMapLoader.js';
import { LoadInlineZooMapLoader } from '../../../scripts/map/loadInlineZooMapLoader.js';


test('Test_LoadInlineZooMap_TestMissingMount_ExpectNull', async () => {
   const original = InlineZooMapLoader.getZooMapMount;
   InlineZooMapLoader.getZooMapMount = () => null;

   try {
      const loaded = await LoadInlineZooMapLoader.loadInlineZooMap();

      assert.equal(loaded, null);
   } finally {
      InlineZooMapLoader.getZooMapMount = original;
   }
});


test('Test_LoadInlineZooMap_TestExistingSvg_ExpectConfigured', async () => {
   const originalMount = InlineZooMapLoader.getZooMapMount;
   const originalExisting = InlineZooMapLoader.getMountedSvg;
   const originalConfigure = InlineZooMapLoader.configureInlineSvg;
   const svgId = 'svg';
   InlineZooMapLoader.getZooMapMount = () => ({ id: 'mount' });
   InlineZooMapLoader.getMountedSvg = () => ({ id: svgId });
   InlineZooMapLoader.configureInlineSvg = (svg) => ({ configured: svg.id });

   try {
      const loaded = await LoadInlineZooMapLoader.loadInlineZooMap();

      assert.deepEqual(loaded, { configured: svgId });
   } finally {
      InlineZooMapLoader.getZooMapMount = originalMount;
      InlineZooMapLoader.getMountedSvg = originalExisting;
      InlineZooMapLoader.configureInlineSvg = originalConfigure;
   }
});


test('Test_LoadInlineZooMap_TestMountFails_ExpectNull', async () => {
   const originalMount = InlineZooMapLoader.getZooMapMount;
   const originalExisting = InlineZooMapLoader.getMountedSvg;
   const originalInline = InlineZooMapLoader.mountInlineSvg;
   InlineZooMapLoader.getZooMapMount = () => ({ id: 'mount' });
   InlineZooMapLoader.getMountedSvg = () => null;
   InlineZooMapLoader.mountInlineSvg = async () => null;

   try {
      const loaded = await LoadInlineZooMapLoader.loadInlineZooMap();

      assert.equal(loaded, null);
   } finally {
      InlineZooMapLoader.getZooMapMount = originalMount;
      InlineZooMapLoader.getMountedSvg = originalExisting;
      InlineZooMapLoader.mountInlineSvg = originalInline;
   }
});


test('Test_LoadInlineZooMap_TestMountNewSvg_ExpectConfigured', async () => {
   const originalMount = InlineZooMapLoader.getZooMapMount;
   const originalExisting = InlineZooMapLoader.getMountedSvg;
   const originalInline = InlineZooMapLoader.mountInlineSvg;
   const originalConfigure = InlineZooMapLoader.configureInlineSvg;
   const svgId = 'new-svg';
   InlineZooMapLoader.getZooMapMount = () => ({ id: 'mount' });
   InlineZooMapLoader.getMountedSvg = () => null;
   InlineZooMapLoader.mountInlineSvg = async () => ({ id: svgId });
   InlineZooMapLoader.configureInlineSvg = (svg) => ({ configured: svg.id });

   try {
      const loaded = await LoadInlineZooMapLoader.loadInlineZooMap();

      assert.deepEqual(loaded, { configured: svgId });
   } finally {
      InlineZooMapLoader.getZooMapMount = originalMount;
      InlineZooMapLoader.getMountedSvg = originalExisting;
      InlineZooMapLoader.mountInlineSvg = originalInline;
      InlineZooMapLoader.configureInlineSvg = originalConfigure;
   }
});
