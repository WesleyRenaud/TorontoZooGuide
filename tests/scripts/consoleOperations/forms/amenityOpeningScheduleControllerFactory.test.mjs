import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpeningScheduleControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityOpeningScheduleControllerFactory.js';
import { OpeningScheduleOverlapFragment } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { WeeklyAvailabilityFormController } from '../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';

test('Test_CreateAmenityOpeningScheduleController_TestWiring_ExpectWeeklyFormWithResolver', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      const controller = AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
         entityLabel: 'Restaurant',
         optionsLabel: 'Restaurants',
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         replaceOverlaps: async (payload) => ({ replaced: payload }),
         trimOverlaps: async (payload) => ({ trimmed: payload }),
      });

      assert.deepEqual(controller, { created: true });
      assert.equal(captured.payloadKey, 'restaurant');

      const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
      const payload = { restaurant: 'Peaks' };

      try {
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
         OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      }
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
   }
});
