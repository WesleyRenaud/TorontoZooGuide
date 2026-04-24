import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createEndGuardiansTalkSchedulePanel() {
   return createPanelShell({
      panelId: 'endGuardiansTalkSchedulePanel',
      title: 'End Meet the Guardians talk schedule',
      bodyChildren: [
         createSelectField({
            label: 'Location',
            inputId: 'endGuardiansTalkScheduleLocation',
            emptyOptionLabel: 'Select a location',
         }),
         createSelectField({
            label: 'Talk name',
            inputId: 'endGuardiansTalkScheduleTalkName',
            emptyOptionLabel: 'Select a talk',
         }),
         createDateField({
            label: 'End date',
            inputId: 'endGuardiansTalkScheduleEndDate',
            placeholder: 'Select the date the schedule should end',
            helpText: 'Leave blank to end the schedule today.',
         }),
         createActions({
            submitId: 'submitEndGuardiansTalkSchedule',
         }),
         createStatus({
            statusId: 'endGuardiansTalkScheduleStatus',
         }),
      ],
   });
}
