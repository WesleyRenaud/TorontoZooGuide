import assert from 'node:assert/strict';
import test from 'node:test';

import { LoadInlineZooMapLoader } from '../../../scripts/map/loadInlineZooMapLoader.js';
import { InlineZooMapLoader } from '../../../scripts/map/inlineZooMapLoader.js';

test('Test_LoadInlineZooMap_TestMissingMount_ExpectNull', async () => {
   const original = InlineZooMapLoader.getZooMapMount;
   InlineZooMapLoader.getZooMapMount = () => null;

   try {
      assert.equal(await LoadInlineZooMapLoader.loadInlineZooMap(), null);
   } finally {
      InlineZooMapLoader.getZooMapMount = original;
   }
});

test('Test_LoadInlineZooMap_TestExistingSvg_ExpectConfigured', async () => {
   const originalMount = InlineZooMapLoader.getZooMapMount;
   const originalExisting = InlineZooMapLoader.getMountedSvg;
   const originalConfigure = InlineZooMapLoader.configureInlineSvg;
   InlineZooMapLoader.getZooMapMount = () => ({ id: 'mount' });
   InlineZooMapLoader.getMountedSvg = () => ({ id: 'svg' });
   InlineZooMapLoader.configureInlineSvg = (svg) => ({ configured: svg.id });

   try {
      assert.deepEqual(await LoadInlineZooMapLoader.loadInlineZooMap(), { configured: 'svg' });
   } finally {
      InlineZooMapLoader.getZooMapMount = originalMount;
      InlineZooMapLoader.getMountedSvg = originalExisting;
      InlineZooMapLoader.configureInlineSvg = originalConfigure;
   }
});

test('Test_LoadInlineZooMap_TestMountNewSvg_ExpectConfiguredOrNull', async () => {
   const originalMount = InlineZooMapLoader.getZooMapMount;
   const originalExisting = InlineZooMapLoader.getMountedSvg;
   const originalInline = InlineZooMapLoader.mountInlineSvg;
   const originalConfigure = InlineZooMapLoader.configureInlineSvg;

   InlineZooMapLoader.getZooMapMount = () => ({ id: 'mount' });
   InlineZooMapLoader.getMountedSvg = () => null;
   InlineZooMapLoader.mountInlineSvg = async () => null;

   try {
      assert.equal(await LoadInlineZooMapLoader.loadInlineZooMap(), null);

      InlineZooMapLoader.mountInlineSvg = async () => ({ id: 'new-svg' });
      InlineZooMapLoader.configureInlineSvg = (svg) => ({ configured: svg.id });
      assert.deepEqual(await LoadInlineZooMapLoader.loadInlineZooMap(), { configured: 'new-svg' });
   } finally {
      InlineZooMapLoader.getZooMapMount = originalMount;
      InlineZooMapLoader.getMountedSvg = originalExisting;
      InlineZooMapLoader.mountInlineSvg = originalInline;
      InlineZooMapLoader.configureInlineSvg = originalConfigure;
   }
});
