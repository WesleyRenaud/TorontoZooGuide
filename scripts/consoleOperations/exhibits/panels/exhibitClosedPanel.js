import {
   createActionsHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createExhibitClosedPanelHtml() {
   return createPanelShellHtml({
      panelId: 'exhibitClosedPanel',
      title: 'Set exhibit as closed',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'exhibitClosedExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createDateRangeFieldsHtml({
   startDateId: 'exhibitClosedStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'exhibitClosedEndDate',
   endHelpText: 'Leave blank to keep the exhibit closed until it is manually reopened.',
})}
${createTextareaFieldHtml({
   label: 'Closure message',
   inputId: 'exhibitClosedMessage',
   placeholder: 'Enter the closure message shown to guests',
})}
${createActionsHtml({
   submitId: 'submitExhibitClosed',
})}
${createStatusHtml({
   statusId: 'exhibitClosedStatus',
})}
      `,
   });
}
