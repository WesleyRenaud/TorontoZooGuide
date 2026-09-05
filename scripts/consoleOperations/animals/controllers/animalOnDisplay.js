import { AnimalViewingScopeControl } from './animalViewingScopeControl.js';
import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { AnimalViewingScope } from '../../../shared/enums/animalViewingScope.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export class AnimalOnDisplay {
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
            species: ControllerUtils.getFieldValue(speciesEl),
            exhibit: ControllerUtils.getFieldValue(exhibitEl),
            viewingScope: ControllerUtils.getFieldValue(viewingScopeEl) || AnimalViewingScope.ALL,
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
         ControllerUtils.resetFormFields(formFieldEls);
         viewingScopeControl.reset();
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
         });
      }

      async function submitOnDisplayStatus({ species, exhibit, viewingScope }) {
         return ConsoleOperationsApi.setAnimalOnDisplay({
            species,
            exhibit,
            viewingScope,
         });
      }

      function handleSubmitSuccess(result) {
         Status.setStatus(
            statusEl,
            APP_STRINGS.status.animalOnDisplay(result),
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
            errorMessage: APP_STRINGS.loadErrors.exhibits,
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
            const result = await submitOnDisplayStatus(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               Status.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(result),
                  'is-error'
               );
            }

         }
         catch(err) {
            Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
         }
      }

      const viewingScopeControl = AnimalViewingScopeControl.createAnimalViewingScopeControl({
         speciesEl,
         exhibitEl,
         viewingScopeEl,
      });

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
