import {
   initDateRangePickers,
   initScheduleDateTimePickers,
   initTimePicker,
} from '../../datePickers/consoleDatePickers.js';

const DATE_PICKER_BINDINGS = {
   dateRanges: [
      ['animals', 'offDisplay'],
      ['animals', 'viewingAlert'],
      ['exhibits', 'closed'],
      ['exhibits', 'open'],
      ['restaurants', 'closed'],
      ['restaurants', 'closureOverride'],
      ['restaurants', 'openingSchedule'],
      ['restrooms', 'closed'],
      ['restrooms', 'open'],
      ['restrooms', 'alert'],
      ['giftShops', 'closed'],
      ['giftShops', 'closureOverride'],
      ['giftShops', 'openingSchedule'],
      ['attractions', 'closed'],
      ['attractions', 'closureOverride'],
      ['attractions', 'openingSchedule'],
      ['zoomobile', 'stationClosed'],
      ['zoomobile', 'route'],
      ['guardiansTalks', 'schedule'],
      ['wildEncounters', 'schedule'],
      ['drinkingFountains', 'closed'],
      ['drinkingFountains', 'open'],
      ['updates', 'create'],
   ],
   singleDates: [
      ['guardiansTalks', 'endSchedule', 'endDateEl'],
      ['wildEncounters', 'endSchedule', 'endDateEl'],
      ['updates', 'end', 'endDateEl'],
      ['updates', 'edit', 'endDateEl'],
   ],
   dateTimes: [
      {
         path: ['animals', 'visibilitySchedule'],
         startTimeKey: 'dailyStartTimeEl',
         endTimeKey: 'dailyEndTimeEl',
      },
      {
         path: ['guardiansTalks', 'schedule'],
         timeFieldKeys: [
            'dailyTimeEl',
            'mondayTimeEl',
            'tuesdayTimeEl',
            'wednesdayTimeEl',
            'thursdayTimeEl',
            'fridayTimeEl',
            'saturdayTimeEl',
            'sundayTimeEl',
         ],
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
   timeFieldKeys = [],
} = {}) {
   const binding = getNestedValue(refs, path);

   if (timeFieldKeys.length) {
      timeFieldKeys.forEach((fieldKey) => {
         initTimePicker(binding?.[fieldKey]);
      });
      return;
   }

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
