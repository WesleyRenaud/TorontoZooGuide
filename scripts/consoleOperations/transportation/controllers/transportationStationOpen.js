import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class TransportationStationOpen {
   static createTransportationStationOpenController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl: transportationStationEl,
         loadOptions: ConsoleOptionsLoader.loadTransportationStations,
         populateOptions: ConsoleDropdownPopulator.populateTransportationStationDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsApi.setTransportationStationOpen({
            transportationStation: entity,
         }),
         entityLabel: Strings.entityLabels.transportationStation,
         optionsLabel: Strings.entityLabels.transportationStations,
         successMessage: result => Strings.status.open(result.transportation_station),
      });
   }
}
