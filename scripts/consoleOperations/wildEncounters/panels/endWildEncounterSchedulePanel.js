import {
   createActions,
   createDateField,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createEndWildEncounterSchedulePanel() {
   return createPanelShell({
      panelId: 'endWildEncounterSchedulePanel',
      title: 'End Wild Encounter schedule',
      bodyChildren: [
         createSelectField({
            label: 'Wild Encounter',
            inputId: 'endWildEncounterScheduleName',
            emptyOptionLabel: 'Select a Wild Encounter',
         }),
         createDateField({
            label: 'End date',
            inputId: 'endWildEncounterScheduleDate',
            placeholder: 'Select the date the schedule should end',
            helpText: 'Leave blank to end the schedule today.',
         }),
         createActions({
            submitId: 'submitEndWildEncounterSchedule',
         }),
         createStatus({
            statusId: 'endWildEncounterScheduleStatus',
         }),
      ],
   });
}
