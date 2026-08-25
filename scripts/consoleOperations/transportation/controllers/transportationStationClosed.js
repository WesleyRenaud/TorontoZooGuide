import { setTransportationStationClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateTransportationStationDropdown } from '../../options/dropdowns.js';
import { loadTransportationStations } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createTransportationStationClosedController({
   transportationStationEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: transportationStationEl,
      loadOptions: loadTransportationStations,
      populateOptions: populateTransportationStationDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setTransportationStationClosed({
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
