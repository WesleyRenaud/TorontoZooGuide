import { ConsoleDateFactory } from '../../datePickers/consoleDateFactory.js';
import { DatePickersBindingHelper } from './datePickersBindingHelper.js';

export class DateFactory {
   static DATE_PICKER_BINDINGS = {
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

   static wireConsoleOperationDatePickers(refs) {
      DateFactory.DATE_PICKER_BINDINGS.dateRanges.forEach(path => {
         DatePickersBindingHelper.initDateRangePickerBinding(refs, path);
      });

      DateFactory.DATE_PICKER_BINDINGS.singleDates.forEach(path => {
         DatePickersBindingHelper.initSingleDatePickerBinding(refs, path);
      });

      DateFactory.DATE_PICKER_BINDINGS.dateTimes.forEach(binding => {
         DatePickersBindingHelper.initDateTimePickerBinding(refs, binding);
      });

      if (refs.attractions?.hoursSchedule) {
         Object.assign(
            refs.attractions.hoursSchedule,
            ConsoleDateFactory.initAttractionHoursSchedulePickers(refs.attractions.hoursSchedule)
         );
      }
   }
}
