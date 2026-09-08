import assert from 'node:assert/strict';
import test from 'node:test';

import { DateView } from '../../../../../scripts/itinerary/panel/components/dateView.js';
import { DraftStore } from '../../../../../scripts/itinerary/draftStore.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeDateCard_TestMissingPrettyDate_ExpectNull', () => {
   const originalFormat = ItineraryItemFormatter.formatISODateLong;
   ItineraryItemFormatter.formatISODateLong = () => '';
   try {
      assert.equal(DateView.makeDateCard({ date: '2026-06-01' }), null);
   } finally {
      ItineraryItemFormatter.formatISODateLong = originalFormat;
   }
});

test('Test_MakeDateCard_TestUsesItineraryDate_ExpectCardAndEditEvent', () => {
   const originalFormat = ItineraryItemFormatter.formatISODateLong;
   const originalGet = DraftStore.getStoredItineraryDate;
   const originalEl = ItineraryPanelHelper.el;
   const originalCustomEvent = globalThis.CustomEvent;
   const dispatched = [];

   ItineraryItemFormatter.formatISODateLong = (date) => `pretty:${date}`;
   DraftStore.getStoredItineraryDate = () => 'should-not-use';
   ItineraryPanelHelper.el = (tag, className, text) => {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text != null) el.textContent = text;
      return el;
   };
   globalThis.CustomEvent = class CustomEvent {
      constructor(type, init = {}) {
         this.type = type;
         this.detail = init.detail;
      }
   };
   window.dispatchEvent = (event) => {
      dispatched.push(event);
      return true;
   };

   try {
      const card = DateView.makeDateCard({ date: '2026-06-15' });
      assert.equal(card.className, 'itin-panel-date');
      assert.ok(card.textContent.includes(Strings.itinerary.selectors.visitDate));
      assert.ok(card.textContent.includes('pretty:2026-06-15'));

      const editBtn = card.children[0].children[1].children[0];
      editBtn.listeners.click({ preventDefault() {}, stopPropagation() {} });
      assert.equal(dispatched.length, 1);
      assert.equal(dispatched[0].type, 'tzg:editItinerarySection');
      assert.deepEqual(dispatched[0].detail, { step: 'date' });
   } finally {
      ItineraryItemFormatter.formatISODateLong = originalFormat;
      DraftStore.getStoredItineraryDate = originalGet;
      ItineraryPanelHelper.el = originalEl;
      globalThis.CustomEvent = originalCustomEvent;
   }
});

test('Test_MakeDateCard_TestFallsBackToStoredDate_ExpectPrettyStored', () => {
   const originalFormat = ItineraryItemFormatter.formatISODateLong;
   const originalGet = DraftStore.getStoredItineraryDate;
   const originalEl = ItineraryPanelHelper.el;
   ItineraryItemFormatter.formatISODateLong = (date) => `pretty:${date}`;
   DraftStore.getStoredItineraryDate = () => '2026-09-01';
   ItineraryPanelHelper.el = (tag, className, text) => {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text != null) el.textContent = text;
      return el;
   };

   try {
      const card = DateView.makeDateCard({});
      assert.ok(card.textContent.includes('pretty:2026-09-01'));
   } finally {
      ItineraryItemFormatter.formatISODateLong = originalFormat;
      DraftStore.getStoredItineraryDate = originalGet;
      ItineraryPanelHelper.el = originalEl;
   }
});
