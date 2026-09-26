import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { GiftShopOpeningController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopOpeningController.js';
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


test('Test_CreateGiftShopOpeningScheduleController_TestWiring_ExpectWeeklyForm', () => {
   const entity = 'Zootique';
   const capture = _captureWeeklyForm();

   try {
      GiftShopOpeningController.createGiftShopOpeningScheduleController({});

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadGiftShops);
      assert.equal(capture.getCaptured().submitSchedule, ConsoleOperationsClient.setGiftShopOpeningSchedule);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.giftShop);
      assert.equal(capture.getCaptured().payloadKey, 'giftShop');
      assert.equal(capture.getCaptured().resultName({ gift_shop: entity }), entity);
   } finally {
      capture.restore();
   }
});


test('Test_CreateGiftShopOpeningScheduleController_TestResolveOverlapReplace_ExpectReplaced', async () => {
   const payload = { giftShop: 'Zootique' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps;
   ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps = async (value) => ({ replaced: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
   );

   try {
      GiftShopOpeningController.createGiftShopOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { replaced: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps = originalReplace;
      capture.restore();
   }
});


test('Test_CreateGiftShopOpeningScheduleController_TestResolveOverlapTrim_ExpectTrimmed', async () => {
   const payload = { giftShop: 'Zootique' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalTrim = ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps;
   ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps = async (value) => ({ trimmed: value });
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
      OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
   );

   try {
      GiftShopOpeningController.createGiftShopOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.deepEqual(result, { trimmed: payload });
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps = originalTrim;
      capture.restore();
   }
});


test('Test_CreateGiftShopOpeningScheduleController_TestResolveOverlapCancel_ExpectNull', async () => {
   const payload = { giftShop: 'Zootique' };
   const capture = _captureWeeklyForm();
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;

   try {
      GiftShopOpeningController.createGiftShopOpeningScheduleController({});
      const result = await capture.getCaptured().resolveOverlapConflict(payload);

      assert.equal(result, null);
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      capture.restore();
   }
});
