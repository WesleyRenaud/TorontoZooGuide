import {
   getStoredItineraryDate,
   setStoredItineraryDate,
} from '../draftStorage.js';
import {
   clampToAllowedVisitDate,
   DEFAULT_DAYS_AHEAD,
   getToday,
   isAfterMaxDate,
   normalizeDate,
   toISODate,
} from '../../visitDates/visitDateRules.js';

export function formatVisitDateLong(date) {
   return date.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

export function readSavedItineraryVisitDate(
   getStoredDate = getStoredItineraryDate
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
   getStoredDate = getStoredItineraryDate,
   setStoredDate = setStoredItineraryDate,
   getTodayFn = getToday,
   daysAhead = DEFAULT_DAYS_AHEAD,
} = {}) {
   const floor = earliestDateFloor ?? getTodayFn();
   let currentDate = null;

   function persistDate(date) {
      setStoredDate(toISODate(date));
   }

   function isSelectableVisitDate(date) {
      if (!date) {
         return false;
      }

      const candidate = normalizeDate(date);

      if (!candidate) {
         return false;
      }

      if (candidate < floor) {
         return false;
      }

      if (isAfterMaxDate(candidate, daysAhead)) {
         return false;
      }

      return true;
   }

   function setDate(date, { updateInput = true, persist = false } = {}) {
      const normalized = normalizeDate(date);

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
         date: toISODate(currentDate),
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

      return clampToAllowedVisitDate(selectedDate, daysAhead, floor);
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
