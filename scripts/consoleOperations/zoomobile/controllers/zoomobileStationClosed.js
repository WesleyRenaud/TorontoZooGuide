import { loadZoomobileStations } from '../../options/loaders.js';
import { populateZoomobileStationDropdown } from '../../options/dropdowns.js';
import { setZoomobileStationClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

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
      entityLabel: 'Zoomobile station',
      optionsLabel: 'zoomobile stations',
      successMessage: result => `${result.zoomobile_station} was set as closed.`,
   });
}
