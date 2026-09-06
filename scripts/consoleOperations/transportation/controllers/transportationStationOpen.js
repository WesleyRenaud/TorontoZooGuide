import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class TransportationStationOpen {
   static createTransportationStationOpenController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl: transportationStationEl,
         loadOptions: Loaders.loadTransportationStations,
         populateOptions: Dropdowns.populateTransportationStationDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsApi.setTransportationStationOpen({
            transportationStation: entity,
         }),
         entityLabel: Strings.entityLabels.transportationStation,
         optionsLabel: Strings.entityLabels.transportationStations,
         successMessage: result => Strings.status.open(result.transportation_station),
      });
   }
}
