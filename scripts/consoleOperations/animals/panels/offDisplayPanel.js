import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createDateRangeFieldsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
   createTextareaFieldHtml,
} from '../../shared/panelFragments.js';

export function createOffDisplayPanelHtml() {
   return createPanelShellHtml({
      panelId: 'offDisplayPanel',
      title: 'Set animal as off display',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'offDisplayExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'offDisplaySpecies',
   resultsId: 'offDisplaySpeciesResults',
   placeholder: 'Search for a species',
})}
${createDateRangeFieldsHtml({
   startDateId: 'offDisplayStartDate',
   startHelpText: 'Leave blank to start immediately.',
   endDateId: 'offDisplayEndDate',
   endHelpText: 'Leave blank to keep the animal off display until it is manually set back on display.',
})}
${createTextareaFieldHtml({
   label: 'Reason',
   inputId: 'offDisplayMessage',
   placeholder: 'Enter the reason this animal is off display',
})}
${createActionsHtml({
   submitId: 'submitOffDisplay',
})}
${createStatusHtml({
   statusId: 'offDisplayStatus',
})}
      `,
   });
}
