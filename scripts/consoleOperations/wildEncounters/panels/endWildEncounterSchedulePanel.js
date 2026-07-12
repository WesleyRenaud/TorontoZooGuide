import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateField,
   createPanelShell,
   createScheduleTimesCheckboxField,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';

export function createEndWildEncounterSchedulePanel() {
   return createPanelShell({
      panelId: 'endWildEncounterSchedulePanel',
      title: APP_STRINGS.panelTitles.endWildEncounterSchedule,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.wildEncounter,
            inputId: 'endWildEncounterScheduleName',
            emptyOptionLabel: APP_STRINGS.placeholders.wildEncounter,
         }),
         createScheduleTimesCheckboxField({
            label: APP_STRINGS.labels.encounterTimes,
            inputId: 'endWildEncounterScheduleTimes',
            helpText: APP_STRINGS.help.endScheduleTimes,
         }),
         createDateField({
            label: APP_STRINGS.labels.endDate,
            inputId: 'endWildEncounterScheduleDate',
            placeholder: APP_STRINGS.placeholders.scheduleEndDate,
            helpText: APP_STRINGS.help.endScheduleToday,
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
