import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createOnDisplayPanelHtml() {
   return createPanelShellHtml({
      panelId: 'onDisplayPanel',
      title: 'Set animal as on display',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'onDisplayExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'onDisplaySpecies',
   resultsId: 'onDisplaySpeciesResults',
   placeholder: 'Search for a species',
})}
${createActionsHtml({
   submitId: 'submitOnDisplay',
})}
${createStatusHtml({
   statusId: 'onDisplayStatus',
})}
      `,
   });
}
