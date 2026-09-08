import { ValueNormalizer } from '../../api/valueNormalizer.js';
import { PanelNavigator } from '../shell/panelNavigator.js';
import { Strings } from '../../strings.js';
import { VisitDateValidator } from '../../visitDates/visitDateValidator.js';

export class ControllerHelper {
   static resetFieldValue(fieldEl) {
      if (!fieldEl) {
         return;
      }

      if (fieldEl.type === 'checkbox' || fieldEl.type === 'radio') {
         fieldEl.checked = false;
         return;
      }

      if ('value' in fieldEl) {
         fieldEl.value = '';
      }

   }

   static getFieldValue(fieldEl) {
      return ValueNormalizer.asTrimmedString(fieldEl?.value);
   }

   static resetFormFields(fieldEls = []) {
      fieldEls.forEach(ControllerHelper.resetFieldValue);
   }

   static hasCheckedField(fieldEls = []) {
      return fieldEls.some(fieldEl => Boolean(fieldEl?.checked));
   }

   static hideConsolePanel({
      panelEl,
      statusEl,
      setStatus,
   } = {}) {
      panelEl?.classList.remove('active');
      PanelNavigator.clearConsolePanelUrlParam();
      PanelNavigator.clearConsoleMenuButtonSelection();
      setStatus?.(statusEl, '');
   }

   static async loadOptionsAndShowPanel({
      statusEl,
      setStatus,
      loadOptions,
      populateOptions,
      targetEl,
      resetForm,
      activatePanel,
      panelEl,
      errorMessage,
   } = {}) {
      setStatus?.(statusEl, '');

      try {
         const options = await loadOptions();
         populateOptions?.(targetEl, options);
         resetForm?.();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus?.(statusEl, errorMessage, 'is-error');
         activatePanel?.(panelEl);
      }

   }

   static validateOptionalDateRange(startDate, endDate) {
      if (!endDate) {
         return null;
      }

      const effectiveStart = VisitDateValidator.resolveOptionalStartDate(startDate);
      const startMs = new Date(effectiveStart).getTime();
      const endMs = new Date(endDate).getTime();

      if (Number.isNaN(startMs) || Number.isNaN(endMs)) {
         return Strings.validation.dateRangeInvalid;
      }

      if (endMs < startMs) {
         return Strings.validation.endDateBeforeStartDate;
      }

      return null;
   }

   static bindResetValueOnChange(sourceEl, targetEl) {
      sourceEl?.addEventListener('change', () => {
         ControllerHelper.resetFieldValue(targetEl);
      });
   }
}
