import { setAnimalViewingAlert } from '../../../api/consoleOperationsApi.js';
import {
   bindResetValueOnChange,
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { loadExhibits } from '../../options/loaders.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

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
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.species);
      }

      if (!exhibit) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.exhibit);
      }

      if (!message) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.alertMessage);
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
         errorMessage: APP_STRINGS.loadErrors.exhibits,
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
