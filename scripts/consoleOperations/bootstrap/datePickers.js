import {
   initOffDisplayDatePickers,
   initVisibilityScheduleDateTimePickers
} from '../../datePickers/consoleDatePickers.js';

export function wireConsoleOperationDatePickers({
   animals,
   exhibits,
   restaurants,
   giftShops,
   attractions,
   zoomobile,
   guardiansTalks,
   wildEncounters,
}) {
   [
      animals.offDisplay,
      animals.viewingAlert,
      exhibits.closed,
      exhibits.open,
      restaurants.closed,
      restaurants.open,
      giftShops.closed,
      giftShops.open,
      attractions.closed,
      attractions.open,
      zoomobile.stationClosed,
      zoomobile.route,
      guardiansTalks.schedule,
      wildEncounters.schedule,
   ].forEach(({ startDateEl, endDateEl }) => {
      initOffDisplayDatePickers(startDateEl, endDateEl);
   });

   [
      guardiansTalks.endSchedule.endDateEl,
      wildEncounters.endSchedule.endDateEl,
   ].forEach(dateEl => {
      initOffDisplayDatePickers(dateEl, null);
   });

   [
      {
         startDateEl: animals.visibilitySchedule.startDateEl,
         endDateEl: animals.visibilitySchedule.endDateEl,
         startTimeEl: animals.visibilitySchedule.dailyStartTimeEl,
         endTimeEl: animals.visibilitySchedule.dailyEndTimeEl,
      },
      {
         startDateEl: guardiansTalks.schedule.startDateEl,
         endDateEl: guardiansTalks.schedule.endDateEl,
         startTimeEl: guardiansTalks.schedule.timeEl,
         endTimeEl: null,
      },
      {
         startDateEl: wildEncounters.schedule.startDateEl,
         endDateEl: wildEncounters.schedule.endDateEl,
         startTimeEl: wildEncounters.schedule.timeEl,
         endTimeEl: null,
      }
   ].forEach(({ startDateEl, endDateEl, startTimeEl, endTimeEl }) => {
      initVisibilityScheduleDateTimePickers(
         startDateEl,
         endDateEl,
         startTimeEl,
         endTimeEl
      );
   });
}
