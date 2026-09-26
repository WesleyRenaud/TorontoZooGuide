import assert from 'node:assert/strict';
import test from 'node:test';

import { WheelBlocker } from '../../../../scripts/itinerary/wizard/wheelBlocker.js';
import { WheelBlockerHelper } from '../../../../scripts/itinerary/wizard/wheelBlockerHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BlockMapWheelWhileWizardOpen_TestMissingMount_ExpectNoOp', () => {
   const mountEl = null;

   assert.doesNotThrow(() => {
      WheelBlocker.blockMapWheelWhileWizardOpen(mountEl);
   });
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
   const prevented = [];
   const stopped = [];

   try {
      WheelBlocker.blockMapWheelWhileWizardOpen(mountEl);
      mountEl.listeners.wheel({
         target,
         preventDefault: () => { prevented.push(true); },
         stopPropagation: () => { stopped.push(true); },
      });

      assert.deepEqual(prevented, [true]);
      assert.deepEqual(stopped, [true]);
   } finally {
      WheelBlockerHelper.findScrollableAncestor = originalFind;
   }
});


test('Test_BlockMapWheelWhileWizardOpen_TestScrollableTarget_ExpectPropagationStopped', () => {
   const mountEl = document.createElement('div');
   const overlay = document.createElement('div');
   overlay.className = 'itin-overlay';
   const target = document.createElement('div');
   overlay.appendChild(target);
   mountEl.appendChild(overlay);
   const originalFind = WheelBlockerHelper.findScrollableAncestor;
   WheelBlockerHelper.findScrollableAncestor = () => target;
   const prevented = [];
   const stopped = [];

   try {
      WheelBlocker.blockMapWheelWhileWizardOpen(mountEl);
      mountEl.listeners.wheel({
         target,
         preventDefault: () => { prevented.push(true); },
         stopPropagation: () => { stopped.push(true); },
      });

      assert.deepEqual(prevented, []);
      assert.deepEqual(stopped, [true]);
   } finally {
      WheelBlockerHelper.findScrollableAncestor = originalFind;
   }
});
