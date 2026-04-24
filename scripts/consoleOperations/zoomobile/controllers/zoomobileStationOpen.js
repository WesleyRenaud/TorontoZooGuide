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
      entityLabel: 'Zoomobile station',
      optionsLabel: 'zoomobile stations',
      successMessage: result => `${result.zoomobile_station} was set as open.`,
   });
}
