import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createRestroomOpenPanel() {
   return createPanelShell({
      panelId: 'restroomOpenPanel',
      title: 'Set restroom as open',
      bodyChildren: [
         createSelectField({
            label: 'Restroom',
            inputId: 'restroomOpenRestroom',
            emptyOptionLabel: 'Select a restroom',
         }),
         createDateRangeFields({
            startDateId: 'restroomOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'restroomOpenEndDate',
            endHelpText: 'Leave blank to keep the restroom explicitly open until it is changed.',
         }),
         createActions({
            submitId: 'submitRestroomOpen',
         }),
         createStatus({
            statusId: 'restroomOpenStatus',
         }),
      ],
   });
}
