import assert from 'node:assert/strict';
import test from 'node:test';

import { RestroomOpenController } from '../../../../../scripts/consoleOperations/restrooms/controllers/restroomOpenController.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateRestroomOpenController_TestWiring_ExpectOpenForm', async () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      RestroomOpenController.createRestroomOpenController({ restroomEl: { id: 'rr' } });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadRestrooms);

      const originalSet = ConsoleOperationsClient.setRestroomOpen;
      ConsoleOperationsClient.setRestroomOpen = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitOpenStatus({ entity: 'Near Cafe', startDate: '', endDate: '2026-07-01' }),
            { restroom: 'Near Cafe', startDate: null, endDate: '2026-07-01' }
         );
         assert.equal(
            captured.successMessage({ restroom: 'Near Cafe' }),
            Strings.status.explicitlyOpen('Near Cafe')
         );
      } finally {
         ConsoleOperationsClient.setRestroomOpen = originalSet;
      }
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});
