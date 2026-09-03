import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { populateTransportationStationDropdown } from '../../options/dropdowns.js';
import { loadTransportationStations } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createTransportationStationOpenController({
   transportationStationEl,
   ...controllerOptions
} = {}) {
   return createEntityOpenFormController({
      ...controllerOptions,
      entityEl: transportationStationEl,
      loadOptions: loadTransportationStations,
      populateOptions: populateTransportationStationDropdown,
      submitOpenStatus: ({ entity }) => ConsoleOperationsApi.setTransportationStationOpen({
         transportationStation: entity,
      }),
      entityLabel: APP_STRINGS.entityLabels.transportationStation,
      optionsLabel: APP_STRINGS.entityLabels.transportationStations,
      successMessage: result => APP_STRINGS.status.open(result.transportation_station),
   });
}
