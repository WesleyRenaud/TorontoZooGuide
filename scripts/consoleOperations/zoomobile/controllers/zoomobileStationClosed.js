import { setZoomobileStationClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateZoomobileStationDropdown } from '../../options/dropdowns.js';
import { loadZoomobileStations } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createZoomobileStationClosedController({
   zoomobileStationEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: zoomobileStationEl,
      loadOptions: loadZoomobileStations,
      populateOptions: populateZoomobileStationDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setZoomobileStationClosed({
         zoomobileStation: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: APP_STRINGS.entityLabels.zoomobileStation,
      optionsLabel: APP_STRINGS.entityLabels.zoomobileStations,
      successMessage: result => APP_STRINGS.status.closed(result.zoomobile_station),
   });
}
