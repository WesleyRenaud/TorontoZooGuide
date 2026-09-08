import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationController } from '../../../../../scripts/consoleOperations/transportation/controllers/transportationStationController.js';
import { EntityClosedFormController } from '../../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateTransportationStationClosedController_TestWiring_ExpectClosedForm', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;
   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      TransportationStationController.createTransportationStationClosedController({
         transportationStationEl: {},
      });
      assert.equal(captured.loadOptions, ConsoleOptionsLoader.loadTransportationStations);
      const originalSet = ConsoleOperationsClient.setTransportationStationClosed;
      ConsoleOperationsClient.setTransportationStationClosed = async (payload) => payload;
      try {
         assert.deepEqual(
            await captured.submitClosedStatus({ entity: 'Hub', startDate: '', endDate: '', message: 'm' }),
            { transportationStation: 'Hub', startDate: null, endDate: null, message: 'm' }
         );
         assert.equal(
            captured.successMessage({ transportation_station: 'Hub' }),
            Strings.status.closed('Hub')
         );
      } finally {
         ConsoleOperationsClient.setTransportationStationClosed = originalSet;
      }
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
