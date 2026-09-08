import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestaurantClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      RestaurantController.createRestaurantClosedController({ restaurantEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestaurants);
      const originalSet = ConsoleOperationsClient.setRestaurantClosed;
      ConsoleOperationsClient.setRestaurantClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Peaks', startDate: 'a', endDate: 'b', message: 'm' }),
            { restaurant: 'Peaks', startDate: 'a', endDate: 'b', message: 'm' }
         );
         assert.equal(captured.successMessage({ restaurant: 'Peaks' }), Strings.status.closed('Peaks'));
      } finally {
         ConsoleOperationsClient.setRestaurantClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
