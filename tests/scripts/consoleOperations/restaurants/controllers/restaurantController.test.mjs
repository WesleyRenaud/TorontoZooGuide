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


test('Test_CreateRestaurantClosedForSeasonController_TestSubmit_ExpectSeasonPayload', async (t) => {
   const restaurant = 'Africa Restaurant';
   const startDate = '2026-11-02';
   const original = EntityClosedFormController.createEntityClosedFormController;
   const originalSet = ConsoleOperationsClient.setRestaurantClosedForSeason;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setRestaurantClosedForSeason = async (payload) => payload;
   t.after(() => {
      EntityClosedFormController.createEntityClosedFormController = original;
      ConsoleOperationsClient.setRestaurantClosedForSeason = originalSet;
   });

   RestaurantController.createRestaurantClosedForSeasonController({ restaurantEl: { id: 'r' } });
   const payload = await captured.submitClosedStatus({
      entity: restaurant,
      startDate,
      endDate: '',
      message: '',
   });

   assert.deepEqual(payload, {
      restaurant,
      startDate,
      endDate: null,
      message: '',
   });
   assert.equal(
      captured.successMessage({ restaurant }),
      Strings.status.closedForSeason(restaurant),
   );
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestaurants);
});


test('Test_CreateRestaurantOpenForSeasonController_TestSubmit_ExpectSeasonList', async (t) => {
   const restaurant = 'Africa Restaurant';
   const { EntityOpenFormController } = await import(
      '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js'
   );
   const original = EntityOpenFormController.createEntityOpenFormController;
   const originalSet = ConsoleOperationsClient.setRestaurantOpenForSeason;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setRestaurantOpenForSeason = async (payload) => payload;
   t.after(() => {
      EntityOpenFormController.createEntityOpenFormController = original;
      ConsoleOperationsClient.setRestaurantOpenForSeason = originalSet;
   });

   RestaurantController.createRestaurantOpenForSeasonController({ restaurantEl: { id: 'r' } });
   const payload = await captured.submitOpenStatus({ entity: restaurant });

   assert.deepEqual(payload, { restaurant });
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadClosedForSeasonRestaurants);
   assert.equal(
      captured.successMessage({ restaurant }),
      Strings.status.openForSeason(restaurant),
   );
});
