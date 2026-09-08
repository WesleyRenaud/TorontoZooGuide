import assert from 'node:assert/strict';
import test from 'node:test';

import { WheelBlocker } from '../../../../scripts/itinerary/wizard/wheelBlocker.js';
import { WheelBlockerHelper } from '../../../../scripts/itinerary/wizard/wheelBlockerHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BlockMapWheelWhileWizardOpen_TestMissingMount_ExpectNoOp', () => {
   WheelBlocker.blockMapWheelWhileWizardOpen(null);
});

test('Test_BlockMapWheelWhileWizardOpen_TestOverlayWheel_ExpectStopped', () => {
   const mountEl = document.createElement('div');
   const overlay = document.createElement('div');
   overlay.className = 'itin-overlay';
   const target = document.createElement('div');
   overlay.appendChild(target);
   mountEl.appendChild(overlay);

   const originalFind = WheelBlockerHelper.findScrollableAncestor;
   WheelBlockerHelper.findScrollableAncestor = () => null;

   try {
      WheelBlocker.blockMapWheelWhileWizardOpen(mountEl);
      const prevented = [];
      const stopped = [];
      mountEl.listeners.wheel({
         target,
         preventDefault: () => { prevented.push(true); },
         stopPropagation: () => { stopped.push(true); },
      });
      assert.deepEqual(prevented, [true]);
      assert.deepEqual(stopped, [true]);

      WheelBlockerHelper.findScrollableAncestor = () => target;
      const prevented2 = [];
      const stopped2 = [];
      mountEl.listeners.wheel({
         target,
         preventDefault: () => { prevented2.push(true); },
         stopPropagation: () => { stopped2.push(true); },
      });
      assert.deepEqual(prevented2, []);
      assert.deepEqual(stopped2, [true]);
   } finally {
      WheelBlockerHelper.findScrollableAncestor = originalFind;
   }
});
