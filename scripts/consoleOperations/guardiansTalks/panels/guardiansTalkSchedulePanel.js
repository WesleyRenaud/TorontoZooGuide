import {
   createActionsHtml,
   createCheckboxGridFieldHtml,
   createDateFieldHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../shared/panelFragments.js';

export function createGuardiansTalkSchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'guardiansTalkSchedulePanel',
      title: 'Set Meet the Guardians talk schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Location',
   inputId: 'guardiansTalkScheduleLocation',
   emptyOptionLabel: 'Select an exhibit',
})}
${createSelectFieldHtml({
   label: 'Talk name',
   inputId: 'guardiansTalkScheduleTalkName',
   emptyOptionLabel: 'Select a talk',
})}
${createDateRangeFieldsHtml({
   startDateId: 'guardiansTalkScheduleStartDate',
   endDateId: 'guardiansTalkScheduleEndDate',
   endHelpText: 'Leave blank to continue until the schedule is ended.',
})}
${createCheckboxGridFieldHtml({
   label: 'Occurs on these days',
   options: [
      { id: 'guardiansTalkScheduleMonday', label: 'Monday' },
      { id: 'guardiansTalkScheduleTuesday', label: 'Tuesday' },
      { id: 'guardiansTalkScheduleWednesday', label: 'Wednesday' },
      { id: 'guardiansTalkScheduleThursday', label: 'Thursday' },
      { id: 'guardiansTalkScheduleFriday', label: 'Friday' },
      { id: 'guardiansTalkScheduleSaturday', label: 'Saturday' },
      { id: 'guardiansTalkScheduleSunday', label: 'Sunday' },
   ],
})}
${createDateFieldHtml({
   label: 'Talk time',
   inputId: 'guardiansTalkScheduleTime',
   placeholder: 'Select a talk time',
})}
${createTextareaFieldHtml({
   label: 'Schedule message',
   inputId: 'guardiansTalkScheduleMessage',
   placeholder: 'Enter an optional message for this talk schedule',
})}
${createActionsHtml({
   submitId: 'submitGuardiansTalkSchedule',
})}
${createStatusHtml({
   statusId: 'guardiansTalkScheduleStatus',
})}
      `,
   });
}
