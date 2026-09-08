import assert from 'node:assert/strict';
import test from 'node:test';

import { RestaurantClosureController } from '../../../../../scripts/consoleOperations/restaurants/controllers/restaurantClosureController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestaurantClosureOverrideController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      RestaurantClosureController.createRestaurantClosureOverrideController({ restaurantEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestaurants);
      assert.equal(captured.entityLabel, Strings.entityLabels.restaurant);

      const originalSet = ConsoleOperationsClient.setRestaurantClosureOverride;
      ConsoleOperationsClient.setRestaurantClosureOverride = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Peaks', startDate: '', endDate: '', message: 'm' }),
            { restaurant: 'Peaks', startDate: null, endDate: null, message: 'm' }
         );
         assert.equal(
            captured.successMessage({ restaurant: 'Peaks' }),
            Strings.status.closureOverrideSaved('Peaks')
         );
      } finally {
         ConsoleOperationsClient.setRestaurantClosureOverride = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
