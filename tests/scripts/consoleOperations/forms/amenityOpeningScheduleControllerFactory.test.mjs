import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpeningScheduleControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityOpeningScheduleControllerFactory.js';
import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';


test('Test_CreateAmenityOpeningScheduleController_TestWiring_ExpectWeeklyForm', () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const created = { created: true };
   const payloadKey = 'restaurant';
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return created;
   };

   try {
      const controller = AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
         entityLabel: 'Restaurant',
         optionsLabel: 'Restaurants',
         payloadKey,
         resultName: result => result.restaurant,
         replaceOverlaps: async (payload) => ({ replaced: payload }),
         trimOverlaps: async (payload) => ({ trimmed: payload }),
      });

      assert.equal(controller, created);
      assert.equal(captured.payloadKey, payloadKey);
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
   }
});


test('Test_CreateAmenityOpeningScheduleController_TestReplaceOverlap_ExpectReplaced', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const payload = { restaurant: 'Peaks' };
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
   );

   try {
      AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
         entityLabel: 'Restaurant',
         optionsLabel: 'Restaurants',
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         replaceOverlaps: async (nextPayload) => ({ replaced: nextPayload }),
         trimOverlaps: async (nextPayload) => ({ trimmed: nextPayload }),
      });

      const result = await captured.resolveOverlapConflict(payload);

      assert.deepEqual(result, { replaced: payload });
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});


test('Test_CreateAmenityOpeningScheduleController_TestTrimOverlap_ExpectTrimmed', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const payload = { restaurant: 'Peaks' };
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
   );

   try {
      AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
         entityLabel: 'Restaurant',
         optionsLabel: 'Restaurants',
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         replaceOverlaps: async (nextPayload) => ({ replaced: nextPayload }),
         trimOverlaps: async (nextPayload) => ({ trimmed: nextPayload }),
      });

      const result = await captured.resolveOverlapConflict(payload);

      assert.deepEqual(result, { trimmed: payload });
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});


test('Test_CreateAmenityOpeningScheduleController_TestDismissOverlap_ExpectNull', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const payload = { restaurant: 'Peaks' };
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;

   try {
      AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitSchedule: async () => ({ success: true }),
         entityLabel: 'Restaurant',
         optionsLabel: 'Restaurants',
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         replaceOverlaps: async (nextPayload) => ({ replaced: nextPayload }),
         trimOverlaps: async (nextPayload) => ({ trimmed: nextPayload }),
      });

      const result = await captured.resolveOverlapConflict(payload);

      assert.equal(result, null);
   } finally {
      WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = original;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
   }
});
