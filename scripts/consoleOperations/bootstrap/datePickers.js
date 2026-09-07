import { ConsoleDatePickers } from '../../datePickers/consoleDatePickers.js';
import { DatePickersBindingHelpers } from './datePickersBindingHelpers.js';

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

export class DatePickers {
   static wireConsoleOperationDatePickers(refs) {
      DATE_PICKER_BINDINGS.dateRanges.forEach(path => {
         DatePickersBindingHelpers.initDateRangePickerBinding(refs, path);
      });

      DATE_PICKER_BINDINGS.singleDates.forEach(path => {
         DatePickersBindingHelpers.initSingleDatePickerBinding(refs, path);
      });

      DATE_PICKER_BINDINGS.dateTimes.forEach(binding => {
         DatePickersBindingHelpers.initDateTimePickerBinding(refs, binding);
      });

      if (refs.attractions?.hoursSchedule) {
         Object.assign(
            refs.attractions.hoursSchedule,
            ConsoleDatePickers.initAttractionHoursSchedulePickers(refs.attractions.hoursSchedule)
         );
      }
   }
}
