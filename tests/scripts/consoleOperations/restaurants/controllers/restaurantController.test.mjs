import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { RestaurantController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantController.js';
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


test('Test_CreateRestaurantClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      RestaurantController.createRestaurantClosedController({ restaurantEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadRestaurants);
   } finally {
      capture.restore();
   }
});


test('Test_CreateRestaurantClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const restaurant = 'Peaks';
   const startDate = 'a';
   const endDate = 'b';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setRestaurantClosed;
   ConsoleOperationsClient.setRestaurantClosed = async (payload) => payload;

   try {
      RestaurantController.createRestaurantClosedController({ restaurantEl: {} });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: restaurant,
         startDate,
         endDate,
         message,
      });

      assert.deepEqual(payload, {
         restaurant,
         startDate,
         endDate,
         message,
      });
   } finally {
      ConsoleOperationsClient.setRestaurantClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateRestaurantClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const restaurant = 'Peaks';
   const capture = _captureClosedForm();

   try {
      RestaurantController.createRestaurantClosedController({ restaurantEl: {} });
      const status = capture.getCaptured().successMessage({ restaurant });

      assert.equal(status, Strings.status.closed(restaurant));
   } finally {
      capture.restore();
   }
});
