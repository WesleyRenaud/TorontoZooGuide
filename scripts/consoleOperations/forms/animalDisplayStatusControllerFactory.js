import { AnimalExhibitAutofillController } from '../animals/controllers/animalExhibitAutofillController.js';
import { AnimalViewingScopeController } from '../animals/controllers/animalViewingScopeController.js';
import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class AnimalDisplayStatusControllerFactory {
   static createAnimalDisplayStatusController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      startDateEl = null,
      endDateEl = null,
      messageEl = null,
      activatePanel,
      submitDisplayStatus,
      successMessage,
      loadExhibits = ConsoleOptionsLoader.loadExhibits,
      loadExhibitsForSpecies = ConsoleOptionsLoader.loadExhibitsForSpecies,
   } = {}) {
      const hasDateRange = Boolean(startDateEl || endDateEl);
      const formFieldEls = [
         speciesEl,
         exhibitEl,
         startDateEl,
         endDateEl,
         messageEl,
      ];
      const viewingScopeControl = AnimalViewingScopeController.createAnimalViewingScopeControl({
         speciesEl,
         exhibitEl,
         viewingScopeEl,
      });


      function getFormValues() {
         return {
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
            viewingScopes: viewingScopeControl.selectedEnclosureNames(),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         };
      }

      function validateForm({
         species,
         exhibit,
         viewingScopes,
         startDate,
         endDate,
      }) {
         if (!species) {
            return Strings.validation.entityRequired(Strings.labels.species);
         }

         if (!exhibit) {
            return Strings.validation.entityRequired(Strings.entityLabels.exhibit);
         }

         if (!viewingScopes.length) {
            return Strings.validation.entityRequired(Strings.labels.viewingScope);
         }

         if (!hasDateRange) {
            return null;
         }

         return ControllerHelper.validateOptionalDateRange(startDate, endDate);
      }

      function clearFields() {
         ControllerHelper.resetFormFields(formFieldEls);
         viewingScopeControl.reset();
      }

      async function resetForm() {
         try {
            await ControllerHelper.reloadOptions({
               loadOptions: loadExhibits,
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

      async function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            successMessage(result),
            'is-success'
         );

         await resetForm();
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: loadExhibits,
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
            const result = await submitDisplayStatus(formValues);

            if (result.success) {
               await handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(result),
                  'is-error'
               );
            }
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
         speciesEl,
         exhibitEl,
         loadExhibits,
         loadExhibitsForSpecies,
         populateExhibits: ConsoleDropdownPopulator.populateExhibitDropdown,
         onUniqueFill: () => viewingScopeControl.refresh(),
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
