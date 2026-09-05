import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

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
         entityLabel: APP_STRINGS.entityLabels.transportationStation,
         optionsLabel: APP_STRINGS.entityLabels.transportationStations,
         successMessage: result => APP_STRINGS.status.closed(result.transportation_station),
      });
   }
}
