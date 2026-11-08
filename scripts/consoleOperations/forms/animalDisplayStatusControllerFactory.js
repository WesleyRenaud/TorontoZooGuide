import { AnimalExhibitAutofillController } from '../animals/controllers/animalExhibitAutofillController.js';
import { AnimalViewingScopeController } from '../animals/controllers/animalViewingScopeController.js';
import { AnimalsClient } from '../../api/animalsClient.js';
import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';
import { UpdateOptions } from '../updates/controllers/updateOptions.js';

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
      closureUpdateEl,
      activatePanel,
      submitDisplayStatus,
      successMessage,
      loadExhibits = ConsoleOptionsLoader.loadExhibits,
      loadExhibitsForSpecies = ConsoleOptionsLoader.loadExhibitsForSpecies,
      loadViewingScopes = AnimalsClient.getAnimalViewingScopes,
      loadAnimalViewingScopes = loadViewingScopes,
   } = {}) {
      const hasDateRange = Boolean(startDateEl || endDateEl);
      const formFieldEls = [
         speciesEl,
         exhibitEl,
         closureUpdateEl,
         startDateEl,
         endDateEl,
         messageEl,
      ];
      const viewingScopeControl = AnimalViewingScopeController.createAnimalViewingScopeControl({
         speciesEl,
         exhibitEl,
         viewingScopeEl,
         loadViewingScopes,
         loadAnimalViewingScopes,
      });


      function getFormValues() {
         const formValues = {
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
            viewingScopes: viewingScopeControl.selectedEnclosureNames(),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         };

         if (closureUpdateEl) {
            const closureUpdate = UpdateOptions.getSelectedUpdateIdentity(closureUpdateEl);
            formValues.closureUpdateTitle = closureUpdate.title || null;
            formValues.closureUpdateStartDate = closureUpdate.startDate || null;
         }

         return formValues;
      }

      function enableDateFields() {
         if (startDateEl) {
            startDateEl.disabled = false;
         }

         if (endDateEl) {
            endDateEl.disabled = false;
         }
      }

      function applyClosureUpdateDates() {
         const closureUpdate = UpdateOptions.getSelectedUpdateData(closureUpdateEl);
         const linked = Boolean(closureUpdate.title);

         if (startDateEl) {
            startDateEl.disabled = linked;
            startDateEl.value = linked ? closureUpdate.startDate : '';
         }

         if (endDateEl) {
            endDateEl.disabled = linked;
            endDateEl.value = linked ? closureUpdate.endDate : '';
         }
      }

      async function refreshClosureUpdates() {
         if (!closureUpdateEl) {
            return;
         }

         enableDateFields();
         const updates = await UpdateOptions.loadActiveUpdates();
         UpdateOptions.populateClosureUpdateDropdown(closureUpdateEl, updates);
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
         enableDateFields();
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

         try {
            await refreshClosureUpdates();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.loadErrors.updates, 'is-error');
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

         try {
            await refreshClosureUpdates();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.loadErrors.updates, 'is-error');
         }
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

      closureUpdateEl?.addEventListener('change', applyClosureUpdateDates);
      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
