import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextInputField,
   createTextareaField,
} from '../../templates/fragments.js';

export function createCreateUpdatePanel() {
   return createPanelShell({
      panelId: 'createUpdatePanel',
      title: 'Create update',
      bodyChildren: [
         createTextInputField({
            label: 'Title',
            inputId: 'createUpdateTitle',
            placeholder: 'Example: New baby giraffe',
         }),
         createTextareaField({
            label: 'Description',
            inputId: 'createUpdateDescription',
            placeholder: 'Enter the update shown to guests',
         }),
         createSelectField({
            label: 'Type',
            inputId: 'createUpdateType',
            emptyOptionLabel: 'Select a type',
            options: [
               { value: 'Animal Birth', label: 'Animal Birth' },
               { value: 'Animal Passing', label: 'Animal Passing' },
               { value: 'Closure', label: 'Closure' },
               { value: 'New Arrival', label: 'New Arrival' },
               { value: 'Departure', label: 'Departure' },
            ],
         }),
         createDateRangeFields({
            startDateId: 'createUpdateStartDate',
            // TO-DO: create centralized strings for things like this
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'createUpdateEndDate',
            endHelpText: 'Leave blank to keep the update active with no end date.',
         }),
         createActions({
            submitId: 'submitCreateUpdate',
         }),
         createStatus({
            statusId: 'createUpdateStatus',
         }),
      ],
   });
}
