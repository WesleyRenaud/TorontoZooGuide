import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ExhibitController } from '../../../../../scripts/consoleOperations/exhibits/controllers/exhibitController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
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


test('Test_CreateExhibitClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      ExhibitController.createExhibitClosedController({ exhibitEl: { id: 'e' } });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadExhibits);
   } finally {
      capture.restore();
   }
});


test('Test_CreateExhibitClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const exhibit = 'Savanna';
   const message = 'Maintenance';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setExhibitClosed;
   ConsoleOperationsClient.setExhibitClosed = async (payload) => payload;

   try {
      ExhibitController.createExhibitClosedController({ exhibitEl: { id: 'e' } });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: exhibit,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         exhibit,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setExhibitClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateExhibitClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const exhibit = 'Savanna';
   const capture = _captureClosedForm();

   try {
      ExhibitController.createExhibitClosedController({ exhibitEl: { id: 'e' } });
      const status = capture.getCaptured().successMessage({ exhibit });

      assert.equal(status, Strings.status.closed(exhibit));
   } finally {
      capture.restore();
   }
});
