import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class TransportationStationOpenController {
   static createTransportationStationOpenController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: transportationStationEl,
         loadOptions: ConsoleOptionsLoader.loadTransportationStations,
         populateOptions: ConsoleDropdownPopulator.populateTransportationStationDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsClient.setTransportationStationOpen({
            transportationStation: entity,
         }),
         entityLabel: Strings.entityLabels.transportationStation,
         optionsLabel: Strings.entityLabels.transportationStations,
         successMessage: result => Strings.status.open(result.transportation_station),
      });
   }
}
