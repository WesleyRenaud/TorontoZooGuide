import assert from 'node:assert/strict';
import test from 'node:test';

import { GlobalListener } from '../../../scripts/tooltips/globalListener.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _createApi(overrides = {}) {
   return GlobalListener.createTooltipGlobalListeners({
      tooltipEl: {
         contains: (target) => target?.inTooltip === true,
      },
      isOpen: () => true,
      close: () => {},
      step: () => {},
      getItemAtIndex: () => null,
      onAnimalCardClick: () => {},
      ...overrides,
   });
}


test('Test_CreateTooltipGlobalListeners_TestInstall_ExpectHandlers', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };
   document.removeEventListener = (type) => {
      listeners[type] = null;
   };

   try {
      const api = _createApi();
      api.install();
      api.install();

      assert.ok(listeners.click);
      assert.ok(listeners.keydown);
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
   }
});


test('Test_CreateTooltipGlobalListeners_TestExternalLink_ExpectOpened', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const originalOpen = window.open;
   const opens = [];
   const href = 'https://example.test';
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };
   window.open = (...args) => {
      opens.push(args);
   };

   try {
      const api = _createApi();
      api.install();
      listeners.click({
         target: {
            closest: (selector) => (selector === '.species-link'
               ? { dataset: { externalHref: href } }
               : null),
         },
         stopPropagation() {},
      });

      assert.deepEqual(opens, [[href, '_blank']]);
   } finally {
      document.addEventListener = originalAdd;
      window.open = originalOpen;
   }
});


test('Test_CreateTooltipGlobalListeners_TestSpeciesLink_ExpectAnimalClick', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const animalClicks = [];
   const tiger = { species: 'Amur Tiger' };
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };

   try {
      const api = _createApi({
         getItemAtIndex: (index) => (index === Position.SECOND ? tiger : null),
         onAnimalCardClick: (item) => {
            animalClicks.push(item);
         },
      });
      api.install();
      listeners.click({
         target: {
            closest: (selector) => (selector === '.species-link'
               ? { dataset: { index: String(Position.SECOND), externalHref: '' } }
               : null),
         },
         stopPropagation() {},
      });

      assert.deepEqual(animalClicks, [tiger]);
   } finally {
      document.addEventListener = originalAdd;
   }
});


test('Test_CreateTooltipGlobalListeners_TestOutsideClick_ExpectClose', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const closes = [];
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };

   try {
      const api = _createApi({
         close: () => {
            closes.push(true);
         },
      });
      api.install();
      listeners.click({
         target: {
            closest: () => null,
            inTooltip: false,
         },
      });

      assert.equal(closes.length, Position.SECOND);
   } finally {
      document.addEventListener = originalAdd;
   }
});


test('Test_CreateTooltipGlobalListeners_TestKeys_ExpectCloseAndStep', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const closes = [];
   const steps = [];
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };

   try {
      const api = _createApi({
         close: () => {
            closes.push(true);
         },
         step: (delta) => {
            steps.push(delta);
         },
      });
      api.install();
      listeners.keydown({ key: 'Escape', preventDefault() {} });
      listeners.keydown({ key: 'ArrowRight', preventDefault() {} });
      listeners.keydown({ key: 'ArrowLeft', preventDefault() {} });

      assert.ok(closes.length >= 1);
      assert.deepEqual(steps, [Position.SECOND, Position.LAST]);
   } finally {
      document.addEventListener = originalAdd;
   }
});


test('Test_CreateTooltipGlobalListeners_TestUninstall_ExpectCleared', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };
   document.removeEventListener = (type) => {
      listeners[type] = null;
   };

   try {
      const api = _createApi();
      api.install();
      api.uninstall();
      api.uninstall();

      assert.equal(listeners.click, null);
      assert.equal(listeners.keydown, null);
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
   }
});


test('Test_CreateTooltipGlobalListeners_TestClosedState_ExpectNoClose', () => {
   const listeners = { click: null, keydown: null };
   const originalAdd = document.addEventListener;
   const closes = [];
   const steps = [];
   document.addEventListener = (type, handler) => {
      listeners[type] = handler;
   };

   try {
      const api = _createApi({
         tooltipEl: { contains: () => false },
         isOpen: () => false,
         close: () => {
            closes.push(true);
         },
         step: (delta) => {
            steps.push(delta);
         },
      });
      api.install();
      listeners.click({
         target: { closest: () => null },
      });
      listeners.keydown({ key: 'Escape', preventDefault() {} });
      listeners.keydown({ key: 'ArrowRight', preventDefault() {} });

      assert.deepEqual(closes, []);
      assert.deepEqual(steps, []);
   } finally {
      document.addEventListener = originalAdd;
   }
});
