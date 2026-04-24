import {
   createActions,
   createAutocompleteField,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createViewingAlertPanel() {
   return createPanelShell({
      panelId: 'viewingAlertPanel',
      title: 'Set animal viewing alert',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'viewingAlertExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'viewingAlertSpecies',
            resultsId: 'viewingAlertSpeciesResults',
            placeholder: 'Search for a species',
         }),
         createDateRangeFields({
            startDateId: 'viewingAlertStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'viewingAlertEndDate',
            endHelpText: 'Leave blank to keep the viewing alert active until manually removed.',
         }),
         createTextareaField({
            label: 'Alert message',
            inputId: 'viewingAlertMessage',
            placeholder: 'Enter the viewing alert shown to guests',
         }),
         createActions({
            submitId: 'submitViewingAlert',
         }),
         createStatus({
            statusId: 'viewingAlertStatus',
         }),
      ],
   });
}
