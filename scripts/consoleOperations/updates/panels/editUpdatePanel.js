import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createEditUpdatePanel() {
   return createPanelShell({
      panelId: 'editUpdatePanel',
      title: 'Edit update',
      bodyChildren: [
         createSelectField({
            label: 'Update',
            inputId: 'editUpdateKey',
            emptyOptionLabel: 'Select an update',
         }),
         createTextareaField({
            label: 'Description',
            inputId: 'editUpdateDescription',
            placeholder: 'Leave blank to keep the current description',
         }),
         createSelectField({
            label: 'Type',
            inputId: 'editUpdateType',
            emptyOptionLabel: 'Keep current type',
            options: [
               { value: 'Animal Birth', label: 'Animal Birth' },
               { value: 'Animal Passing', label: 'Animal Passing' },
               { value: 'Closure', label: 'Closure' },
               { value: 'New Arrival', label: 'New Arrival' },
               { value: 'Departure', label: 'Departure' },
            ],
         }),
         createDateField({
            label: 'End date',
            inputId: 'editUpdateEndDate',
            placeholder: 'Select a new end date',
            helpText: 'Leave blank to keep the current end date.',
         }),
         createActions({
            submitId: 'submitEditUpdate',
         }),
         createStatus({
            statusId: 'editUpdateStatus',
         }),
      ],
   });
}
