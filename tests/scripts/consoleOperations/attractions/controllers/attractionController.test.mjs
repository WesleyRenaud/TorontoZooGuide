import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateAttractionClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      AttractionController.createAttractionClosedController({ attractionEl: { id: 'a' } });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadAttractions);

      const originalSet = ConsoleOperationsClient.setAttractionClosed;
      ConsoleOperationsClient.setAttractionClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({
               entity: 'Carousel',
               startDate: '2026-06-01',
               endDate: '',
               message: 'Closed',
            }),
            {
               attraction: 'Carousel',
               startDate: '2026-06-01',
               endDate: null,
               message: 'Closed',
            }
         );
         assert.equal(captured.successMessage({ attraction: 'Carousel' }), Strings.status.closed('Carousel'));
      } finally {
         ConsoleOperationsClient.setAttractionClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
