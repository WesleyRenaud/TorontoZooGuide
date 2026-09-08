import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelSectionBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilder.js';
import { ItineraryPanelSectionBuilderHelper } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilderHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks({
   before: () => {
      globalThis.cancelAnimationFrame = () => {};
      globalThis.requestAnimationFrame = (callback) => {
         callback();
         return 1;
      };
      globalThis.CustomEvent = class CustomEvent {
         constructor(type, options = {}) {
            this.type = type;
            this.detail = options.detail;
         }
      };
   },
   after: () => {
      delete globalThis.cancelAnimationFrame;
      delete globalThis.requestAnimationFrame;
      delete globalThis.CustomEvent;
      delete globalThis.ResizeObserver;
   },
});

test('Test_MakeSection_TestHeaderToggleEditCleanup_ExpectSection', () => {
   const originalUpdate = ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight;
   const heights = [];
   const events = [];
   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = (...args) => {
      heights.push(args);
   };
   const originalDispatch = globalThis.window.dispatchEvent;
   globalThis.window.dispatchEvent = (event) => { events.push(event); };

   const observed = [];
   const resizeCallbacks = [];
   globalThis.ResizeObserver = class ResizeObserver {
      constructor(callback) {
         this.callback = callback;
         resizeCallbacks.push(callback);
      }

      observe(item) {
         observed.push(item);
         this.callback?.();
      }

      disconnect() {
         this.disconnected = true;
      }
   };

   try {
      const child = document.createElement('div');
      const image = document.createElement('img');
      child.appendChild(image);
      const section = ItineraryPanelSectionBuilder.makeSection({
         title: 'Animals',
         count: 2,
         children: [child],
         stepKey: 'animals',
         showEditButton: true,
      });

      assert.equal(section.className, 'itin-panel-section');
      assert.match(section.textContent, /Animals/);
      assert.match(section.textContent, /\(2\)/);
      assert.equal(observed.length, 1);

      image.listeners?.load?.();
      image.listeners?.error?.();
      resizeCallbacks[0]?.();

      const editBtn = section.querySelector('.itin-panel-section-edit-btn');
      editBtn.listeners.click({
         preventDefault() {},
         stopPropagation() {},
      });
      assert.equal(events[0].type, 'tzg:editItinerarySection');
      assert.deepEqual(events[0].detail, { step: 'animals' });

      // Exercise collapse listeners (dom mock toggle ignores force-less calls).
      section.querySelector('.itin-panel-section-header').listeners.click();
      section.querySelector('.itin-panel-toggle').listeners.click({ stopPropagation() {} });

      assert.equal(typeof section.__tzgCleanup, 'function');
      section.__tzgCleanup();
      assert.equal(section.__tzgCleanup, undefined);
      assert.ok(heights.length >= 1);
      assert.equal(editBtn.getAttribute('aria-label'), Strings.itinerary.panel.editSectionAria('Animals'));
   } finally {
      ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = originalUpdate;
      globalThis.window.dispatchEvent = originalDispatch;
   }
});

test('Test_MakeSection_TestHideEditButton_ExpectNoEdit', () => {
   const originalUpdate = ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight;
   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = () => {};

   try {
      const section = ItineraryPanelSectionBuilder.makeSection({
         title: 'Date',
         count: 0,
         showEditButton: false,
      });
      assert.equal(section.querySelector('.itin-panel-section-edit-btn'), null);
      section.__tzgCleanup?.();
   } finally {
      ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = originalUpdate;
   }
});
