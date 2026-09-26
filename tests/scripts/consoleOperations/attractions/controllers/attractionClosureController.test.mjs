import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { AttractionClosureController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionClosureController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
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


test('Test_CreateAttractionClosureOverrideController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      AttractionClosureController.createAttractionClosureOverrideController({ attractionEl: {} });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadAttractions);
   } finally {
      capture.restore();
   }
});


test('Test_CreateAttractionClosureOverrideController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const attraction = 'Carousel';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setAttractionClosureOverride;
   ConsoleOperationsClient.setAttractionClosureOverride = async (payload) => payload;

   try {
      AttractionClosureController.createAttractionClosureOverrideController({ attractionEl: {} });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: attraction,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         attraction,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setAttractionClosureOverride = originalSet;
      capture.restore();
   }
});


test('Test_CreateAttractionClosureOverrideController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const attraction = 'Carousel';
   const capture = _captureClosedForm();

   try {
      AttractionClosureController.createAttractionClosureOverrideController({ attractionEl: {} });
      const status = capture.getCaptured().successMessage({ attraction });

      assert.equal(status, Strings.status.closureOverrideSaved(attraction));
   } finally {
      capture.restore();
   }
});
