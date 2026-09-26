import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { RestroomClosedController } from '../../../../../scripts/consoleOperations/restrooms/controllers/restroomClosedController.js';
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


test('Test_CreateRestroomClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      RestroomClosedController.createRestroomClosedController({ restroomEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadRestrooms);
   } finally {
      capture.restore();
   }
});


test('Test_CreateRestroomClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const restroom = 'RR1';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setRestroomClosed;
   ConsoleOperationsClient.setRestroomClosed = async (payload) => payload;

   try {
      RestroomClosedController.createRestroomClosedController({ restroomEl: {} });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: restroom,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         restroom,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setRestroomClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateRestroomClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const restroom = 'RR1';
   const capture = _captureClosedForm();

   try {
      RestroomClosedController.createRestroomClosedController({ restroomEl: {} });
      const status = capture.getCaptured().successMessage({ restroom });

      assert.equal(status, Strings.status.closed(restroom));
   } finally {
      capture.restore();
   }
});
