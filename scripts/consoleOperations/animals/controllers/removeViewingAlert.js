import { loadExhibits, setStatus, populateExhibitDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   bindResetValueOnChange,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../shared/controllerUtils.js';

export function createRemoveViewingAlertController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   speciesEl,
   exhibitEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([speciesEl, exhibitEl]);
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

      setStatus(statusEl, '');

      if (!species) {
         setStatus(statusEl, 'Species name is required.', 'is-error');
         return;
      }

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/remove-animal-viewing-alert', {
            species,
            exhibit
         });

         if (result.success) {

            setStatus(
               statusEl,
               `Viewing alert removed for ${result.species} in ${result.exhibit}.`,
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
      hide,
   };
}
