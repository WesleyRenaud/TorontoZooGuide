import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSchedulePresetField,
   createSelectField,
   createStatus,
   createTextareaField,
   createWeeklyScheduleCheckboxes,
} from '../../templates/fragments.js';

export function createRestaurantOpenPanel() {
   return createPanelShell({
      panelId: 'restaurantOpenPanel',
      title: 'Set restaurant as open',
      bodyChildren: [
         createSelectField({
            label: 'Restaurant',
            inputId: 'restaurantOpenRestaurant',
            emptyOptionLabel: 'Select a restaurant',
         }),
         createSchedulePresetField({
            inputId: 'restaurantOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'restaurantOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'restaurantOpenEndDate',
            endHelpText: 'Leave blank to keep this schedule active until it is changed.',
         }),
         createWeeklyScheduleCheckboxes({
            dayIds: {
               monday: 'restaurantOpenMonday',
               tuesday: 'restaurantOpenTuesday',
               wednesday: 'restaurantOpenWednesday',
               thursday: 'restaurantOpenThursday',
               friday: 'restaurantOpenFriday',
               saturday: 'restaurantOpenSaturday',
               sunday: 'restaurantOpenSunday',
               holidays: 'restaurantOpenHolidaysOnly',
            },
         }),
         createTextareaField({
            label: 'Schedule message',
            inputId: 'restaurantOpenMessage',
            placeholder: 'Enter the message shown when the restaurant is closed outside this schedule',
         }),
         createActions({
            submitId: 'submitRestaurantOpen',
         }),
         createStatus({
            statusId: 'restaurantOpenStatus',
         }),
      ],
   });
}
