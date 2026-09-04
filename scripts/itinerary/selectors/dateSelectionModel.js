import { DraftStorage } from '../draftStorage.js';
import { VisitDateRules } from '../../visitDates/visitDateRules.js';

export function formatVisitDateLong(date) {
   return date.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

export function readSavedItineraryVisitDate(
   getStoredDate = DraftStorage.getStoredItineraryDate
) {
   const iso = getStoredDate();

   if (!iso) {
      return null;
   }

   const savedDate = new Date(`${iso}T12:00:00`);

   return Number.isFinite(savedDate.getTime()) ? savedDate : null;
}

export function createDateSelectionModel({
   initialDate = null,
   syncInputValue = () => {},
   earliestDateFloor = null,
   getStoredDate = DraftStorage.getStoredItineraryDate,
   setStoredDate = DraftStorage.setStoredItineraryDate,
   getTodayFn = VisitDateRules.getToday,
   daysAhead = VisitDateRules.DEFAULT_DAYS_AHEAD,
} = {}) {
   const floor = earliestDateFloor ?? getTodayFn();
   let currentDate = null;

   function persistDate(date) {
      setStoredDate(VisitDateRules.toISODate(date));
   }

   function isSelectableVisitDate(date) {
      if (!date) {
         return false;
      }

      const candidate = VisitDateRules.normalizeDate(date);

      if (!candidate) {
         return false;
      }

      if (candidate < floor) {
         return false;
      }

      if (candidate > VisitDateRules.addLocalCalendarDays(getTodayFn(), daysAhead)) {
         return false;
      }

      return true;
   }

   function setDate(date, { updateInput = true, persist = false } = {}) {
      const normalized = VisitDateRules.normalizeDate(date);

      if (!isSelectableVisitDate(normalized)) {
         return false;
      }

      currentDate = normalized;

      if (updateInput) {
         syncInputValue(normalized);
      }

      if (persist) {
         persistDate(normalized);
      }

      return true;
   }

   function buildCurrentDatePayload() {
      if (!isSelectableVisitDate(currentDate)) {
         return null;
      }

      return {
         date: VisitDateRules.toISODate(currentDate),
         dateObj: currentDate,
      };
   }

   function persistCurrentDate() {
      if (!setDate(currentDate, { persist: true, updateInput: true })) {
         return null;
      }

      return buildCurrentDatePayload();
   }

   function getDisplayDate() {
      const savedDate = readSavedItineraryVisitDate(getStoredDate);
      const selectedDate = initialDate || savedDate || floor;

      return VisitDateRules.clampToAllowedVisitDate(selectedDate, daysAhead, floor, getTodayFn());
   }

   function getDate() {
      return currentDate;
   }

   return {
      getDate,
      setDate,
      persistCurrentDate,
      getDisplayDate,
   };
}
