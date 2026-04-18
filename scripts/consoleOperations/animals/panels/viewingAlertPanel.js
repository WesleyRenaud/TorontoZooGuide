import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../templates/fragments.js';

export function createViewingAlertPanelHtml() {
   return createPanelShellHtml({
      panelId: 'viewingAlertPanel',
      title: 'Set animal viewing alert',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'viewingAlertExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'viewingAlertSpecies',
   resultsId: 'viewingAlertSpeciesResults',
   placeholder: 'Search for a species',
})}
${createDateRangeFieldsHtml({
   startDateId: 'viewingAlertStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'viewingAlertEndDate',
   endHelpText: 'Leave blank to keep the viewing alert active until manually removed.',
})}
${createTextareaFieldHtml({
   label: 'Alert message',
   inputId: 'viewingAlertMessage',
   placeholder: 'Enter the viewing alert shown to guests',
})}
${createActionsHtml({
   submitId: 'submitViewingAlert',
})}
${createStatusHtml({
   statusId: 'viewingAlertStatus',
})}
      `,
   });
}
