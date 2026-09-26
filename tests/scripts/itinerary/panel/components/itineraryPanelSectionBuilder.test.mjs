import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelSectionBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilder.js';
import { ItineraryPanelSectionBuilderHelper } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilderHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
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
   const title = 'Animals';
   const count = 2;
   const stepKey = 'animals';
   const observed = [];
   const resizeCallbacks = [];

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = (...args) => {
      heights.push(args);
   };
   const originalDispatch = globalThis.window.dispatchEvent;
   globalThis.window.dispatchEvent = (event) => { events.push(event); };
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
         title,
         count,
         children: [child],
         stepKey,
         showEditButton: true,
      });
      image.listeners?.load?.();
      image.listeners?.error?.();
      resizeCallbacks.at(Position.FIRST)?.();
      const editBtn = section.querySelector('.itin-panel-section-edit-btn');
      editBtn.listeners.click({
         preventDefault() {},
         stopPropagation() {},
      });
      section.querySelector('.itin-panel-section-header').listeners.click();
      section.querySelector('.itin-panel-toggle').listeners.click({ stopPropagation() {} });
      section.__tzgCleanup();

      assert.equal(section.className, 'itin-panel-section');
      assert.match(section.textContent, new RegExp(title));
      assert.match(section.textContent, new RegExp(`\\(${count}\\)`));
      assert.equal(observed.length, 1);
      assert.equal(events.at(Position.FIRST).type, 'tzg:editItinerarySection');
      assert.deepEqual(events.at(Position.FIRST).detail, { step: stepKey });
      assert.equal(section.__tzgCleanup, undefined);
      assert.ok(heights.length >= 1);
      assert.equal(editBtn.getAttribute('aria-label'), Strings.itinerary.panel.editSectionAria(title));
   } finally {
      ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = originalUpdate;
      globalThis.window.dispatchEvent = originalDispatch;
   }
});


test('Test_MakeSection_TestHideEditButton_ExpectNoEdit', () => {
   const originalUpdate = ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight;
   const title = 'Date';

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = () => {};

   try {
      const section = ItineraryPanelSectionBuilder.makeSection({
         title,
         count: 0,
         showEditButton: false,
      });

      assert.equal(section.querySelector('.itin-panel-section-edit-btn'), null);
      section.__tzgCleanup?.();
   } finally {
      ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight = originalUpdate;
   }
});
