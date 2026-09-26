import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { RestroomOpenController } from '../../../../../scripts/consoleOperations/restrooms/controllers/restroomOpenController.js';
import { Strings } from '../../../../../scripts/strings.js';


function _captureOpenForm() {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };
   return {
      getCaptured: () => captured,
      restore: () => {
         EntityOpenFormController.createEntityOpenFormController = original;
      },
   };
}


test('Test_CreateRestroomOpenController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureOpenForm();

   try {
      RestroomOpenController.createRestroomOpenController({ restroomEl: { id: 'rr' } });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadClosedRestrooms);
   } finally {
      capture.restore();
   }
});


test('Test_CreateRestroomOpenController_TestSubmitOpenStatus_ExpectPayload', async () => {
   const restroom = 'Near Cafe';
   const endDate = '2026-07-01';
   const capture = _captureOpenForm();
   const originalSet = ConsoleOperationsClient.setRestroomOpen;
   ConsoleOperationsClient.setRestroomOpen = async (payload) => payload;

   try {
      RestroomOpenController.createRestroomOpenController({ restroomEl: { id: 'rr' } });
      const payload = await capture.getCaptured().submitOpenStatus({
         entity: restroom,
         startDate: '',
         endDate,
      });

      assert.deepEqual(payload, {
         restroom,
         startDate: null,
         endDate,
      });
   } finally {
      ConsoleOperationsClient.setRestroomOpen = originalSet;
      capture.restore();
   }
});


test('Test_CreateRestroomOpenController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const restroom = 'Near Cafe';
   const capture = _captureOpenForm();

   try {
      RestroomOpenController.createRestroomOpenController({ restroomEl: { id: 'rr' } });
      const message = capture.getCaptured().successMessage({ restroom });

      assert.equal(message, Strings.status.explicitlyOpen(restroom));
   } finally {
      capture.restore();
   }
});
