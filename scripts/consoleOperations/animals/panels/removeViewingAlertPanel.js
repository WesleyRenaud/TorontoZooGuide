import {
   createActions,
   createAutocompleteField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createRemoveViewingAlertPanel() {
   return createPanelShell({
      panelId: 'removeViewingAlertPanel',
      title: 'Remove animal viewing alert',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'removeViewingAlertExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'removeViewingAlertSpecies',
            resultsId: 'removeViewingAlertSpeciesResults',
            placeholder: 'Search for a species',
         }),
         createActions({
            submitId: 'submitRemoveViewingAlert',
            submitLabel: 'Remove alert',
         }),
         createStatus({
            statusId: 'removeViewingAlertStatus',
         }),
      ],
   });
}
