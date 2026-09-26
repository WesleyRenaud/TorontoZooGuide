import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { TransportationStationController } from '../../../../../scripts/consoleOperations/transportation/controllers/transportationStationController.js';
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


test('Test_CreateTransportationStationClosedController_TestWiring_ExpectLoadOptions', () => {
   const capture = _captureClosedForm();

   try {
      TransportationStationController.createTransportationStationClosedController({
         transportationStationEl: {},
      });

      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadTransportationStations);
   } finally {
      capture.restore();
   }
});


test('Test_CreateTransportationStationClosedController_TestSubmitClosedStatus_ExpectPayload', async () => {
   const station = 'Hub';
   const message = 'm';
   const capture = _captureClosedForm();
   const originalSet = ConsoleOperationsClient.setTransportationStationClosed;
   ConsoleOperationsClient.setTransportationStationClosed = async (payload) => payload;

   try {
      TransportationStationController.createTransportationStationClosedController({
         transportationStationEl: {},
      });
      const payload = await capture.getCaptured().submitClosedStatus({
         entity: station,
         startDate: '',
         endDate: '',
         message,
      });

      assert.deepEqual(payload, {
         transportationStation: station,
         startDate: null,
         endDate: null,
         message,
      });
   } finally {
      ConsoleOperationsClient.setTransportationStationClosed = originalSet;
      capture.restore();
   }
});


test('Test_CreateTransportationStationClosedController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const station = 'Hub';
   const capture = _captureClosedForm();

   try {
      TransportationStationController.createTransportationStationClosedController({
         transportationStationEl: {},
      });
      const status = capture.getCaptured().successMessage({ transportation_station: station });

      assert.equal(status, Strings.status.closed(station));
   } finally {
      capture.restore();
   }
});
