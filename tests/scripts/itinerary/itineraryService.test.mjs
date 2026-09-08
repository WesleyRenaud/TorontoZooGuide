import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryNormalizer } from '../../../scripts/itinerary/itineraryNormalizer.js';
import { ItinerarySearchContext } from '../../../scripts/itinerary/itinerarySearchContext.js';
import { ItineraryService } from '../../../scripts/itinerary/itineraryService.js';
import { ItineraryServiceHelper } from '../../../scripts/itinerary/itineraryServiceHelper.js';
import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('Test_DispatchItineraryUpdated_TestItinerary_ExpectCustomEvent', () => {
   const events = [];
   window.dispatchEvent = (event) => {
      events.push(event);
      return true;
   };

   ItineraryService.dispatchItineraryUpdated({ date: '2026-06-15' });

   assert.equal(events.length, 1);
   assert.equal(events[0].type, 'tzg:itineraryUpdated');
   assert.deepEqual(events[0].detail, { itinerary: { date: '2026-06-15' } });
});

test('Test_DispatchScheduleItineraryItemResult_TestMissingItinerary_ExpectNoOp', () => {
   const original = ItineraryService.dispatchItineraryUpdated;
   const calls = [];
   ItineraryService.dispatchItineraryUpdated = (...args) => {
      calls.push(args);
   };

   try {
      ItineraryService.dispatchScheduleItineraryItemResult({});
      assert.deepEqual(calls, []);
   } finally {
      ItineraryService.dispatchItineraryUpdated = original;
   }
});

test('Test_DispatchScheduleItineraryItemResult_TestWithItinerary_ExpectNormalizedDispatch', () => {
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const calls = [];

   ItineraryNormalizer.normalizeItineraryFromApiResult = (result) => ({
      ...result.itinerary,
      normalized: true,
   });
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      calls.push(itinerary);
   };

   try {
      ItineraryService.dispatchScheduleItineraryItemResult({
         itinerary: { date: '2026-06-15' },
      });
      assert.deepEqual(calls, [{ date: '2026-06-15', normalized: true }]);
   } finally {
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});

test('Test_GetItinerary_TestApiResult_ExpectNormalized', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.getItineraryRequest;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;

   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => '2026-06-15';
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.getItineraryRequest = async (temp) => {
      assert.equal(temp, null);
      return { itinerary: { date: '2026-06-15' } };
   };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({
      date: '2026-06-15',
      animals: [],
   });

   try {
      assert.deepEqual(await ItineraryService.getItinerary(), {
         date: '2026-06-15',
         animals: [],
      });
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.getItineraryRequest = originalRequest;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
   }
});

test('Test_GetZooHours_TestMissingOrInvalidDate_ExpectNull', async () => {
   assert.equal(await ItineraryService.getZooHours(null), null);
   assert.equal(await ItineraryService.getZooHours(''), null);

   const originalMonth = VisitDateValidator.getMonth;
   const originalDay = VisitDateValidator.getDay;
   const originalYear = VisitDateValidator.getYear;
   VisitDateValidator.getMonth = () => null;
   VisitDateValidator.getDay = () => 15;
   VisitDateValidator.getYear = () => 2026;

   try {
      assert.equal(await ItineraryService.getZooHours('2026-06-15'), null);
   } finally {
      VisitDateValidator.getMonth = originalMonth;
      VisitDateValidator.getDay = originalDay;
      VisitDateValidator.getYear = originalYear;
   }
});

test('Test_GetZooHours_TestValidDate_ExpectHours', async () => {
   const originalMonth = VisitDateValidator.getMonth;
   const originalDay = VisitDateValidator.getDay;
   const originalYear = VisitDateValidator.getYear;
   const originalRequest = ItineraryClient.getZooHoursRequest;

   VisitDateValidator.getMonth = () => 'JUN';
   VisitDateValidator.getDay = () => 15;
   VisitDateValidator.getYear = () => 2026;
   ItineraryClient.getZooHoursRequest = async (payload) => {
      assert.deepEqual(payload, { day: 15, month: 'JUN', year: 2026 });
      return { hours: { openTime: '09:30', closeTime: '19:00' } };
   };

   try {
      assert.deepEqual(await ItineraryService.getZooHours('2026-06-15'), {
         openTime: '09:30',
         closeTime: '19:00',
      });
   } finally {
      VisitDateValidator.getMonth = originalMonth;
      VisitDateValidator.getDay = originalDay;
      VisitDateValidator.getYear = originalYear;
      ItineraryClient.getZooHoursRequest = originalRequest;
   }
});

test('Test_ClearItinerary_TestSuccess_ExpectClearedEvents', async () => {
   const originalRequest = ItineraryClient.clearItineraryRequest;
   const originalEmpty = ItineraryNormalizer.createEmptyItinerary;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const events = [];
   const dispatches = [];

   ItineraryClient.clearItineraryRequest = async () => ({ success: true });
   ItineraryNormalizer.createEmptyItinerary = () => ({ date: null, animals: [] });
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };
   window.dispatchEvent = (event) => {
      events.push(event.type);
      return true;
   };

   try {
      assert.deepEqual(await ItineraryService.clearItinerary(), { success: true });
      assert.deepEqual(events, ['tzg:itineraryCleared']);
      assert.deepEqual(dispatches, [{ date: null, animals: [] }]);
   } finally {
      ItineraryClient.clearItineraryRequest = originalRequest;
      ItineraryNormalizer.createEmptyItinerary = originalEmpty;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});

test('Test_BulkScheduleItinerary_TestError_ExpectMessagePayload', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.bulkScheduleItineraryRequest;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;

   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => '2026-06-15';
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: false });
   ItineraryClient.bulkScheduleItineraryRequest = async (_temp, options) => {
      assert.equal(options.confirmingFixedTimeItemLongWait, true);
      return { errorType: 'fixedTimeItemLongWait', issues: [{ code: 'wait' }] };
   };
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => 'long wait';

   try {
      assert.deepEqual(
         await ItineraryService.bulkScheduleItinerary({ confirmingFixedTimeItemLongWait: true }),
         {
            errorType: 'fixedTimeItemLongWait',
            message: 'long wait',
            issues: [{ code: 'wait' }],
         }
      );
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.bulkScheduleItineraryRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
   }
});

test('Test_BulkScheduleItinerary_TestSuccess_ExpectNormalizedItinerary', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.bulkScheduleItineraryRequest;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const dispatches = [];

   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => '2026-06-15';
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.bulkScheduleItineraryRequest = async () => ({
      errorType: 'success',
      itinerary: { date: '2026-06-15' },
      issues: [],
   });
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({ date: '2026-06-15', animals: [] });
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };

   try {
      assert.deepEqual(await ItineraryService.bulkScheduleItinerary(), {
         itinerary: { date: '2026-06-15', animals: [] },
         issues: [],
      });
      assert.equal(dispatches.length, 1);
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.bulkScheduleItineraryRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});

test('Test_UnscheduleAllItineraryItems_TestErrorAndSuccess_ExpectPayloads', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.unscheduleAllItineraryItemsRequest;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;

   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => '2026-06-15';
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.unscheduleAllItineraryItemsRequest = async () => ({ errorType: 'empty' });
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => 'nothing scheduled';

   try {
      assert.deepEqual(await ItineraryService.unscheduleAllItineraryItems(), {
         errorType: 'empty',
         message: 'nothing scheduled',
      });

      ItineraryErrorTypes.isItinerarySuccess = () => true;
      ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({ date: '2026-06-15' });
      ItineraryService.dispatchItineraryUpdated = () => {};
      ItineraryClient.unscheduleAllItineraryItemsRequest = async () => ({
         errorType: 'success',
         itinerary: { date: '2026-06-15' },
      });

      assert.deepEqual(await ItineraryService.unscheduleAllItineraryItems(), {
         itinerary: { date: '2026-06-15' },
      });
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.unscheduleAllItineraryItemsRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});

test('Test_AcceptItinerary_TestKeepLists_ExpectNormalized', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.acceptItineraryRequest;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const dispatches = [];

   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => '2026-06-15';
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: true });
   ItineraryClient.acceptItineraryRequest = async (temp, keep) => {
      assert.equal(temp, true);
      assert.deepEqual(keep, {
         animalsToKeep: ['Lion'],
         attractionsToKeep: ['Carousel'],
      });
      return { itinerary: { date: '2026-06-15' } };
   };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => ({ date: '2026-06-15', accepted: true });
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };

   try {
      assert.deepEqual(
         await ItineraryService.acceptItinerary({
            animalsToKeep: ['Lion'],
            attractionsToKeep: ['Carousel'],
         }),
         { date: '2026-06-15', accepted: true }
      );
      assert.equal(dispatches.length, 1);
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.acceptItineraryRequest = originalRequest;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});

test('Test_HasActiveItinerary_TestFlags_ExpectBoolean', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalHas = ItineraryShape.hasSavedItineraryContent;

   ItineraryService.getItinerary = async () => ({ isActive: true });
   ItineraryShape.hasSavedItineraryContent = () => true;

   try {
      assert.equal(await ItineraryService.hasActiveItinerary(), true);

      ItineraryShape.hasSavedItineraryContent = () => false;
      assert.equal(await ItineraryService.hasActiveItinerary(), false);

      ItineraryService.getItinerary = async () => ({ isActive: false });
      ItineraryShape.hasSavedItineraryContent = () => true;
      assert.equal(await ItineraryService.hasActiveItinerary(), false);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryShape.hasSavedItineraryContent = originalHas;
   }
});
