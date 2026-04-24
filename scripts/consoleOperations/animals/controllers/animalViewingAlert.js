import { loadExhibits } from '../../options/loaders.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import { setAnimalViewingAlert } from '../../../api/consoleOperationsApi.js';
import {
   bindResetValueOnChange,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';

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
} = {}) {
   const formFieldEls = [speciesEl, exhibitEl, startDateEl, endDateEl, messageEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getFormValues() {
      return {
         species: getFieldValue(speciesEl),
         exhibit: getFieldValue(exhibitEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
         message: getFieldValue(messageEl),
      };
   }

   function validateForm({
      species,
      exhibit,
      startDate,
      endDate,
      message,
   }) {
      if (!species) {
         return 'Species name is required.';
      }

      if (!exhibit) {
         return 'Exhibit is required.';
      }

      if (!message) {
         return 'Alert message is required.';
      }

      return validateOptionalDateRange(startDate, endDate);
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

   async function submitViewingAlert({
      species,
      exhibit,
      startDate,
      endDate,
      message,
   }) {
      return setAnimalViewingAlert({
         species,
         exhibit,
         alertStartDate: startDate || null,
         alertEndDate: endDate || null,
         message,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.species} in ${result.exhibit} was given a viewing alert.`,
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
         const result = await submitViewingAlert(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
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

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
