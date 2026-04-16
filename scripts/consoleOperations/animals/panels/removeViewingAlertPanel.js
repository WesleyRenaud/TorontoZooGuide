import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createRemoveViewingAlertPanelHtml() {
   return createPanelShellHtml({
      panelId: 'removeViewingAlertPanel',
      title: 'Remove animal viewing alert',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'removeViewingAlertExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'removeViewingAlertSpecies',
   resultsId: 'removeViewingAlertSpeciesResults',
   placeholder: 'Search for a species',
})}
${createActionsHtml({
   submitId: 'submitRemoveViewingAlert',
   submitLabel: 'Remove alert',
})}
${createStatusHtml({
   statusId: 'removeViewingAlertStatus',
})}
      `,
   });
}
