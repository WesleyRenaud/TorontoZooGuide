import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomClosedController } from '../../../../../scripts/consoleOperations/restrooms/controllers/restroomClosedController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestroomClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      RestroomClosedController.createRestroomClosedController({ restroomEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestrooms);
      const originalSet = ConsoleOperationsClient.setRestroomClosed;
      ConsoleOperationsClient.setRestroomClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'RR1', startDate: '', endDate: '', message: 'm' }),
            { restroom: 'RR1', startDate: null, endDate: null, message: 'm' }
         );
         assert.equal(captured.successMessage({ restroom: 'RR1' }), Strings.status.closed('RR1'));
      } finally {
         ConsoleOperationsClient.setRestroomClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
