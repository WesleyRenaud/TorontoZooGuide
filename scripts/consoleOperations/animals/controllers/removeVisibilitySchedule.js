import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';

export class RemoveVisibilitySchedule {
   static createRemoveVisibilityScheduleController({
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
            species: ControllerUtils.getFieldValue(speciesEl),
            exhibit: ControllerUtils.getFieldValue(exhibitEl),
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
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
         });
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

      async function submitVisibilityScheduleRemoval({ species, exhibit }) {
         return ConsoleOperationsApi.removeAnimalVisibilitySchedule({
            species,
            exhibit,
         });
      }

      function handleSubmitSuccess(result) {
         Status.setStatus(
            statusEl,
            `${result.species} in ${result.exhibit} no longer has a visibility schedule.`,
            'is-success'
         );

         resetForm();
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
            const result = await submitVisibilityScheduleRemoval(formValues);

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
