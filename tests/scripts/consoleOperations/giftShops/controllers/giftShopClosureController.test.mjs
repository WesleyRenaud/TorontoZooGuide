import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { GiftShopClosureController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopClosureController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { Strings } from '../../../../../scripts/strings.js';


function _captureClosedForm() {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };
   return {
      getCaptured: () => captured,
      restore: () => {
         EntityClosedFormController.createEntityClosedFormController = original;
      },
   };
}


test('Test_CreateGiftShopClosureOverrideController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      GiftShopClosureController.createGiftShopClosureOverrideController({ giftShopEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadGiftShops);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.giftShop);
   } finally {
      capture.restore();
   }
});


test('Test_CreateGiftShopClosureOverrideController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const giftShop = 'Zootique';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setGiftShopClosureOverride;
   ConsoleOperationsClient.setGiftShopClosureOverride = async (payload) => payload;

   try {
      GiftShopClosureController.createGiftShopClosureOverrideController({ giftShopEl: {} });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: giftShop,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         giftShop,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setGiftShopClosureOverride = originalSet;
      capture.restore();
   }
});


test('Test_CreateGiftShopClosureOverrideController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const giftShop = 'Zootique';
   const capture = _captureClosedForm();

   try {
      GiftShopClosureController.createGiftShopClosureOverrideController({ giftShopEl: {} });
      const status = capture.getCaptured().successMessage({ gift_shop: giftShop });

      assert.equal(status, Strings.status.closureOverrideSaved(giftShop));
   } finally {
      capture.restore();
   }
});
