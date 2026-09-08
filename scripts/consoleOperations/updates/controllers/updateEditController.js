import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';
import { UpdateOptions } from './updateOptions.js';

export class UpdateEditController {
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
         ControllerHelper.resetFormFields(formFieldEls);
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
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
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
         ControllerHelper.hideConsolePanel({ panelEl, statusEl, setStatus: ConsoleStatusPresenter.setStatus });
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
            description: ControllerHelper.getFieldValue(descriptionEl),
            type: ControllerHelper.getFieldValue(typeEl),
            endDate: ControllerHelper.getFieldValue(endDateEl) || null,
         };
         const validationError = validateForm(values);

         ConsoleStatusPresenter.setStatus(statusEl, '');

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsClient.editUpdate(values);

            if (result.success) {
               ConsoleStatusPresenter.setStatus(statusEl, Strings.status.updateEdited, 'is-success');
               resetForm();
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);
      updateEl?.addEventListener('change', populateFieldsFromSelectedUpdate);

      return { show, hide };
   }
}
