import { AnimalViewingScopeController } from './animalViewingScopeController.js';
import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class AnimalOnController {
   static createAnimalOnDisplayController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      speciesEl,
      exhibitEl,
      viewingScopeEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [speciesEl, exhibitEl, viewingScopeEl];


      function getFormValues() {
         return {
            species: ControllerHelper.getFieldValue(speciesEl),
            exhibit: ControllerHelper.getFieldValue(exhibitEl),
            viewingScope: ControllerHelper.getFieldValue(viewingScopeEl) || AnimalViewingScope.ALL,
         };
      }

      function validateForm({ species, exhibit }) {
         if (!species) {
            return Strings.validation.entityRequired(Strings.labels.species);
         }

         if (!exhibit) {
            return Strings.validation.entityRequired(Strings.entityLabels.exhibit);
         }

         return null;
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
         viewingScopeControl.reset();
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function submitOnDisplayStatus({ species, exhibit, viewingScope }) {
         return ConsoleOperationsClient.setAnimalOnDisplay({
            species,
            exhibit,
            viewingScope,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.animalOnDisplay(result),
            'is-success'
         );

         resetForm();
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: ConsoleOptionsLoader.loadExhibits,
            populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
            targetEl: exhibitEl,
            resetForm,
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
            const result = await submitOnDisplayStatus(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(result),
                  'is-error'
               );
            }

         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      const viewingScopeControl = AnimalViewingScopeController.createAnimalViewingScopeControl({
         speciesEl,
         exhibitEl,
         viewingScopeEl,
      });

      ControllerHelper.bindResetValueOnChange(exhibitEl, speciesEl);

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
