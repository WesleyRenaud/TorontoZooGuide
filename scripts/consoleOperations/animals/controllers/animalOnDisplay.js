import { loadExhibits } from '../../options/loaders.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import { setAnimalOnDisplay } from '../../../api/consoleOperationsApi.js';
import {
   bindResetValueOnChange,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';

export function createAnimalOnDisplayController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   speciesEl,
   exhibitEl,
   activatePanel,
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

   async function show() {
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
         const result = await setAnimalOnDisplay({
            species,
            exhibit
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.species} in ${result.exhibit} was set as on display.`,
               'is-success'
            );
            resetForm();
         }
         else {
            setStatus(
               statusEl,
               result.error || 'Failed.',
               'is-error'
            );
         }

      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   bindResetValueOnChange(exhibitEl, speciesEl);

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
