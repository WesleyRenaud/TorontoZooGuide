import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopOpeningController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopOpeningController.js';
import { WeeklyAvailabilityFormController } from '../../../../../scripts/consoleOperations/forms/weeklyAvailabilityFormController.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateGiftShopOpeningScheduleController_TestWiring_ExpectWeeklyForm', async () => {
   const original = WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController;
   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalReplace = ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps;
   const originalTrim = ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps;
   let captured;

   WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps = async (p) => ({ replaced: p });
   ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps = async (p) => ({ trimmed: p });

   try {
      GiftShopOpeningController.createGiftShopOpeningScheduleController({ giftShopEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadGiftShops);
      assert.equal(captured.submitSchedule, ConsoleOperationsClient.setGiftShopOpeningSchedule);
      assert.equal(captured.entityLabel, Strings.entityLabels.giftShop);
      assert.equal(captured.payloadKey, 'giftShop');
      assert.equal(captured.resultName({ gift_shop: 'Zootique' }), 'Zootique');

      const payload = { giftShop: 'Zootique' };

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
      ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps = originalReplace;
      ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps = originalTrim;
   }
});
