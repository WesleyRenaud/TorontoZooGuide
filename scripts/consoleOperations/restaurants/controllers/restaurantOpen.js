import { loadRestaurants, setStatus, populateRestaurantDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createRestaurantOpenController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   restaurantEl,
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
      getDayCheckboxes().forEach(checkbox => {
         if (checkbox) checkbox.disabled = false;
      });

      if (holidaysOnlyEl) holidaysOnlyEl.disabled = false;
   }

   function applyPreset() {
      const preset = presetEl?.value ?? 'everyDay';

      resetDays();
      enableDayCheckboxes();

      if (preset === 'everyDay') {
         getDayCheckboxes().forEach(checkbox => {
            if (!checkbox) return;

            checkbox.checked = true;
            checkbox.disabled = true;
         });

         if (holidaysOnlyEl) {
            holidaysOnlyEl.checked = true;
            holidaysOnlyEl.disabled = true;
         }

         return;
      }

      if (preset === 'weekendsOnly') {
         if (saturdayEl) saturdayEl.checked = true;
         if (sundayEl) sundayEl.checked = true;

         getDayCheckboxes().forEach(checkbox => {
            if (checkbox) checkbox.disabled = true;
         });

         if (holidaysOnlyEl) {
            holidaysOnlyEl.checked = false;
            holidaysOnlyEl.disabled = true;
         }

         return;
      }

      if (preset === 'weekendsAndHolidays') {
         if (saturdayEl) saturdayEl.checked = true;
         if (sundayEl) sundayEl.checked = true;

         getDayCheckboxes().forEach(checkbox => {
            if (checkbox) checkbox.disabled = true;
         });

         if (holidaysOnlyEl) {
            holidaysOnlyEl.checked = true;
            holidaysOnlyEl.disabled = true;
         }
      }
   }

   function resetForm() {
      if (restaurantEl) restaurantEl.value = '';
      if (presetEl) presetEl.value = 'everyDay';
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

   function isEveryDaySchedule() {
      return Boolean(
         mondayEl?.checked
         && tuesdayEl?.checked
         && wednesdayEl?.checked
         && thursdayEl?.checked
         && fridayEl?.checked
         && saturdayEl?.checked
         && sundayEl?.checked
      );
   }

   async function onShowClick() {

      setStatus(statusEl, '');

      try {
         const restaurants = await loadRestaurants();
         populateRestaurantDropdown(restaurantEl, restaurants);
         resetForm();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load restaurants.', 'is-error');
         activatePanel?.(panelEl);
      }

   }

   async function onSubmitClick() {

      const restaurant = restaurantEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!restaurant) {
         setStatus(statusEl, 'Restaurant is required.', 'is-error');
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

         const result = await postJson('/set-restaurant-opening-schedule', {
            restaurant,
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
               isEveryDaySchedule()
                  ? `${result.restaurant} was set as open.`
                  : `${result.restaurant} opening schedule was saved.`,
               'is-success'
            );

            resetForm();

         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }

      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }

   }

   presetEl?.addEventListener('change', applyPreset);
   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide
   };

}
