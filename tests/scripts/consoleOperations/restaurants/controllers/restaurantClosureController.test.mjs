import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { RestaurantClosureController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantClosureController.js';
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


test('Test_CreateRestaurantClosureOverrideController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      RestaurantClosureController.createRestaurantClosureOverrideController({ restaurantEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadRestaurants);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.restaurant);
   } finally {
      capture.restore();
   }
});


test('Test_CreateRestaurantClosureOverrideController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const restaurant = 'Peaks';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setRestaurantClosureOverride;
   ConsoleOperationsClient.setRestaurantClosureOverride = async (payload) => payload;

   try {
      RestaurantClosureController.createRestaurantClosureOverrideController({ restaurantEl: {} });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: restaurant,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         restaurant,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setRestaurantClosureOverride = originalSet;
      capture.restore();
   }
});


test('Test_CreateRestaurantClosureOverrideController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const restaurant = 'Peaks';
   const capture = _captureClosedForm();

   try {
      RestaurantClosureController.createRestaurantClosureOverrideController({ restaurantEl: {} });
      const status = capture.getCaptured().successMessage({ restaurant });

      assert.equal(status, Strings.status.closureOverrideSaved(restaurant));
   } finally {
      capture.restore();
   }
});
