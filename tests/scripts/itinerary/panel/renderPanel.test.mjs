import assert from 'node:assert/strict';
import test from 'node:test';

import { RenderPanel } from '../../../../scripts/itinerary/panel/renderPanel.js';
import { ItineraryPanelViewState } from '../../../../scripts/itinerary/panel/itineraryPanelViewState.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

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

test.describe('RenderPanel.renderItineraryPanelInto', () => {
   installDomTestHooks({
      before: () => {
         ItineraryPanelViewState.resetActiveItineraryPanelView('list');
      },
   });

   test('Test_Renders_TestRendersBuildOnlyContentWhenNoItineraryIs_ExpectOk', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');

      await RenderPanel.renderItineraryPanelInto(bodyEl, {
         loadItinerary: async () => null,
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
      });

      assert.equal(bodyEl.children.length, 1);
      assert.ok(bodyEl.querySelector('.itin-panel-view-toggle'));
      assert.ok(bodyEl.querySelector('.itin-panel-build-btn'));
      assert.equal(bodyEl.querySelector('.itin-panel-date'), null);
   });

   test('Test_Renders_TestRendersDateOnlyItinerariesTheSameAsOther_ExpectOk', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');

      await RenderPanel.renderItineraryPanelInto(bodyEl, {
         loadItinerary: async () => ({
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: POPULATED_ITINERARY.itineraryConfig,
         }),
         resolveHoursDate: async () => '2026-06-15',
         loadZooHours: async () => ZOO_HOURS,
      });

      assert.ok(bodyEl.querySelector('.itin-panel-actions-wrap'));
      assert.ok(bodyEl.querySelector('.itin-panel-date'));
      assert.ok(bodyEl.querySelector('.itin-panel-section'));
      assert.ok(bodyEl.querySelector('.itinerary-day-planner-content'));
      assert.equal(bodyEl.querySelector('.itin-panel-empty-items-alert'), null);
      assert.equal(bodyEl.querySelectorAll('.itin-panel-build-btn').length, 0);
   });

   test('Test_Renders_TestRendersItinerarySectionsAndTheDayPlannerFor_ExpectOk', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');

      await RenderPanel.renderItineraryPanelInto(bodyEl, {
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

   test('Test_Ignores_TestIgnoresStaleRendersWhenANewerRenderStarts_ExpectOk', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      let resolveFirst = null;
      let buildCount = 0;

      const buildMarkerContent = () => {
         buildCount += 1;
         const fragment = document.createDocumentFragment();
         fragment.appendChild(createDomNode('div', 'render-marker'));
         return fragment;
      };

      const firstRender = RenderPanel.renderItineraryPanelInto(bodyEl, {
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

      await RenderPanel.renderItineraryPanelInto(bodyEl, {
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

   test('Test_RenderPanel_TestRenderPanelRenderItineraryPanelIntoReturnsEarlyWithoutABodyElement_ExpectOk', async () => {
      await RenderPanel.renderItineraryPanelInto(null, {
         loadItinerary: async () => {
            throw new Error('should not load');
         },
      });
   });
});

test.describe('RenderPanel.clearStoredItinerary', () => {
   test('Test_Clears_TestClearsTheSavedItineraryAndDraftStorage_ExpectOk', async () => {
      let cleared = false;
      let draftCleared = false;

      await RenderPanel.clearStoredItinerary({
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

   test('Test_Logs_TestLogsAndSwallowsErrorsWhenClearingTheItinerary_ExpectOk', async () => {
      const errors = [];
      const originalConsoleError = console.error;

      console.error = (...args) => {
         errors.push(args);
      };

      try {
         await RenderPanel.clearStoredItinerary({
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
