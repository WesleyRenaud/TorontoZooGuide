import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelView } from '../../../../scripts/itinerary/panel/components/itineraryPanelView.js';
import { ItineraryPanelViewStore } from '../../../../scripts/itinerary/panel/itineraryPanelViewStore.js';
import { RenderView } from '../../../../scripts/itinerary/panel/renderView.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

const visitDate = '2026-06-15';
const zooHours = {
   open: '09:00',
   close: '19:00',
};
const populatedItinerary = {
   date: visitDate,
   animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia Wilds' }],
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

installDomTestHooks({
   before: () => {
      ItineraryPanelViewStore.resetActiveItineraryPanelView(ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
   },
});


test('Test_RenderItineraryPanelInto_TestNoItinerary_ExpectBuildOnlyContent', async () => {
   const bodyEl = createDomNode('div', 'side-panel-body');

   await RenderView.renderItineraryPanelInto(bodyEl, {
      loadItinerary: async () => null,
      resolveHoursDate: async () => visitDate,
      loadZooHours: async () => zooHours,
   });

   assert.equal(bodyEl.children.length, Position.SECOND);
   assert.ok(bodyEl.querySelector('.itin-panel-view-toggle'));
   assert.ok(bodyEl.querySelector('.itin-panel-build-btn'));
   assert.equal(bodyEl.querySelector('.itin-panel-date'), null);
});


test('Test_RenderItineraryPanelInto_TestDateOnlyItinerary_ExpectDayPlanner', async () => {
   const bodyEl = createDomNode('div', 'side-panel-body');
   const dateOnlyItinerary = {
      date: visitDate,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      itineraryConfig: populatedItinerary.itineraryConfig,
   };

   await RenderView.renderItineraryPanelInto(bodyEl, {
      loadItinerary: async () => dateOnlyItinerary,
      resolveHoursDate: async () => visitDate,
      loadZooHours: async () => zooHours,
   });

   assert.ok(bodyEl.querySelector('.itin-panel-actions-wrap'));
   assert.ok(bodyEl.querySelector('.itin-panel-date'));
   assert.ok(bodyEl.querySelector('.itin-panel-section'));
   assert.ok(bodyEl.querySelector('.itinerary-day-planner-content'));
   assert.equal(bodyEl.querySelector('.itin-panel-empty-items-alert'), null);
   assert.equal(bodyEl.querySelectorAll('.itin-panel-build-btn').length, 0);
});


test('Test_RenderItineraryPanelInto_TestPopulatedItinerary_ExpectSectionsAndDayPlanner', async () => {
   const bodyEl = createDomNode('div', 'side-panel-body');

   await RenderView.renderItineraryPanelInto(bodyEl, {
      loadItinerary: async () => populatedItinerary,
      resolveHoursDate: async () => visitDate,
      loadZooHours: async () => zooHours,
   });

   assert.ok(bodyEl.querySelector('.itin-panel-actions-wrap'));
   assert.ok(bodyEl.querySelector('.itin-panel-date'));
   assert.ok(bodyEl.querySelector('.itin-panel-section'));
   assert.ok(bodyEl.querySelector('.itinerary-day-planner-content'));
   assert.equal(bodyEl.querySelectorAll('.itin-panel-build-btn').length, 0);
});


test('Test_RenderItineraryPanelInto_TestStaleRender_ExpectNewerRenderKept', async () => {
   const bodyEl = createDomNode('div', 'side-panel-body');
   const markerClass = 'render-marker';
   let resolveFirst = null;
   let buildCount = 0;
   const buildMarkerContent = () => {
      buildCount += 1;
      const fragment = document.createDocumentFragment();
      fragment.appendChild(createDomNode('div', markerClass));
      return fragment;
   };

   const firstRender = RenderView.renderItineraryPanelInto(bodyEl, {
      loadItinerary: () => new Promise((resolve) => {
         resolveFirst = resolve;
      }),
      resolveHoursDate: async () => visitDate,
      loadZooHours: async () => zooHours,
      buildContent: buildMarkerContent,
      buildEmptyContent: () => {
         buildCount += 1;
      },
   });
   await RenderView.renderItineraryPanelInto(bodyEl, {
      loadItinerary: async () => populatedItinerary,
      resolveHoursDate: async () => visitDate,
      loadZooHours: async () => zooHours,
      buildContent: buildMarkerContent,
      buildEmptyContent: () => {
         buildCount += 1;
      },
   });
   resolveFirst?.(populatedItinerary);
   await firstRender;
   const markers = bodyEl.querySelectorAll(`.${markerClass}`);

   assert.equal(buildCount, Position.SECOND);
   assert.equal(markers.length, Position.SECOND);
});


test('Test_RenderItineraryPanelInto_TestMissingBody_ExpectNoLoad', async () => {
   let loaded = false;

   await RenderView.renderItineraryPanelInto(null, {
      loadItinerary: async () => {
         loaded = true;
         throw new Error('should not load');
      },
   });

   assert.equal(loaded, false);
});


test('Test_ClearStoredItinerary_TestSavedAndDraft_ExpectCleared', async () => {
   let cleared = false;
   let draftCleared = false;

   await RenderView.clearStoredItinerary({
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


test('Test_ClearStoredItinerary_TestClearFails_ExpectErrorSwallowed', async () => {
   const errors = [];
   const originalConsoleError = console.error;
   const failure = new Error('clear failed');
   console.error = (...args) => {
      errors.push(args);
   };

   try {
      await RenderView.clearStoredItinerary({
         clearSavedItinerary: async () => {
            throw failure;
         },
         clearDraftStorage: () => {
            throw new Error('should not run');
         },
      });

      const loggedError = errors.at(Position.FIRST);

      assert.equal(errors.length, Position.SECOND);
      assert.match(String(loggedError.at(Position.FIRST)), /Failed to clear itinerary/);
   } finally {
      console.error = originalConsoleError;
   }
});
