import {
   initDateRangePickers,
   initScheduleDateTimePickers,
} from '../../datePickers/consoleDatePickers.js';

const DATE_PICKER_BINDINGS = {
   dateRanges: [
      ['animals', 'offDisplay'],
      ['animals', 'viewingAlert'],
      ['exhibits', 'closed'],
      ['exhibits', 'open'],
      ['restaurants', 'closed'],
      ['restaurants', 'open'],
      ['restrooms', 'closed'],
      ['restrooms', 'open'],
      ['restrooms', 'alert'],
      ['giftShops', 'closed'],
      ['giftShops', 'open'],
      ['attractions', 'closed'],
      ['attractions', 'open'],
      ['zoomobile', 'stationClosed'],
      ['zoomobile', 'route'],
      ['guardiansTalks', 'schedule'],
      ['wildEncounters', 'schedule'],
      ['drinkingFountains', 'closed'],
      ['drinkingFountains', 'open'],
   ],
   singleDates: [
      ['guardiansTalks', 'endSchedule', 'endDateEl'],
      ['wildEncounters', 'endSchedule', 'endDateEl'],
   ],
   dateTimes: [
      {
         path: ['animals', 'visibilitySchedule'],
         startTimeKey: 'dailyStartTimeEl',
         endTimeKey: 'dailyEndTimeEl',
      },
      {
         path: ['guardiansTalks', 'schedule'],
         startTimeKey: 'timeEl',
      },
      {
         path: ['wildEncounters', 'schedule'],
         startTimeKey: 'timeEl',
      },
   ],
};

function getNestedValue(source, path = []) {
   return path.reduce(
      (currentValue, key) => currentValue?.[key],
      source
   );
}

function initDateRangePickerBinding(refs, path) {
   const binding = getNestedValue(refs, path);

   initDateRangePickers(
      binding?.startDateEl,
      binding?.endDateEl
   );
}

function initSingleDatePickerBinding(refs, path) {
   initDateRangePickers(
      getNestedValue(refs, path),
      null
   );
}

function initDateTimePickerBinding(refs, {
   path,
   startTimeKey,
   endTimeKey = null,
} = {}) {
   const binding = getNestedValue(refs, path);

   initScheduleDateTimePickers(
      binding?.startDateEl,
      binding?.endDateEl,
      binding?.[startTimeKey],
      endTimeKey ? binding?.[endTimeKey] : null
   );
}

export function wireConsoleOperationDatePickers(refs) {
   DATE_PICKER_BINDINGS.dateRanges.forEach(path => {
      initDateRangePickerBinding(refs, path);
   });

   DATE_PICKER_BINDINGS.singleDates.forEach(path => {
      initSingleDatePickerBinding(refs, path);
   });

   DATE_PICKER_BINDINGS.dateTimes.forEach(binding => {
      initDateTimePickerBinding(refs, binding);
   });
}
