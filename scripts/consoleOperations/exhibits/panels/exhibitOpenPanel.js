import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createExhibitOpenPanel() {
   return createPanelShell({
      panelId: 'exhibitOpenPanel',
      title: 'Set exhibit as open',
      bodyChildren: [
         createSelectField({
            label: 'Exhibit',
            inputId: 'exhibitOpenExhibit',
            emptyOptionLabel: 'Select an exhibit',
         }),
         createDateRangeFields({
            startDateId: 'exhibitOpenStartDate',
            startHelpText: 'Leave blank to start immediately.',
            endDateId: 'exhibitOpenEndDate',
            endHelpText: 'Leave blank to keep the exhibit explicitly open until it is changed.',
         }),
         createActions({
            submitId: 'submitExhibitOpen',
         }),
         createStatus({
            statusId: 'exhibitOpenStatus',
         }),
      ],
   });
}
