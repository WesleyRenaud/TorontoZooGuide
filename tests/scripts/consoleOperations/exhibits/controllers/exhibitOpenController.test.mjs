import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { ExhibitOpenController } from '../../../../../scripts/consoleOperations/exhibits/controllers/exhibitOpenController.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
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


test('Test_CreateExhibitOpenController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureOpenForm();

   try {
      ExhibitOpenController.createExhibitOpenController({ exhibitEl: { id: 'exhibit' } });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadClosedExhibits);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.exhibit);
   } finally {
      capture.restore();
   }
});


test('Test_CreateExhibitOpenController_TestSubmitOpenStatus_ExpectPayload', async () => {
   const exhibit = 'Savanna';
   const startDate = '2026-06-01';
   const capture = _captureOpenForm();
   const originalSet = ConsoleOperationsClient.setExhibitOpen;
   ConsoleOperationsClient.setExhibitOpen = async (payload) => payload;

   try {
      ExhibitOpenController.createExhibitOpenController({ exhibitEl: { id: 'exhibit' } });
      const payload = await capture.getCaptured().submitOpenStatus({
         entity: exhibit,
         startDate,
         endDate: '',
      });

      assert.deepEqual(payload, {
         exhibit,
         startDate,
         endDate: null,
      });
   } finally {
      ConsoleOperationsClient.setExhibitOpen = originalSet;
      capture.restore();
   }
});


test('Test_CreateExhibitOpenController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const exhibit = 'Savanna';
   const capture = _captureOpenForm();

   try {
      ExhibitOpenController.createExhibitOpenController({ exhibitEl: { id: 'exhibit' } });
      const message = capture.getCaptured().successMessage({ exhibit });

      assert.equal(message, Strings.status.explicitlyOpen(exhibit));
   } finally {
      capture.restore();
   }
});
