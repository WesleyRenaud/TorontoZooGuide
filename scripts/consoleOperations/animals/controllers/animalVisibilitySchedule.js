import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';

export class AnimalVisibilitySchedule {
   static createAnimalVisibilityScheduleController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      startDateEl,
      endDateEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      messageEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [
         speciesEl,
         exhibitEl,
         startDateEl,
         endDateEl,
         dailyStartTimeEl,
         dailyEndTimeEl,
         messageEl,
      ];


      function getFormValues() {
         return {
            species: ControllerUtils.getFieldValue(speciesEl),
            exhibit: ControllerUtils.getFieldValue(exhibitEl),
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
            dailyStartTime: ControllerUtils.getFieldValue(dailyStartTimeEl),
            dailyEndTime: ControllerUtils.getFieldValue(dailyEndTimeEl),
            message: ControllerUtils.getFieldValue(messageEl),
         };
      }

      function validateForm({
         species,
         exhibit,
         startDate,
         endDate,
         dailyStartTime,
         dailyEndTime,
      }) {
         if (!species) {
            return Strings.validation.entityRequired(Strings.labels.species);
         }

         if (!exhibit) {
            return Strings.validation.entityRequired(Strings.entityLabels.exhibit);
         }

         if (!dailyStartTime || !dailyEndTime) {
            return Strings.validation.dailyViewingTimes;
         }

         return ControllerUtils.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
         });
      }

      async function submitVisibilitySchedule({
         species,
         exhibit,
         startDate,
         endDate,
         dailyStartTime,
         dailyEndTime,
         message,
      }) {
         return ConsoleOperationsApi.setAnimalVisibilitySchedule({
            species,
            exhibit,
            startDate: startDate || null,
            endDate: endDate || null,
            dailyStartTime,
            dailyEndTime,
            message,
         });
      }

      function handleSubmitSuccess(result) {
         Status.setStatus(
            statusEl,
            `${result.species} in ${result.exhibit} viewing schedule updated.`,
            'is-success'
         );

         resetForm();
      }

      async function show() {
         await ControllerUtils.loadOptionsAndShowPanel({
            statusEl,
            setStatus: Status.setStatus,
            loadOptions: Loaders.loadExhibits,
            populateOptions: Dropdowns.populateExhibitDropdown,
            targetEl: exhibitEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.exhibits,
         });
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         Status.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitVisibilitySchedule(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch(err) {
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      ControllerUtils.bindResetValueOnChange(exhibitEl, speciesEl);

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
