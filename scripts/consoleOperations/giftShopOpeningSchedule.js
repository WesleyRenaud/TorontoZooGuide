import { loadGiftShops, postJson, setStatus, populateGiftShopDropdown } from './utils.js';

export function createGiftShopOpeningScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   giftShopEl,
   presetEl,
   startDateEl,
   endDateEl,
   mondayEl,
   tuesdayEl,
   wednesdayEl,
   thursdayEl,
   fridayEl,
   saturdayEl,
   sundayEl,
   holidaysOnlyEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function getDayCheckboxes() {
      return [
         mondayEl,
         tuesdayEl,
         wednesdayEl,
         thursdayEl,
         fridayEl,
         saturdayEl,
         sundayEl,
      ];
   }

   function resetDays() {
      if (mondayEl) mondayEl.checked = false;
      if (tuesdayEl) tuesdayEl.checked = false;
      if (wednesdayEl) wednesdayEl.checked = false;
      if (thursdayEl) thursdayEl.checked = false;
      if (fridayEl) fridayEl.checked = false;
      if (saturdayEl) saturdayEl.checked = false;
      if (sundayEl) sundayEl.checked = false;
      if (holidaysOnlyEl) holidaysOnlyEl.checked = false;
   }

   function enableDayCheckboxes() {
      const dayCheckboxes = getDayCheckboxes();

      dayCheckboxes.forEach(checkbox => {
         if (checkbox) checkbox.disabled = false;
      });

      if (holidaysOnlyEl) holidaysOnlyEl.disabled = false;
   }

   function applyPreset() {
      const preset = presetEl?.value ?? 'custom';

      resetDays();
      enableDayCheckboxes();

      if (preset === 'weekendsOnly') {
         if (saturdayEl) saturdayEl.checked = true;
         if (sundayEl) sundayEl.checked = true;

         getDayCheckboxes().forEach(checkbox => {
            if (checkbox) checkbox.disabled = true;
         });

         if (holidaysOnlyEl) holidaysOnlyEl.disabled = true;
         return;
      }

      if (preset === 'weekendsAndHolidays') {
         if (saturdayEl) saturdayEl.checked = true;
         if (sundayEl) sundayEl.checked = true;
         if (holidaysOnlyEl) holidaysOnlyEl.checked = true;

         getDayCheckboxes().forEach(checkbox => {
            if (checkbox) checkbox.disabled = true;
         });

         if (holidaysOnlyEl) holidaysOnlyEl.disabled = true;
      }
   }

   function resetForm() {
      if (giftShopEl) giftShopEl.value = '';
      if (presetEl) presetEl.value = 'custom';
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (messageEl) messageEl.value = '';

      resetDays();
      applyPreset();
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   function hasAtLeastOneOpenDay() {
      return Boolean(
         mondayEl?.checked
         || tuesdayEl?.checked
         || wednesdayEl?.checked
         || thursdayEl?.checked
         || fridayEl?.checked
         || saturdayEl?.checked
         || sundayEl?.checked
         || holidaysOnlyEl?.checked
      );
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         const giftShops = await loadGiftShops();
         populateGiftShopDropdown(giftShopEl, giftShops);
         resetForm();
         activatePanel?.(panelEl);
      }
      catch (err) {
         setStatus(statusEl, 'Failed to load gift shops.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const giftShop = giftShopEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!giftShop) {
         setStatus(statusEl, 'Gift shop is required.', 'is-error');
         return;
      }

      if (!hasAtLeastOneOpenDay()) {
         setStatus(statusEl, 'At least one day or holidays must be selected.', 'is-error');
         return;
      }

      const effectiveStart = startDate || new Date().toISOString().split('T')[0];

      if (endDate) {
         const startMs = new Date(effectiveStart).getTime();
         const endMs = new Date(endDate).getTime();

         if (Number.isNaN(startMs) || Number.isNaN(endMs)) {
            setStatus(statusEl, 'Invalid start or end date.', 'is-error');
            return;
         }

         if (endMs < startMs) {
            setStatus(statusEl, 'End date cannot be before the start date.', 'is-error');
            return;
         }
      }

      try {
         const result = await postJson('/set-gift-shop-opening-schedule', {
            giftShop,
            scheduleStartDate: startDate || null,
            scheduleEndDate: endDate || null,
            monday: Boolean(mondayEl?.checked),
            tuesday: Boolean(tuesdayEl?.checked),
            wednesday: Boolean(wednesdayEl?.checked),
            thursday: Boolean(thursdayEl?.checked),
            friday: Boolean(fridayEl?.checked),
            saturday: Boolean(saturdayEl?.checked),
            sunday: Boolean(sundayEl?.checked),
            holidaysOnly: Boolean(holidaysOnlyEl?.checked),
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.giftShop} opening schedule was saved.`,
               'is-success'
            );
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   presetEl?.addEventListener('change', applyPreset);
   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}