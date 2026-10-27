import assert from 'node:assert/strict';
import test from 'node:test';

import { DateView } from '../../../../../scripts/itinerary/panel/components/dateView.js';
import { DraftStore } from '../../../../../scripts/itinerary/draftStore.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { VisitDateFormatter } from '../../../../../scripts/visitDates/visitDateFormatter.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _prettyDate(date) {
   return `pretty:${date}`;
}

installDomTestHooks();


test('Test_MakeDateCard_TestMissingPrettyDate_ExpectNull', () => {
   const originalFormat = VisitDateFormatter.formatLong;
   const date = '2026-06-01';

   VisitDateFormatter.formatLong = () => '';

   try {
      const card = DateView.makeDateCard({ date });

      assert.equal(card, null);
   } finally {
      VisitDateFormatter.formatLong = originalFormat;
   }
});


test('Test_MakeDateCard_TestItineraryDate_ExpectCardAndEditEvent', () => {
   const originalFormat = VisitDateFormatter.formatLong;
   const originalGet = DraftStore.getStoredItineraryDate;
   const originalEl = ItineraryPanelHelper.el;
   const originalCustomEvent = globalThis.CustomEvent;
   const date = '2026-06-15';
   const dispatched = [];

   VisitDateFormatter.formatLong = _prettyDate;
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
      const card = DateView.makeDateCard({ date });
      const editBtn = card.children.at(Position.FIRST)
         .children.at(Position.SECOND)
         .children.at(Position.FIRST);
      editBtn.listeners.click({ preventDefault() {}, stopPropagation() {} });
      const event = dispatched.at(Position.FIRST);

      assert.equal(card.className, 'itin-panel-date');
      assert.ok(card.textContent.includes(Strings.itinerary.selectors.visitDate));
      assert.ok(card.textContent.includes(_prettyDate(date)));
      assert.equal(dispatched.length, 1);
      assert.equal(event.type, 'tzg:editItinerarySection');
      assert.deepEqual(event.detail, { step: 'date' });
   } finally {
      VisitDateFormatter.formatLong = originalFormat;
      DraftStore.getStoredItineraryDate = originalGet;
      ItineraryPanelHelper.el = originalEl;
      globalThis.CustomEvent = originalCustomEvent;
   }
});


test('Test_MakeDateCard_TestStoredDate_ExpectPrettyStored', () => {
   const originalFormat = VisitDateFormatter.formatLong;
   const originalGet = DraftStore.getStoredItineraryDate;
   const originalEl = ItineraryPanelHelper.el;
   const storedDate = '2026-09-01';

   VisitDateFormatter.formatLong = _prettyDate;
   DraftStore.getStoredItineraryDate = () => storedDate;
   ItineraryPanelHelper.el = (tag, className, text) => {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text != null) el.textContent = text;
      return el;
   };

   try {
      const card = DateView.makeDateCard({});

      assert.ok(card.textContent.includes(_prettyDate(storedDate)));
   } finally {
      VisitDateFormatter.formatLong = originalFormat;
      DraftStore.getStoredItineraryDate = originalGet;
      ItineraryPanelHelper.el = originalEl;
   }
});
