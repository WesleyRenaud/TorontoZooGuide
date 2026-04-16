import {
   createActionsHtml,
   createAutocompleteFieldHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createRemoveVisibilitySchedulePanelHtml() {
   return createPanelShellHtml({
      panelId: 'removeVisibilitySchedulePanel',
      title: 'Remove visibility schedule',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Exhibit',
   inputId: 'removeVisibilityScheduleExhibit',
   emptyOptionLabel: 'Select an exhibit',
})}
${createAutocompleteFieldHtml({
   label: 'Species',
   inputId: 'removeVisibilityScheduleSpecies',
   resultsId: 'removeVisibilityScheduleSpeciesResults',
   placeholder: 'Search for a species',
})}
${createActionsHtml({
   submitId: 'submitRemoveVisibilitySchedule',
})}
${createStatusHtml({
   statusId: 'removeVisibilityScheduleStatus',
})}
      `,
   });
}
