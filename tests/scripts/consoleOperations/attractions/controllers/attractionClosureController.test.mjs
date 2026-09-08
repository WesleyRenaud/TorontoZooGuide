import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionClosureController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionClosureController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateAttractionClosureOverrideController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      AttractionClosureController.createAttractionClosureOverrideController({ attractionEl: {} });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadAttractions);
      const originalSet = ConsoleOperationsClient.setAttractionClosureOverride;
      ConsoleOperationsClient.setAttractionClosureOverride = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Carousel', startDate: '', endDate: '', message: 'm' }),
            { attraction: 'Carousel', startDate: null, endDate: null, message: 'm' }
         );
         assert.equal(
            captured.successMessage({ attraction: 'Carousel' }),
            Strings.status.closureOverrideSaved('Carousel')
         );
      } finally {
         ConsoleOperationsClient.setAttractionClosureOverride = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
