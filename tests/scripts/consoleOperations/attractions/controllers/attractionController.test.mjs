import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { AttractionController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionController.js';
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


test('Test_CreateAttractionClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      AttractionController.createAttractionClosedController({ attractionEl: { id: 'a' } });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadAttractions);
   } finally {
      capture.restore();
   }
});


test('Test_CreateAttractionClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const attraction = 'Carousel';
   const startDate = '2026-06-01';
   const message = 'Closed';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setAttractionClosed;
   ConsoleOperationsClient.setAttractionClosed = async (payload) => payload;

   try {
      AttractionController.createAttractionClosedController({ attractionEl: { id: 'a' } });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: attraction,
         startDate,
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         attraction,
         startDate,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setAttractionClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateAttractionClosedForSeasonController_TestSubmit_ExpectSeasonPayload', async (t) => {
   const attraction = 'Carousel';
   const startDate = '2026-11-02';
   const original = EntityClosedFormController.createEntityClosedFormController;
   const originalSet = ConsoleOperationsClient.setAttractionClosedForSeason;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setAttractionClosedForSeason = async (payload) => payload;
   t.after(() => {
      EntityClosedFormController.createEntityClosedFormController = original;
      ConsoleOperationsClient.setAttractionClosedForSeason = originalSet;
   });

   AttractionController.createAttractionClosedForSeasonController({ attractionEl: { id: 'a' } });
   const payload = await captured.submitClosedStatus({
      entity: attraction,
      startDate,
      endDate: '',
      message: '',
   });

   assert.deepEqual(payload, {
      attraction,
      startDate,
      endDate: null,
      message: '',
   });
   assert.equal(
      captured.successMessage({ attraction }),
      Strings.status.closedForSeason(attraction),
   );
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadAttractions);
});


test('Test_CreateAttractionOpenForSeasonController_TestSubmit_ExpectSeasonList', async (t) => {
   const attraction = 'Carousel';
   const { EntityOpenFormController } = await import(
      '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js'
   );
   const original = EntityOpenFormController.createEntityOpenFormController;
   const originalSet = ConsoleOperationsClient.setAttractionOpenForSeason;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };
   ConsoleOperationsClient.setAttractionOpenForSeason = async (payload) => payload;
   t.after(() => {
      EntityOpenFormController.createEntityOpenFormController = original;
      ConsoleOperationsClient.setAttractionOpenForSeason = originalSet;
   });

   AttractionController.createAttractionOpenForSeasonController({ attractionEl: { id: 'a' } });
   const payload = await captured.submitOpenStatus({ entity: attraction });

   assert.deepEqual(payload, { attraction });
   assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadClosedForSeasonAttractions);
   assert.equal(
      captured.successMessage({ attraction }),
      Strings.status.openForSeason(attraction),
   );
});


test('Test_CreateAttractionClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const attraction = 'Carousel';
   const capture = _captureClosedForm();

   try {
      AttractionController.createAttractionClosedController({ attractionEl: { id: 'a' } });
      const status = capture.getCaptured().successMessage({ attraction });

      assert.equal(status, Strings.status.closed(attraction));
   } finally {
      capture.restore();
   }
});
