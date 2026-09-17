import { AnimalExhibitAutofillController } from './animalExhibitAutofillController.js';
import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class AnimalVisibilityController {
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
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            dailyStartTime: ControllerHelper.getFieldValue(dailyStartTimeEl),
            dailyEndTime: ControllerHelper.getFieldValue(dailyEndTimeEl),
            message: ControllerHelper.getFieldValue(messageEl),
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

         return ControllerHelper.validateOptionalDateRange(startDate, endDate);
      }

      function clearFields() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      async function resetForm() {
         try {
            await ControllerHelper.reloadOptions({
               loadOptions: ConsoleOptionsLoader.loadExhibits,
               populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
               targetEl: exhibitEl,
               resetForm: clearFields,
            });
         }
         catch (err) {
            clearFields();
         }
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
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
         return ConsoleOperationsClient.setAnimalVisibilitySchedule({
            species,
            exhibit,
            startDate: startDate || null,
            endDate: endDate || null,
            dailyStartTime,
            dailyEndTime,
            message,
         });
      }

      async function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.animalVisibilityScheduleSaved(result),
            'is-success'
         );

         await resetForm();
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: ConsoleOptionsLoader.loadExhibits,
            populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
            targetEl: exhibitEl,
            resetForm: clearFields,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.exhibits,
         });
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         ConsoleStatusPresenter.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitVisibilitySchedule(formValues);

            if (result.success) {
               await handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      ControllerHelper.bindResetValueOnChange(exhibitEl, speciesEl);
      AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
         speciesEl,
         exhibitEl,
         loadExhibits: ConsoleOptionsLoader.loadExhibits,
         loadExhibitsForSpecies: ConsoleOptionsLoader.loadExhibitsForSpecies,
         populateExhibits: ConsoleDropdownPopulator.populateExhibitDropdown,
      });

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
