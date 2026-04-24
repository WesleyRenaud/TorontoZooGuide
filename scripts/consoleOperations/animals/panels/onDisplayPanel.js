import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createOnDisplayPanel() {
   return createPanelShell({
      panelId: 'onDisplayPanel',
      title: 'Set animal as on display',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'onDisplayExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'onDisplaySpecies',
            resultsId: 'onDisplaySpeciesResults',
            placeholder: 'Search for a species',
         }),
         createActions({
            submitId: 'submitOnDisplay',
         }),
         createStatus({
            statusId: 'onDisplayStatus',
         }),
      ],
   });
}
