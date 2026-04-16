import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSchedulePresetFieldHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
   createWeeklyScheduleCheckboxesHtml,
} from '../../shared/panelFragments.js';

export function createRestaurantOpenPanelHtml() {
   return createPanelShellHtml({
      panelId: 'restaurantOpenPanel',
      title: 'Set restaurant as open',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Restaurant',
   inputId: 'restaurantOpenRestaurant',
   emptyOptionLabel: 'Select a restaurant',
})}
${createSchedulePresetFieldHtml({
   inputId: 'restaurantOpenPreset',
})}
${createDateRangeFieldsHtml({
   startDateId: 'restaurantOpenStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'restaurantOpenEndDate',
   endHelpText: 'Leave blank to keep this schedule active until it is changed.',
})}
${createWeeklyScheduleCheckboxesHtml({
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
})}
${createTextareaFieldHtml({
   label: 'Schedule message',
   inputId: 'restaurantOpenMessage',
   placeholder: 'Enter the message shown when the restaurant is closed outside this schedule',
})}
${createActionsHtml({
   submitId: 'submitRestaurantOpen',
})}
${createStatusHtml({
   statusId: 'restaurantOpenStatus',
})}
      `,
   });
}
