import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateGiftShopClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      GiftShopController.createGiftShopClosedController({ giftShopEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadGiftShops);
      const originalSet = ConsoleOperationsClient.setGiftShopClosed;
      ConsoleOperationsClient.setGiftShopClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Zootique', startDate: '', endDate: '', message: 'x' }),
            { giftShop: 'Zootique', startDate: null, endDate: null, message: 'x' }
         );
         assert.equal(captured.successMessage({ gift_shop: 'Zootique' }), Strings.status.closed('Zootique'));
      } finally {
         ConsoleOperationsClient.setGiftShopClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
