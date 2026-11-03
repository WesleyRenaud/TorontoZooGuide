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


test('Test_CreateGiftShopClosedForSeasonController_TestSubmit_ExpectSeasonPayload', async (t) => {
   const giftShop = 'Zootique';
   const startDate = '2026-11-02';
   const original = EntityClosedFormController.createEntityClosedFormController;
   const originalSet = ConsoleOperationsClient.setGiftShopClosedForSeason;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setGiftShopClosedForSeason = async (payload) => payload;
   t.after(() => {
      EntityClosedFormController.createEntityClosedFormController = original;
      ConsoleOperationsClient.setGiftShopClosedForSeason = originalSet;
   });

   GiftShopController.createGiftShopClosedForSeasonController({ giftShopEl: { id: 'g' } });
   const payload = await captured.submitClosedStatus({
      entity: giftShop,
      startDate,
      endDate: '',
      message: '',
   });

   assert.deepEqual(payload, {
      giftShop,
      startDate,
      endDate: null,
      message: '',
   });
   assert.equal(
      captured.successMessage({ gift_shop: giftShop }),
      Strings.status.closedForSeason(giftShop),
   );
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadGiftShops);
});


test('Test_CreateGiftShopOpenForSeasonController_TestSubmit_ExpectSeasonList', async (t) => {
   const giftShop = 'Zootique';
   const { EntityOpenFormController } = await import(
      '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js'
   );
   const original = EntityOpenFormController.createEntityOpenFormController;
   const originalSet = ConsoleOperationsClient.setGiftShopOpenForSeason;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setGiftShopOpenForSeason = async (payload) => payload;
   t.after(() => {
      EntityOpenFormController.createEntityOpenFormController = original;
      ConsoleOperationsClient.setGiftShopOpenForSeason = originalSet;
   });

   GiftShopController.createGiftShopOpenForSeasonController({ giftShopEl: { id: 'g' } });
   const payload = await captured.submitOpenStatus({ entity: giftShop });

   assert.deepEqual(payload, { giftShop });
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadClosedForSeasonGiftShops);
   assert.equal(
      captured.successMessage({ gift_shop: giftShop }),
      Strings.status.openForSeason(giftShop),
   );
});
