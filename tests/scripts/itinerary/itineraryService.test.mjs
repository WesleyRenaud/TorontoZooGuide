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
import { Position } from '../../../scripts/shared/enums/position.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();


test('Test_DispatchItineraryUpdated_TestItinerary_ExpectCustomEvent', () => {
   const events = [];
   const date = '2026-06-15';
   const itinerary = { date };
   window.dispatchEvent = (event) => {
      events.push(event);
      return true;
   };

   ItineraryService.dispatchItineraryUpdated(itinerary);

   assert.equal(events.length, 1);
   assert.equal(events[Position.FIRST].type, 'tzg:itineraryUpdated');
   assert.deepEqual(events[Position.FIRST].detail, { itinerary });
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
   const date = '2026-06-15';
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
         itinerary: { date },
      });

      assert.deepEqual(calls, [{ date, normalized: true }]);
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
   const date = '2026-06-15';
   const normalized = { date, animals: [] };
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.getItineraryRequest = async (temp) => {
      assert.equal(temp, null);
      return { itinerary: { date } };
   };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;

   try {
      const itinerary = await ItineraryService.getItinerary();

      assert.deepEqual(itinerary, normalized);
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.getItineraryRequest = originalRequest;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
   }
});


test('Test_GetZooHours_TestNull_ExpectNull', async () => {
   const date = null;

   const hours = await ItineraryService.getZooHours(date);

   assert.equal(hours, null);
});


test('Test_GetZooHours_TestEmpty_ExpectNull', async () => {
   const date = '';

   const hours = await ItineraryService.getZooHours(date);

   assert.equal(hours, null);
});


test('Test_GetZooHours_TestInvalidMonth_ExpectNull', async () => {
   const originalMonth = VisitDateValidator.getMonth;
   const originalDay = VisitDateValidator.getDay;
   const originalYear = VisitDateValidator.getYear;
   const date = '2026-06-15';
   VisitDateValidator.getMonth = () => null;
   VisitDateValidator.getDay = () => 15;
   VisitDateValidator.getYear = () => 2026;

   try {
      const hours = await ItineraryService.getZooHours(date);

      assert.equal(hours, null);
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
   const date = '2026-06-15';
   const day = 15;
   const month = 'JUN';
   const year = 2026;
   const openTime = '09:30';
   const closeTime = '19:00';
   VisitDateValidator.getMonth = () => month;
   VisitDateValidator.getDay = () => day;
   VisitDateValidator.getYear = () => year;
   ItineraryClient.getZooHoursRequest = async (payload) => {
      assert.deepEqual(payload, { day, month, year });
      return { hours: { openTime, closeTime } };
   };

   try {
      const hours = await ItineraryService.getZooHours(date);

      assert.deepEqual(hours, { openTime, closeTime });
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
   const cleared = { success: true };
   const emptyItinerary = { date: null, animals: [] };
   ItineraryClient.clearItineraryRequest = async () => cleared;
   ItineraryNormalizer.createEmptyItinerary = () => emptyItinerary;
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };
   window.dispatchEvent = (event) => {
      events.push(event.type);
      return true;
   };

   try {
      const result = await ItineraryService.clearItinerary();

      assert.deepEqual(result, cleared);
      assert.deepEqual(events, ['tzg:itineraryCleared']);
      assert.deepEqual(dispatches, [emptyItinerary]);
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
   const date = '2026-06-15';
   const errorType = 'fixedTimeItemLongWait';
   const message = 'long wait';
   const issues = [{ code: 'wait' }];
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: false });
   ItineraryClient.bulkScheduleItineraryRequest = async (_temp, options) => {
      assert.equal(options.confirmingFixedTimeItemLongWait, true);
      return { errorType, issues };
   };
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => message;

   try {
      const result = await ItineraryService.bulkScheduleItinerary({
         confirmingFixedTimeItemLongWait: true,
      });

      assert.equal(result.errorType, errorType);
      assert.equal(result.message, message);
      assert.deepEqual(result.issues, issues);
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
   const date = '2026-06-15';
   const issues = [];
   const normalized = { date, animals: [] };
   const dispatches = [];
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.bulkScheduleItineraryRequest = async () => ({
      errorType: 'success',
      itinerary: { date },
      issues,
   });
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };

   try {
      const result = await ItineraryService.bulkScheduleItinerary();

      assert.equal(result.itinerary, normalized);
      assert.deepEqual(result.issues, issues);
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


test('Test_UnscheduleAllItineraryItems_TestError_ExpectMessagePayload', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.unscheduleAllItineraryItemsRequest;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalResolve = ItineraryErrorTypes.resolveItineraryErrorMessage;
   const date = '2026-06-15';
   const errorType = 'empty';
   const message = 'nothing scheduled';
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryClient.unscheduleAllItineraryItemsRequest = async () => ({ errorType });
   ItineraryErrorTypes.isItinerarySuccess = () => false;
   ItineraryErrorTypes.resolveItineraryErrorMessage = () => message;

   try {
      const result = await ItineraryService.unscheduleAllItineraryItems();

      assert.equal(result.errorType, errorType);
      assert.equal(result.message, message);
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.unscheduleAllItineraryItemsRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
      ItineraryErrorTypes.resolveItineraryErrorMessage = originalResolve;
   }
});


test('Test_UnscheduleAllItineraryItems_TestSuccess_ExpectNormalizedItinerary', async () => {
   const originalFetchDate = ItineraryServiceHelper.fetchSavedItineraryVisitDate;
   const originalContext = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalRequest = ItineraryClient.unscheduleAllItineraryItemsRequest;
   const originalSuccess = ItineraryErrorTypes.isItinerarySuccess;
   const originalNormalize = ItineraryNormalizer.normalizeItineraryFromApiResult;
   const originalDispatch = ItineraryService.dispatchItineraryUpdated;
   const date = '2026-06-15';
   const normalized = { date };
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: null });
   ItineraryErrorTypes.isItinerarySuccess = () => true;
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;
   ItineraryService.dispatchItineraryUpdated = () => {};
   ItineraryClient.unscheduleAllItineraryItemsRequest = async () => ({
      errorType: 'success',
      itinerary: { date },
   });

   try {
      const result = await ItineraryService.unscheduleAllItineraryItems();

      assert.deepEqual(result, { itinerary: normalized });
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.unscheduleAllItineraryItemsRequest = originalRequest;
      ItineraryErrorTypes.isItinerarySuccess = originalSuccess;
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
   const date = '2026-06-15';
   const animalsToKeep = ['Lion'];
   const attractionsToKeep = ['Carousel'];
   const normalized = { date, accepted: true };
   const dispatches = [];
   ItineraryServiceHelper.fetchSavedItineraryVisitDate = async () => date;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ temp: true });
   ItineraryClient.acceptItineraryRequest = async (temp, keep) => {
      assert.equal(temp, true);
      assert.deepEqual(keep, { animalsToKeep, attractionsToKeep });
      return { itinerary: { date } };
   };
   ItineraryNormalizer.normalizeItineraryFromApiResult = () => normalized;
   ItineraryService.dispatchItineraryUpdated = (itinerary) => {
      dispatches.push(itinerary);
   };

   try {
      const itinerary = await ItineraryService.acceptItinerary({
         animalsToKeep,
         attractionsToKeep,
      });

      assert.deepEqual(itinerary, normalized);
      assert.equal(dispatches.length, 1);
   } finally {
      ItineraryServiceHelper.fetchSavedItineraryVisitDate = originalFetchDate;
      ItinerarySearchContext.getItineraryDateSearchContext = originalContext;
      ItineraryClient.acceptItineraryRequest = originalRequest;
      ItineraryNormalizer.normalizeItineraryFromApiResult = originalNormalize;
      ItineraryService.dispatchItineraryUpdated = originalDispatch;
   }
});


test('Test_HasActiveItinerary_TestActiveWithContent_ExpectTrue', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalHas = ItineraryShape.hasSavedItineraryContent;
   ItineraryService.getItinerary = async () => ({ isActive: true });
   ItineraryShape.hasSavedItineraryContent = () => true;

   try {
      const isActive = await ItineraryService.hasActiveItinerary();

      assert.equal(isActive, true);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryShape.hasSavedItineraryContent = originalHas;
   }
});


test('Test_HasActiveItinerary_TestNoContent_ExpectFalse', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalHas = ItineraryShape.hasSavedItineraryContent;
   ItineraryService.getItinerary = async () => ({ isActive: true });
   ItineraryShape.hasSavedItineraryContent = () => false;

   try {
      const isActive = await ItineraryService.hasActiveItinerary();

      assert.equal(isActive, false);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryShape.hasSavedItineraryContent = originalHas;
   }
});


test('Test_HasActiveItinerary_TestInactiveWithContent_ExpectFalse', async () => {
   const originalGet = ItineraryService.getItinerary;
   const originalHas = ItineraryShape.hasSavedItineraryContent;
   ItineraryService.getItinerary = async () => ({ isActive: false });
   ItineraryShape.hasSavedItineraryContent = () => true;

   try {
      const isActive = await ItineraryService.hasActiveItinerary();

      assert.equal(isActive, false);
   } finally {
      ItineraryService.getItinerary = originalGet;
      ItineraryShape.hasSavedItineraryContent = originalHas;
   }
});
