import { removeAnimalVisibilitySchedule } from '../../../api/consoleOperationsApi.js';
import {
   bindResetValueOnChange,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { loadExhibits } from '../../options/loaders.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRemoveVisibilityScheduleController({
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
         errorMessage: APP_STRINGS.loadErrors.exhibits,
      });
   }

   async function submitVisibilityScheduleRemoval({ species, exhibit }) {
      return removeAnimalVisibilitySchedule({
         species,
         exhibit,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.species} in ${result.exhibit} no longer has a visibility schedule.`,
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
         const result = await submitVisibilityScheduleRemoval(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
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
