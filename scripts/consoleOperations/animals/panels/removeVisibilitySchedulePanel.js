import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createRemoveVisibilitySchedulePanel() {
   return createPanelShell({
      panelId: 'removeVisibilitySchedulePanel',
      title: 'Remove visibility schedule',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'removeVisibilityScheduleExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'removeVisibilityScheduleSpecies',
            resultsId: 'removeVisibilityScheduleSpeciesResults',
            placeholder: 'Search for a species',
         }),
         createActions({
            submitId: 'submitRemoveVisibilitySchedule',
         }),
         createStatus({
            statusId: 'removeVisibilityScheduleStatus',
         }),
      ],
   });
}
