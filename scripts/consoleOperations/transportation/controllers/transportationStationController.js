import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class TransportationStationController {
   static createTransportationStationClosedController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedControllerFactory.createEntityClosedController({
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
         resultName: result => result.transportation_station,
      });
   }
}
