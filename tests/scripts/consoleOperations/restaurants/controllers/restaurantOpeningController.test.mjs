import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantOpeningController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantOpeningController.js';
import { WeeklyAvailabilityFormController } from '../../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestaurantOpeningScheduleController_TestWiring_ExpectWeeklyForm', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps;
   const originalTrim = ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps;
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps = async (p) => ({ replaced: p });
   ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps = async (p) => ({ trimmed: p });

   try {
      RestaurantOpeningController.createRestaurantOpeningScheduleController({ restaurantEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestaurants);
      assert.equal(captured.submitSchedule, ConsoleOperationsClient.setRestaurantOpeningSchedule);
      assert.equal(captured.entityLabel, Strings.entityLabels.restaurant);
      assert.equal(captured.payloadKey, 'restaurant');
      assert.equal(captured.resultName({ restaurant: 'Peaks' }), 'Peaks');

      const payload = { restaurant: 'Peaks' };

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );
      assert.deepEqual(await captured.resolveOverlapConflict(payload), { replaced: payload });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
      );
      assert.deepEqual(await captured.resolveOverlapConflict(payload), { trimmed: payload });

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      assert.equal(await captured.resolveOverlapConflict(payload), null);
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps = originalReplace;
      ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps = originalTrim;
   }
});
