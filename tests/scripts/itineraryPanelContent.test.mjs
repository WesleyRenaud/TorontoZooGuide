import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildEmptyItineraryPanelContent,
   buildItineraryPanelContent,
   clearRenderedPanel,
   destroyRenderedPanelChildren,
} from '../../scripts/itinerary/panel/itineraryPanelContent.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { ItineraryErrorTypes } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { MOCK_ERROR_TYPES } from './helpers/scheduleItemActionsTestSetup.mjs';

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
   installDomTestHooks();

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

   test('buildEmptyItineraryPanelContent shows error feedback when bulk scheduling fails', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => {
            throw new Error('Bulk schedule failed');
         },
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: 'Bulk schedule failed',
      }]);
   });

   test('buildEmptyItineraryPanelContent shows error feedback when nothing is scheduled to rebuild', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            errorType: MOCK_ERROR_TYPES.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
            message: APP_STRINGS.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
      }]);
   });

   test('buildEmptyItineraryPanelContent shows error feedback when nothing is scheduled to unschedule', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         unscheduleAll: async () => ({
            errorType: MOCK_ERROR_TYPES.UNSCHEDULE_ALL_NOTHING_SCHEDULED,
            message: APP_STRINGS.itinerary.errors.unscheduleAllNothingScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onUnscheduleAllItemsClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.errors.unscheduleAllNothingScheduled,
      }]);
   });

   test('buildEmptyItineraryPanelContent refreshes and shows not-enough-time feedback', async () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            issues: [{
               type: 'bulkScheduleItineraryNotEnoughTime',
               items: [],
            }],
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.confirmation.bulkScheduleItineraryNotEnoughTimeMessage,
      }]);
   });

   test('buildItineraryPanelContent uses the generic error when bulk scheduling fails without a message', async () => {
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => {
            throw new Error('');
         },
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
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
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.errors.generic,
      }]);
   });

   test('buildItineraryPanelContent queues success feedback after rebuild schedule', async () => {
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            issues: [],
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [{
               species: 'Tiger',
               exhibit: 'Savanna',
               start_time: '10:00',
               end_time: '10:30',
            }],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'success',
         message: APP_STRINGS.itinerary.dayPlanner.rebuildScheduleSuccess,
      }]);
   });

   test('buildEmptyItineraryPanelContent rebuilds without long-wait confirmation for existing items', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      const bodyEl = createDomNode('div', 'side-panel-body');
      let refreshed = false;
      const feedbackCalls = [];
      const confirmationCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            issues: [],
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
         showLongWaitConfirmation: (options) => {
            confirmationCalls.push(options);
         },
      });

      buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.equal(confirmationCalls.length, 0);
      assert.deepEqual(feedbackCalls, [{
         variant: 'success',
         message: APP_STRINGS.itinerary.dayPlanner.rebuildScheduleSuccess,
      }]);
   });

   test('buildItineraryPanelContent shows error feedback when nothing is scheduled to rebuild', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            errorType: MOCK_ERROR_TYPES.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
            message: APP_STRINGS.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
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
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
      }]);
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

   test('buildItineraryPanelContent unschedules all items and queues success feedback', async () => {
      let unscheduled = false;
      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         unscheduleAll: async () => {
            unscheduled = true;
            return {};
         },
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [{
               species: 'Tiger',
               exhibit: 'Savanna',
               start_time: '10:00',
               end_time: '10:30',
            }],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onUnscheduleAllItemsClick?.();

      assert.equal(unscheduled, true);
      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'success',
         message: APP_STRINGS.itinerary.dayPlanner.unscheduleAllSuccess,
      }]);
   });

   test('buildItineraryPanelContent shows error feedback when nothing is scheduled to unschedule', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      let refreshed = false;
      const feedbackCalls = [];
      const notices = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         unscheduleAll: async () => ({
            errorType: MOCK_ERROR_TYPES.UNSCHEDULE_ALL_NOTHING_SCHEDULED,
            message: APP_STRINGS.itinerary.errors.unscheduleAllNothingScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
         showNotice: (message) => {
            notices.push(message);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [{
               species: 'Tiger',
               exhibit: 'Savanna',
            }],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onUnscheduleAllItemsClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(notices, []);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: APP_STRINGS.itinerary.errors.unscheduleAllNothingScheduled,
      }]);
   });

   test('buildItineraryPanelContent shows error feedback when unschedule all throws', async () => {
      let refreshed = false;
      const feedbackCalls = [];
      const notices = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         unscheduleAll: async () => {
            throw new TypeError('Failed to fetch');
         },
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
         showNotice: (message) => {
            notices.push(message);
         },
      });

      buildItineraryPanelContent(
         {
            date: '2026-06-15',
            animals: [{
               species: 'Tiger',
               exhibit: 'Savanna',
               start_time: '10:00',
               end_time: '10:30',
            }],
            attractions: [],
            guardiansTalks: [],
            wildEncounters: [],
            itineraryConfig: ITINERARY_CONFIG,
         },
         ZOO_HOURS,
         {
            onPanelRefresh: async () => {
               refreshed = true;
            },
            deps,
         }
      );

      await getPlannerOptions()?.onUnscheduleAllItemsClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(notices, []);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: 'Failed to fetch',
      }]);
   });
});
