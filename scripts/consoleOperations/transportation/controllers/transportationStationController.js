import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class TransportationStationController {
   static createTransportationStationClosedController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: transportationStationEl,
         loadOptions: ConsoleOptionsLoader.loadTransportationStations,
         populateOptions: ConsoleDropdownPopulator.populateTransportationStationDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setTransportationStationClosed({
            transportationStation: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.transportationStation,
         optionsLabel: Strings.entityLabels.transportationStations,
         successMessage: result => Strings.status.closed(result.transportation_station),
      });
   }
}
