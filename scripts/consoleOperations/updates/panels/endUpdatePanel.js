import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createEndUpdatePanel() {
   return createPanelShell({
      panelId: 'endUpdatePanel',
      title: 'End update',
      bodyChildren: [
         createSelectField({
            label: 'Update',
            inputId: 'endUpdateKey',
            emptyOptionLabel: 'Select an update',
         }),
         createDateField({
            label: 'End date',
            inputId: 'endUpdateEndDate',
            placeholder: 'Select an end date',
            helpText: 'Leave blank to end the update today.',
         }),
         createActions({
            submitId: 'submitEndUpdate',
         }),
         createStatus({
            statusId: 'endUpdateStatus',
         }),
      ],
   });
}
