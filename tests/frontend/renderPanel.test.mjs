import assert from 'node:assert/strict';
import test from 'node:test';

import { renderItineraryPanelInto, clearStoredItinerary } from '../../scripts/itinerary/panel/renderPanel.js';
import { resetActiveItineraryPanelView } from '../../scripts/itinerary/panel/itineraryPanelViewState.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

const ZOO_HOURS = {
   open: '09:00',
   close: '19:00',
};

const POPULATED_ITINERARY = {
   date: '2026-06-15',
   animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
   attractions: [],
   guardiansTalks: [],
   wildEncounters: [],
   itineraryConfig: {
      eventTypes: ['lunch', 'break', 'arrival', 'departure'],
      visitBoundaryEventTypes: {
         arrival: 'arrival',
         departure: 'departure',
      },
   },
};

test.describe('renderItineraryPanelInto', () => {
   test.beforeEach(() => {
      installTestWindow();
      installDocument();
      resetActiveItineraryPanelView('list');
   });

   test.afterEach(() => {
      teardownDocument();
      delete globalThis.window;
   });

   test('renders build-only content for an empty itinerary', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');

      await renderItineraryPanelInto(bodyEl, {
         loadItinerary: async () => ({
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
         }),
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
      });

      assert.equal(bodyEl.children.length, 1);
      assert.ok(bodyEl.querySelector('.itin-panel-view-toggle'));
      assert.ok(bodyEl.querySelector('.itin-panel-build-btn'));
      assert.ok(bodyEl.querySelector('.itinerary-day-planner-content'));
   });

   test('renders itinerary sections and the day planner for populated itineraries', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');

      await renderItineraryPanelInto(bodyEl, {
         loadItinerary: async () => POPULATED_ITINERARY,
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
      });

      assert.ok(bodyEl.querySelector('.itin-panel-actions-wrap'));
      assert.ok(bodyEl.querySelector('.itin-panel-date'));
      assert.ok(bodyEl.querySelector('.itin-panel-section'));
      assert.ok(bodyEl.querySelector('.itinerary-day-planner-content'));
      assert.equal(bodyEl.querySelectorAll('.itin-panel-build-btn').length, 0);
   });

   test('ignores stale renders when a newer render starts first', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      let resolveFirst = null;
      let buildCount = 0;

      const buildMarkerContent = () => {
         buildCount += 1;
         const fragment = document.createDocumentFragment();
         fragment.appendChild(createDomNode('div', 'render-marker'));
         return fragment;
      };

      const firstRender = renderItineraryPanelInto(bodyEl, {
         loadItinerary: () => new Promise((resolve) => {
            resolveFirst = resolve;
         }),
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
         buildContent: buildMarkerContent,
         buildEmptyContent: () => {
            buildCount += 1;
         },
      });

      await renderItineraryPanelInto(bodyEl, {
         loadItinerary: async () => POPULATED_ITINERARY,
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
         buildContent: buildMarkerContent,
         buildEmptyContent: () => {
            buildCount += 1;
         },
      });

      resolveFirst?.(POPULATED_ITINERARY);
      await firstRender;

      assert.equal(buildCount, 1);
      assert.equal(bodyEl.querySelectorAll('.render-marker').length, 1);
   });
});

test.describe('clearStoredItinerary', () => {
   test('clears the saved itinerary and draft storage', async () => {
      let cleared = false;
      let draftCleared = false;

      await clearStoredItinerary({
         clearSavedItinerary: async () => {
            cleared = true;
         },
         clearDraftStorage: () => {
            draftCleared = true;
         },
      });

      assert.equal(cleared, true);
      assert.equal(draftCleared, true);
   });

   test('logs and swallows errors when clearing the itinerary fails', async () => {
      const errors = [];
      const originalConsoleError = console.error;

      console.error = (...args) => {
         errors.push(args);
      };

      try {
         await clearStoredItinerary({
            clearSavedItinerary: async () => {
               throw new Error('clear failed');
            },
            clearDraftStorage: () => {
               throw new Error('should not run');
            },
         });
      }
      finally {
         console.error = originalConsoleError;
      }

      assert.equal(errors.length, 1);
      assert.match(String(errors[0][0]), /Failed to clear itinerary/);
   });
});
