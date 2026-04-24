import {
   createActions,
   createAutocompleteField,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createOffDisplayPanel() {
   return createPanelShell({
      panelId: 'offDisplayPanel',
      title: 'Set animal as off display',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'offDisplayExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createAutocompleteField({
            label: 'Species',
            inputId: 'offDisplaySpecies',
            resultsId: 'offDisplaySpeciesResults',
            placeholder: 'Search for a species',
         }),
         createDateRangeFields({
            startDateId: 'offDisplayStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'offDisplayEndDate',
            endHelpText: 'Leave blank to keep the animal off display until it is manually set back on display.',
         }),
         createTextareaField({
            label: 'Reason',
            inputId: 'offDisplayMessage',
            placeholder: 'Enter the reason this animal is off display',
         }),
         createActions({
            submitId: 'submitOffDisplay',
         }),
         createStatus({
            statusId: 'offDisplayStatus',
         }),
      ],
   });
}
