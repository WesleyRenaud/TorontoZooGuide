import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelContent } from '../../../../scripts/itinerary/panel/itineraryPanelContent.js';
import { Strings } from '../../../../scripts/strings.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { MOCK_ERROR_TYPES } from '../../helpers/scheduleItemActionsTestSetup.mjs';

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

   test('Test_ItineraryPanelContent_TestItineraryPanelContentDestroyRenderedPanelChildrenRunsChildCleanupHooks_ExpectOk', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      const child = createDomNode('div', 'panel-child');
      let cleaned = false;

      child.__tzgCleanup = () => {
         cleaned = true;
      };
      bodyEl.appendChild(child);

      ItineraryPanelContent.destroyRenderedPanelChildren(bodyEl);

      assert.equal(cleaned, true);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentClearRenderedPanelRemovesRenderedChildren_ExpectOk', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      bodyEl.appendChild(createDomNode('div', 'panel-child'));

      ItineraryPanelContent.clearRenderedPanel(bodyEl);

      assert.equal(bodyEl.children.length, 0);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentOpensTheScheduleModuleFromThe_ExpectOk', () => {
      const bodyEl = createDomNode('div', 'side-panel-body');
      const opened = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         openModule: (options) => {
            opened.push(options);
         },
         buildEventTypes: () => ['lunch'],
      });

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         deps,
      });

      getPlannerOptions()?.onScheduleItemClick?.();

      assert.equal(opened.length, 1);
      assert.deepEqual(opened[0].eventTypes, ['lunch']);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentShowsErrorFeedbackWhenBulkScheduling_ExpectOk', async () => {
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

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
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

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentShowsErrorFeedbackWhenNothingIs_ExpectOk', async () => {
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
            message: Strings.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: Strings.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentShowsErrorFeedbackWhenNothingIs_ExpectOk', async () => {
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
            message: Strings.itinerary.errors.unscheduleAllNothingScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onUnscheduleAllItemsClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: Strings.itinerary.errors.unscheduleAllNothingScheduled,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentRefreshesAndShowsNotEnoughTime_ExpectOk', async () => {
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

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps,
      });

      await getPlannerOptions()?.onRebuildScheduleClick?.();

      assert.equal(refreshed, true);
      assert.deepEqual(feedbackCalls, [{
         variant: 'error',
         message: Strings.itinerary.confirmation.bulkScheduleItineraryNotEnoughTimeMessage,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentUsesTheGenericErrorWhenBulk_ExpectOk', async () => {
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

      ItineraryPanelContent.buildItineraryPanelContent(
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
         message: Strings.itinerary.errors.generic,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentQueuesSuccessFeedbackAfterRebuildSchedule_ExpectOk', async () => {
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

      ItineraryPanelContent.buildItineraryPanelContent(
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
         message: Strings.itinerary.dayPlanner.rebuildScheduleSuccess,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildEmptyItineraryPanelContentRebuildsWithoutLongWaitConfirmationFor_ExpectOk', async () => {
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

      ItineraryPanelContent.buildEmptyItineraryPanelContent(bodyEl, ZOO_HOURS, {
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
         message: Strings.itinerary.dayPlanner.rebuildScheduleSuccess,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentShowsErrorFeedbackWhenNothingIs_ExpectOk', async () => {
      ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });

      let refreshed = false;
      const feedbackCalls = [];
      const { deps, getPlannerOptions } = captureDayPlannerOptions({
         bulkSchedule: async () => ({
            errorType: MOCK_ERROR_TYPES.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
            message: Strings.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
      });

      ItineraryPanelContent.buildItineraryPanelContent(
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
         message: Strings.itinerary.errors.bulkScheduleItineraryAlreadyScheduled,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentRefreshesAfterArrivalAndDepartureTime_ExpectOk', async () => {
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

      ItineraryPanelContent.buildItineraryPanelContent(
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

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentUnschedulesAllItemsAndQueuesSuccess_ExpectOk', async () => {
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

      ItineraryPanelContent.buildItineraryPanelContent(
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
         message: Strings.itinerary.dayPlanner.unscheduleAllSuccess,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentShowsErrorFeedbackWhenNothingIs_ExpectOk', async () => {
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
            message: Strings.itinerary.errors.unscheduleAllNothingScheduled,
         }),
         setActionFeedback: (feedback) => {
            feedbackCalls.push(feedback);
         },
         showNotice: (message) => {
            notices.push(message);
         },
      });

      ItineraryPanelContent.buildItineraryPanelContent(
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
         message: Strings.itinerary.errors.unscheduleAllNothingScheduled,
      }]);
   });

   test('Test_ItineraryPanelContent_TestItineraryPanelContentBuildItineraryPanelContentShowsErrorFeedbackWhenUnscheduleAll_ExpectOk', async () => {
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

      ItineraryPanelContent.buildItineraryPanelContent(
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
