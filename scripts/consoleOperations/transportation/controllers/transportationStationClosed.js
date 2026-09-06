import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class TransportationStationClosed {
   static createTransportationStationClosedController({
      transportationStationEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: transportationStationEl,
         loadOptions: Loaders.loadTransportationStations,
         populateOptions: Dropdowns.populateTransportationStationDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setTransportationStationClosed({
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
