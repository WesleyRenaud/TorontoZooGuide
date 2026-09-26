import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { GiftShopController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopController.js';
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


test('Test_CreateGiftShopClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      GiftShopController.createGiftShopClosedController({ giftShopEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadGiftShops);
   } finally {
      capture.restore();
   }
});


test('Test_CreateGiftShopClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const giftShop = 'Zootique';
   const message = 'x';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setGiftShopClosed;
   ConsoleOperationsClient.setGiftShopClosed = async (payload) => payload;

   try {
      GiftShopController.createGiftShopClosedController({ giftShopEl: {} });
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
      ConsoleOperationsClient.setGiftShopClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateGiftShopClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const giftShop = 'Zootique';
   const capture = _captureClosedForm();

   try {
      GiftShopController.createGiftShopClosedController({ giftShopEl: {} });
      const status = capture.getCaptured().successMessage({ gift_shop: giftShop });

      assert.equal(status, Strings.status.closed(giftShop));
   } finally {
      capture.restore();
   }
});
