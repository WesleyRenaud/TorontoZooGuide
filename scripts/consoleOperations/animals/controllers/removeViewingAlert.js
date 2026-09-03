import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   bindResetValueOnChange,
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { loadExhibits } from '../../options/loaders.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRemoveViewingAlertController({
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


   function getFormValues() {
      return {
         species: getFieldValue(speciesEl),
         exhibit: getFieldValue(exhibitEl),
      };
   }

   function validateForm({ species, exhibit }) {
      if (!species) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.species);
      }

      if (!exhibit) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.exhibit);
      }

      return null;
   }

   function resetForm() {
      resetFormFields(formFieldEls);
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
         errorMessage: APP_STRINGS.loadErrors.exhibits,
      });
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function submitViewingAlertRemoval({ species, exhibit }) {
      return ConsoleOperationsApi.removeAnimalViewingAlert({
         species,
         exhibit,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `Viewing alert removed for ${result.species} in ${result.exhibit}.`,
         'is-success'
      );

      resetForm();
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
         const result = await submitViewingAlertRemoval(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
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
