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

export function createAttractionOpenPanel() {
   return createPanelShell({
      panelId: 'attractionOpenPanel',
      title: 'Set attraction as open',
      bodyChildren: [
         createSelectField({
            label: 'Attraction',
            inputId: 'attractionOpenAttraction',
            emptyOptionLabel: 'Select an attraction',
         }),
         createSchedulePresetField({
            inputId: 'attractionOpenPreset',
         }),
         createDateRangeFields({
            startDateId: 'attractionOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'attractionOpenEndDate',
            endHelpText: 'Leave blank to keep this schedule active until it is changed.',
         }),
         createWeeklyScheduleCheckboxes({
            dayIds: {
               monday: 'attractionOpenMonday',
               tuesday: 'attractionOpenTuesday',
               wednesday: 'attractionOpenWednesday',
               thursday: 'attractionOpenThursday',
               friday: 'attractionOpenFriday',
               saturday: 'attractionOpenSaturday',
               sunday: 'attractionOpenSunday',
               holidays: 'attractionOpenHolidaysOnly',
            },
         }),
         createTextareaField({
            label: 'Schedule message',
            inputId: 'attractionOpenMessage',
            placeholder: 'Enter the message shown when the attraction is closed outside this schedule',
         }),
         createActions({
            submitId: 'submitAttractionOpen',
         }),
         createStatus({
            statusId: 'attractionOpenStatus',
         }),
      ],
   });
}
