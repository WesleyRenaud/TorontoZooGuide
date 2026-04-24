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
   const formFieldEls = [speciesEl, exhibitEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getFormValues() {
      return {
         species: getFieldValue(speciesEl),
         exhibit: getFieldValue(exhibitEl),
      };
   }

   function validateForm({ species, exhibit }) {
      if (!species) {
         return 'Species name is required.';
      }

      if (!exhibit) {
         return 'Exhibit is required.';
      }

      return null;
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function submitOnDisplayStatus({ species, exhibit }) {
      return setAnimalOnDisplay({
         species,
         exhibit,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.species} in ${result.exhibit} was set as on display.`,
         'is-success'
      );

      resetForm();
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
      const formValues = getFormValues();

      setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await submitOnDisplayStatus(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
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
