import {
   createActionsHtml,
   createDateFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createEndGuardiansTalkSchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'endGuardiansTalkSchedulePanel',
      title: 'End Meet the Guardians talk schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Location',
   inputId: 'endGuardiansTalkScheduleLocation',
   emptyOptionLabel: 'Select a location',
})}
${createSelectFieldHtml({
   label: 'Talk name',
   inputId: 'endGuardiansTalkScheduleTalkName',
   emptyOptionLabel: 'Select a talk',
})}
${createDateFieldHtml({
   label: 'End date',
   inputId: 'endGuardiansTalkScheduleEndDate',
   placeholder: 'Select the date the schedule should end',
   helpText: 'Leave blank to end the schedule today.',
})}
${createActionsHtml({
   submitId: 'submitEndGuardiansTalkSchedule',
})}
${createStatusHtml({
   statusId: 'endGuardiansTalkScheduleStatus',
})}
      `,
   });
}
