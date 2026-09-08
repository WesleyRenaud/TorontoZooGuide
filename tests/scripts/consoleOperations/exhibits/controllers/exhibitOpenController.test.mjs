import assert from 'node:assert/strict';
import test from 'node:test';

import { ExhibitOpenController } from '../../../../../scripts/consoleOperations/exhibits/controllers/exhibitOpenController.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateExhibitOpenController_TestWiring_ExpectOpenForm', async () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      ExhibitOpenController.createExhibitOpenController({ exhibitEl: { id: 'exhibit' } });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadExhibits);
      assert.equal(captured.entityLabel, Strings.entityLabels.exhibit);

      const originalSet = ConsoleOperationsClient.setExhibitOpen;
      ConsoleOperationsClient.setExhibitOpen = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitOpenStatus({
               entity: 'Savanna',
               startDate: '2026-06-01',
               endDate: '',
            }),
            { exhibit: 'Savanna', startDate: '2026-06-01', endDate: null }
         );
         assert.equal(
            captured.successMessage({ exhibit: 'Savanna' }),
            Strings.status.explicitlyOpen('Savanna')
         );
      } finally {
         ConsoleOperationsClient.setExhibitOpen = originalSet;
      }
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});
