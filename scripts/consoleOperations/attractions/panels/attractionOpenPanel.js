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

export function createAttractionOpenPanelHtml() {
   return createPanelShellHtml({
      panelId: 'attractionOpenPanel',
      title: 'Set attraction as open',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Attraction',
   inputId: 'attractionOpenAttraction',
   emptyOptionLabel: 'Select an attraction',
})}
${createSchedulePresetFieldHtml({
   inputId: 'attractionOpenPreset',
})}
${createDateRangeFieldsHtml({
   startDateId: 'attractionOpenStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'attractionOpenEndDate',
   endHelpText: 'Leave blank to keep this schedule active until it is changed.',
})}
${createWeeklyScheduleCheckboxesHtml({
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
})}
${createTextareaFieldHtml({
   label: 'Schedule message',
   inputId: 'attractionOpenMessage',
   placeholder: 'Enter the message shown when the attraction is closed outside this schedule',
})}
${createActionsHtml({
   submitId: 'submitAttractionOpen',
})}
${createStatusHtml({
   statusId: 'attractionOpenStatus',
})}
      `,
   });
}
