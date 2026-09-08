import assert from 'node:assert/strict';
import test from 'node:test';

import { GiftShopClosureController } from '../../../../../scripts/consoleOperations/giftShops/controllers/giftShopClosureController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateGiftShopClosureOverrideController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      GiftShopClosureController.createGiftShopClosureOverrideController({ giftShopEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadGiftShops);
      assert.equal(captured.entityLabel, Strings.entityLabels.giftShop);

      const originalSet = ConsoleOperationsClient.setGiftShopClosureOverride;
      ConsoleOperationsClient.setGiftShopClosureOverride = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Zootique', startDate: '', endDate: '', message: 'm' }),
            { giftShop: 'Zootique', startDate: null, endDate: null, message: 'm' }
         );
         assert.equal(
            captured.successMessage({ gift_shop: 'Zootique' }),
            Strings.status.closureOverrideSaved('Zootique')
         );
      } finally {
         ConsoleOperationsClient.setGiftShopClosureOverride = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
