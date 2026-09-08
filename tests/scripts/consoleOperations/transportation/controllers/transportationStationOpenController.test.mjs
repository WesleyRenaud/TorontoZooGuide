import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationOpenController } from '../../../../../scripts/consoleOperations/transportation/controllers/transportationStationOpenController.js';
import { EntityOpenFormController } from '../../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleDropdownPopulator } from '../../../../../scripts/consoleOperations/options/consoleDropdownPopulator.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateTransportationStationOpenController_TestWiring_ExpectOpenForm', async () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;
   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      const entityEl = { id: 'station' };
      assert.deepEqual(
         TransportationStationOpenController.createTransportationStationOpenController({
            transportationStationEl: entityEl,
            extra: 1,
         }),
         { created: true }
      );
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.extra, 1);
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadTransportationStations);
      assert.equal(captured.populateOptions, ConsoleDropdownPopulator.populateTransportationStationDropdown);
      assert.equal(captured.entityLabel, Strings.entityLabels.transportationStation);

      const originalSet = ConsoleOperationsClient.setTransportationStationOpen;
      ConsoleOperationsClient.setTransportationStationOpen = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitOpenStatus({ entity: 'Main Station' }),
            { transportationStation: 'Main Station' }
         );
         assert.equal(captured.successMessage({ transportation_station: 'Main Station' }), Strings.status.open('Main Station'));
      } finally {
         ConsoleOperationsClient.setTransportationStationOpen = originalSet;
      }
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});
