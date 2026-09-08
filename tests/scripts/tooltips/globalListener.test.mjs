import assert from 'node:assert/strict';
import test from 'node:test';

import { GlobalListener } from '../../../scripts/tooltips/globalListener.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTooltipGlobalListeners_TestInstallUninstallAndEvents_ExpectHandlers', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;
   const originalOpen = window.open;
   const closes = [];
   const steps = [];
   const animalClicks = [];
   const opens = [];

   document.addEventListener = (type, handler) => { listeners[type] = handler; };
   document.removeEventListener = (type) => { listeners[type] = null; };
   window.open = (...args) => { opens.push(args); };

   const tooltipEl = {
      contains: (target) => target?.inTooltip === true,
   };

   const api = GlobalListener.createTooltipGlobalListeners({
      tooltipEl,
      isOpen: () => true,
      close: () => { closes.push(true); },
      step: (delta) => { steps.push(delta); },
      getItemAtIndex: (index) => (index === 1 ? { species: 'Tiger' } : null),
      onAnimalCardClick: (item) => { animalClicks.push(item); },
   });

   try {
      api.install();
      api.install();
      assert.ok(listeners.click);
      assert.ok(listeners.keydown);

      listeners.click({
         target: {
            closest: (selector) => (selector === '.species-link'
               ? { dataset: { externalHref: 'https://example.test' } }
               : null),
         },
         stopPropagation() {},
      });
      assert.deepEqual(opens, [['https://example.test', '_blank']]);

      listeners.click({
         target: {
            closest: (selector) => (selector === '.species-link'
               ? { dataset: { index: '1', externalHref: '' } }
               : null),
         },
         stopPropagation() {},
      });
      assert.deepEqual(animalClicks, [{ species: 'Tiger' }]);

      listeners.click({
         target: {
            closest: () => null,
            inTooltip: false,
         },
      });
      assert.equal(closes.length, 1);

      listeners.keydown({ key: 'Escape', preventDefault() {} });
      listeners.keydown({ key: 'ArrowRight', preventDefault() {} });
      listeners.keydown({ key: 'ArrowLeft', preventDefault() {} });
      assert.ok(closes.length >= 2);
      assert.deepEqual(steps, [1, -1]);

      api.uninstall();
      api.uninstall();
      assert.equal(listeners.click, null);
      assert.equal(listeners.keydown, null);
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
      window.open = originalOpen;
   }
});
