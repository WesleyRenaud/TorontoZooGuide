import { loadExhibits, setStatus, populateExhibitDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   bindResetValueOnChange,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

export function createAnimalViewingAlertController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   speciesEl,
   exhibitEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([speciesEl, exhibitEl, startDateEl, endDateEl, messageEl]);
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
         loadOptions: loadExhibits,
         populateOptions: populateExhibitDropdown,
         targetEl: exhibitEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load exhibits.',
      });
   }

   async function onSubmitClick() {
      const species = speciesEl?.value.trim() ?? '';
      const exhibit = exhibitEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!species) {
         setStatus(statusEl, 'Species name is required.', 'is-error');
         return;
      }

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      if (!message) {
         setStatus(statusEl, 'Alert message is required.', 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-animal-viewing-alert', {
            species,
            exhibit,
            alertStartDate: startDate || null,
            alertEndDate: endDate || null,
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.species} in ${result.exhibit} was given a viewing alert.`,
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

   bindResetValueOnChange(exhibitEl, speciesEl);

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
