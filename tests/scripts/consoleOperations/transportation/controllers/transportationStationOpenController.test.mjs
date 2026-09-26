import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { TransportationStationOpenController } from '../../../../../scripts/consoleOperations/transportation/controllers/transportationStationOpenController.js';
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


test('Test_CreateTransportationStationOpenController_TestWiring_ExpectOpenForm', () => {
   const entityEl = { id: 'station' };
   const extra = 1;
   const capture = _captureOpenForm();

   try {
      const created = TransportationStationOpenController.createTransportationStationOpenController({
         transportationStationEl: entityEl,
         extra,
      });

      assert.deepEqual(created, { created: true });
      assert.equal(capture.getCaptured().entityEl, entityEl);
      assert.equal(capture.getCaptured().extra, extra);
      assert.equal(capture.getCaptured().loadOptions, ConsoleOptionsLoader.loadClosedTransportationStations);
      assert.equal(capture.getCaptured().populateOptions, ConsoleDropdownPopulator.populateTransportationStationDropdown);
      assert.equal(capture.getCaptured().entityLabel, Strings.entityLabels.transportationStation);
   } finally {
      capture.restore();
   }
});


test('Test_CreateTransportationStationOpenController_TestSubmitOpenStatus_ExpectPayload', async () => {
   const station = 'Main Station';
   const capture = _captureOpenForm();
   const originalSet = ConsoleOperationsClient.setTransportationStationOpen;
   ConsoleOperationsClient.setTransportationStationOpen = async (payload) => payload;

   try {
      TransportationStationOpenController.createTransportationStationOpenController({
         transportationStationEl: { id: 'station' },
      });
      const payload = await capture.getCaptured().submitOpenStatus({ entity: station });

      assert.deepEqual(payload, { transportationStation: station });
   } finally {
      ConsoleOperationsClient.setTransportationStationOpen = originalSet;
      capture.restore();
   }
});


test('Test_CreateTransportationStationOpenController_TestSuccessMessage_ExpectCatalogMessage', () => {
   const station = 'Main Station';
   const capture = _captureOpenForm();

   try {
      TransportationStationOpenController.createTransportationStationOpenController({
         transportationStationEl: { id: 'station' },
      });
      const status = capture.getCaptured().successMessage({ transportation_station: station });

      assert.equal(status, Strings.status.open(station));
   } finally {
      capture.restore();
   }
});
