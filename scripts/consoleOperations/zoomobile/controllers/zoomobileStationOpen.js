import { APP_STRINGS } from '../../../strings.js';
import { loadZoomobileStations } from '../../options/loaders.js';
import { populateZoomobileStationDropdown } from '../../options/dropdowns.js';
import { setZoomobileStationOpen } from '../../../api/consoleOperationsApi.js';
import { createEntityOpenFormController } from '../../forms/entityOpenFormController.js';

export function createZoomobileStationOpenController({
   zoomobileStationEl,
   ...controllerOptions
} = {}) {
   return createEntityOpenFormController({
      ...controllerOptions,
      entityEl: zoomobileStationEl,
      loadOptions: loadZoomobileStations,
      populateOptions: populateZoomobileStationDropdown,
      submitOpenStatus: ({ entity }) => setZoomobileStationOpen({
         zoomobileStation: entity,
      }),
      entityLabel: APP_STRINGS.entityLabels.zoomobileStation,
      optionsLabel: APP_STRINGS.entityLabels.zoomobileStations,
      successMessage: result => APP_STRINGS.status.open(result.zoomobile_station),
   });
}
