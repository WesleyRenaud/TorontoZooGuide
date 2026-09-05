import { ConsoleDatePickers } from '../../datePickers/consoleDatePickers.js';

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
      ['transportation', 'stationClosed'],
      ['transportation', 'route'],
      ['guardiansTalks', 'schedule'],
      ['wildEncounters', 'schedule'],
      ['drinkingFountains', 'closed'],
      ['drinkingFountains', 'open'],
      ['events', 'create'],
      ['updates', 'create'],
   ],
   singleDates: [
      ['guardiansTalks', 'endSchedule', 'endDateEl'],
      ['guardiansTalks', 'addOccurrence', 'dateEl'],
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
         path: ['guardiansTalks', 'addOccurrence'],
         timeFieldKeys: ['timeEl'],
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

   ConsoleDatePickers.initDateRangePickers(
      binding?.startDateEl,
      binding?.endDateEl
   );
}

function initSingleDatePickerBinding(refs, path) {
   ConsoleDatePickers.initDateRangePickers(
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
         ConsoleDatePickers.initTimePicker(binding?.[fieldKey]);
      });
      return;
   }

   ConsoleDatePickers.initScheduleDateTimePickers(
      binding?.startDateEl,
      binding?.endDateEl,
      binding?.[startTimeKey],
      endTimeKey ? binding?.[endTimeKey] : null
   );
}

export class DatePickers {
   static wireConsoleOperationDatePickers(refs) {
      DATE_PICKER_BINDINGS.dateRanges.forEach(path => {
         initDateRangePickerBinding(refs, path);
      });

      DATE_PICKER_BINDINGS.singleDates.forEach(path => {
         initSingleDatePickerBinding(refs, path);
      });

      DATE_PICKER_BINDINGS.dateTimes.forEach(binding => {
         initDateTimePickerBinding(refs, binding);
      });

      if (refs.attractions?.hoursSchedule) {
         Object.assign(
            refs.attractions.hoursSchedule,
            ConsoleDatePickers.initAttractionHoursSchedulePickers(refs.attractions.hoursSchedule)
         );
      }
   }
}
