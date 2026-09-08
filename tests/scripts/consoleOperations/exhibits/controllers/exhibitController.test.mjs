import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitController } from '../../../../../scripts/consoleOperations/exhibits/controllers/exhibitController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateExhibitClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      ExhibitController.createExhibitClosedController({ exhibitEl: { id: 'e' } });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadExhibits);

      const originalSet = ConsoleOperationsClient.setExhibitClosed;
      ConsoleOperationsClient.setExhibitClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({
               entity: 'Savanna',
               startDate: '',
               endDate: '',
               message: 'Maintenance',
            }),
            {
               exhibit: 'Savanna',
               startDate: null,
               endDate: null,
               message: 'Maintenance',
            }
         );
         assert.equal(captured.successMessage({ exhibit: 'Savanna' }), Strings.status.closed('Savanna'));
      } finally {
         ConsoleOperationsClient.setExhibitClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
