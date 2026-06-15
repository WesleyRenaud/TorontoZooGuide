import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildEmptyItineraryPanelContent,
   buildItineraryPanelContent,
   clearRenderedPanel,
   destroyRenderedPanelChildren,
} from '../../scripts/itinerary/panel/itineraryPanelContent.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

const ZOO_HOURS = {
   open: '09:00',
   close: '19:00',
};

const ITINERARY_CONFIG = {
   eventTypes: ['lunch', 'break'],
   visitBoundaryEventTypes: {
      arrival: 'arrival',
      departure: 'departure',
   },
};

function makeViewShell() {
   const root = createDomNode('div', 'itin-panel-root');
   const sharedHeader = createDomNode('div', 'itin-panel-shared-header');
   const listView = createDomNode('div', 'itin-panel-list-view');
   const dayPlannerView = createDomNode('div', 'itin-panel-day-planner-view');

   root.appendChild(sharedHeader);
   root.appendChild(listView);
   root.appendChild(dayPlannerView);

   return {
      root,
      sharedHeader,
      listView,
      dayPlannerView,
   };
}

function captureDayPlannerOptions(deps = {}) {
   let plannerOptions = null;
   let timeHandlers = null;

   return {
      deps: {
         makeViewShell,
         renderEmptyState: () => {},
         makeActions: () => createDomNode('div', 'itin-panel-actions-wrap'),
         createDateCard: () => null,
         buildSections: () => [],
         createSection: () => createDomNode('section', 'itin-panel-section'),
         buildScheduleHandlers: () => ({
            onRemoveItineraryItem: () => {},
         }),
         makeDayPlanner: (_zooHours, _itinerary, handlers, options) => {
            timeHandlers = handlers;
            plannerOptions = options;
            return createDomNode('div', 'day-planner-stub');
         },
         ...deps,
      },
      getPlannerOptions: () => plannerOptions,
      getTimeHandlers: () => timeHandlers,
   };
}

test.describe('itineraryPanelContent', () => {
   test.beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   test.afterEach(() => {
      teardownDocument();
      delete globalThis.window;
   });

   test('destroyRenderedPanelChildren runs child cleanup hooks', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      const child = createDomNode('div', 'panel-child');
      let cleaned = false;

      child.__tzgCleanup = () => {
         cleaned = true;
      };
      bodyEl.appendChild(child);

      destroyRenderedPanelChildren(bodyEl);

      assert.equal(cleaned, true);
   });

   test('clearRenderedPanel removes rendered children', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      bodyEl.appendChild(createDomNode('div', 'panel-child'));

      clearRenderedPanel(bodyEl);

      assert.equal(bodyEl.children.length, 0);
   });

   test('buildEmptyItineraryPanelContent opens the schedule module from the planner', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      const opened = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         openModule: (options) => {
            opened.push(options);
         },
         buildEventTypes: () => ['lunch'],
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         deps,
      });

      getPlannerOptions()?.onScheduleItemClick?.();

      assert.equal(opened.length, 1);
      assert.deepEqual(opened[0].eventTypes, ['lunch']);
   });

   test('buildEmptyItineraryPanelContent shows a notice when bulk scheduling fails', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      const notices = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => {
            throw new Error('Bulk schedule failed');
         },
         showNotice: (message) => {
            notices.push(message);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, { deps });

      await getPlannerOptions()?.onBulkScheduleAnimalsClick?.();

      assert.deepEqual(notices, ['Bulk schedule failed']);
   });

   test('buildEmptyItineraryPanelContent refreshes and warns when bulk scheduling is tight on time', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      let warned = false;
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            issues: [{ code: 'notEnoughTime' }],
         }),
         hasNotEnoughTimeIssue: () => true,
         showNotEnoughTimeNotice: () => {
            warned = true;
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onBulkScheduleAnimalsClick?.();

      assert.equal(refreshed, true);
      assert.equal(warned, true);
   });

   test('buildItineraryPanelContent uses the generic error when bulk scheduling fails without a message', async () => {
      const notices = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => {
            throw new Error('');
         },
         showNotice: (message) => {
            notices.push(message);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         { deps }
      );

      await getPlannerOptions()?.onBulkScheduleAnimalsClick?.();

      assert.deepEqual(notices, [APP_STRINGS.itinerary.errors.generic]);
   });

   test('buildItineraryPanelContent refreshes after arrival and departure time changes', async () => {
      const arrivalCalls = [];
      const departureCalls = [];
      let refreshed = 0;
      const { deps, getTimeHandlers } = captureDayPlannerOptions({
         setArrivalTime: async (time) => {
            arrivalCalls.push(time);
         },
         setDepartureTime: async (time) => {
            departureCalls.push(time);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         {
            onPanelRefresh: async () => {
               refreshed += 1;
            },
            deps,
         }
      );

      await getTimeHandlers()?.onArrivalTimeChange?.('09:30');
      await getTimeHandlers()?.onDepartureTimeChange?.('17:00');

      assert.deepEqual(arrivalCalls, ['09:30']);
      assert.deepEqual(departureCalls, ['17:00']);
      assert.equal(refreshed, 2);
   });
});
