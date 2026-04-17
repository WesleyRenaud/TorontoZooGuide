export function resetFieldValue(fieldEl) {
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

export function resetFormFields(fieldEls = []) {
   fieldEls.forEach(resetFieldValue);
}

export function hasCheckedField(fieldEls = []) {
   return fieldEls.some(fieldEl => Boolean(fieldEl?.checked));
}

export function hideConsolePanel({
   panelEl,
   statusEl,
   setStatus,
} = {}) {
   panelEl?.classList.remove('active');
   setStatus?.(statusEl, '');
}

export async function loadOptionsAndShowPanel({
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

export function validateOptionalDateRange(startDate, endDate) {
   if (!endDate) {
      return null;
   }

   const effectiveStart = startDate || new Date().toISOString().split('T')[0];
   const startMs = new Date(effectiveStart).getTime();
   const endMs = new Date(endDate).getTime();

   if (Number.isNaN(startMs) || Number.isNaN(endMs)) {
      return 'Invalid start or end date.';
   }

   if (endMs < startMs) {
      return 'End date cannot be before the start date.';
   }

   return null;
}

export function bindResetValueOnChange(sourceEl, targetEl) {
   sourceEl?.addEventListener('change', () => {
      resetFieldValue(targetEl);
   });
}
