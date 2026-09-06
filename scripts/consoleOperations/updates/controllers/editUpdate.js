import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';
import { UpdateOptions } from './updateOptions.js';

export class EditUpdate {
   static createEditUpdateController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      updateEl,
      descriptionEl,
      typeEl,
      endDateEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [updateEl, descriptionEl, typeEl, endDateEl];


      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function setFieldValue(fieldEl, value) {
         if (!fieldEl || !('value' in fieldEl)) {
            return;
         }

         fieldEl.value = value || '';
      }

      function populateFieldsFromSelectedUpdate() {
         const selectedUpdate = UpdateOptions.getSelectedUpdateData(updateEl);

         setFieldValue(descriptionEl, selectedUpdate.description);
         setFieldValue(typeEl, selectedUpdate.type);
         setFieldValue(endDateEl, selectedUpdate.endDate);
      }

      async function show() {
         await ControllerUtils.loadOptionsAndShowPanel({
            statusEl,
            setStatus: Status.setStatus,
            loadOptions: UpdateOptions.loadActiveUpdates,
            populateOptions: UpdateOptions.populateUpdateDropdown,
            targetEl: updateEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.updates,
         });
      }

      function hide() {
         ControllerUtils.hideConsolePanel({ panelEl, statusEl, setStatus: Status.setStatus });
      }

      function validateForm({
         title,
         startDate,
         description,
         type,
         endDate,
      }) {
         if (!title || !startDate) return Strings.validation.entityRequired(Strings.labels.update);
         if (!description) return Strings.validation.entityRequired(Strings.labels.description);
         if (!type) return Strings.validation.entityRequired(Strings.labels.type);

         if (endDate && new Date(endDate).getTime() < new Date(startDate).getTime()) {
            return Strings.validation.endDateBeforeStartDate;
         }

         return null;
      }

      async function onSubmitClick() {
         const selectedUpdate = UpdateOptions.getSelectedUpdateData(updateEl);
         const values = {
            title: selectedUpdate.title,
            startDate: selectedUpdate.startDate,
            description: ControllerUtils.getFieldValue(descriptionEl),
            type: ControllerUtils.getFieldValue(typeEl),
            endDate: ControllerUtils.getFieldValue(endDateEl) || null,
         };
         const validationError = validateForm(values);

         Status.setStatus(statusEl, '');

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.editUpdate(values);

            if (result.success) {
               Status.setStatus(statusEl, Strings.status.updateEdited, 'is-success');
               resetForm();
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);
      updateEl?.addEventListener('change', populateFieldsFromSelectedUpdate);

      return { show, hide };
   }
}
