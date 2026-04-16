import { loadZoomobileStations, setStatus, populateZoomobileStationDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../shared/controllerUtils.js';

export function createZoomobileStationOpenController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   zoomobileStationEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([zoomobileStationEl]);
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadZoomobileStations,
         populateOptions: populateZoomobileStationDropdown,
         targetEl: zoomobileStationEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load zoomobile stations.',
      });
   }

   async function onSubmitClick() {
      const zoomobileStation = zoomobileStationEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!zoomobileStation) {
         setStatus(statusEl, 'Zoomobile station is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-zoomobile-station-open', {
            zoomobileStation
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.zoomobile_station} was set as open.`,
               'is-success'
            );
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
