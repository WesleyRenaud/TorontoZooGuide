import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { RestaurantOpeningController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantOpeningController.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { Strings } from '../../../../../scripts/strings.js';


function _captureWeeklyForm() {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   let captured;
   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   return {
      getCaptured: () => captured,
      restore: () => {
         WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      },
   };
}


test('Test_CreateRestaurantOpeningScheduleController_TestWiring_ExpectWeeklyForm', () => {
   const entity = 'Peaks';
   const capture = _captureWeeklyForm();

   try {
      RestaurantOpeningController.createRestaurantOpeningScheduleController({});

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadRestaurants);
      assert.equal(capture.getCaptured().submitSchedule, ConsoleOperationsClient.setRestaurantOpeningSchedule);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.restaurant);
      assert.equal(capture.getCaptured().payloadKey, 'restaurant');
      assert.equal(capture.getCaptured().resultName({ restaurant: entity }), entity);
   } finally {
      capture.restore();
   }
});


test('Test_CreateRestaurantOpeningScheduleController_TestResolveOverlapReplace_ExpectReplaced', async () => {
   const payload = { restaurant: 'Peaks' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps;
   ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps = async (value) => ({ replaced: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
   );

   try {
      RestaurantOpeningController.createRestaurantOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { replaced: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps = originalReplace;
      capture.restore();
   }
});


test('Test_CreateRestaurantOpeningScheduleController_TestResolveOverlapTrim_ExpectTrimmed', async () => {
   const payload = { restaurant: 'Peaks' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalTrim = ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps;
   ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps = async (value) => ({ trimmed: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
   );

   try {
      RestaurantOpeningController.createRestaurantOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { trimmed: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps = originalTrim;
      capture.restore();
   }
});


test('Test_CreateRestaurantOpeningScheduleController_TestResolveOverlapCancel_ExpectNull', async () => {
   const payload = { restaurant: 'Peaks' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;

   try {
      RestaurantOpeningController.createRestaurantOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.equal(result, null);
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      capture.restore();
   }
});
