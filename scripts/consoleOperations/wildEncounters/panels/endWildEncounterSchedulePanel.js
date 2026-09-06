import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class EndWildEncounterSchedulePanel {
   static createEndWildEncounterSchedulePanel() {
      return Fragments.createPanelShell({
         panelId: 'endWildEncounterSchedulePanel',
         title: Strings.panelTitles.endWildEncounterSchedule,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'endWildEncounterScheduleName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            Fragments.createScheduleTimesCheckboxField({
               label: Strings.labels.encounterTimes,
               inputId: 'endWildEncounterScheduleTimes',
               helpText: Strings.help.endScheduleTimes,
            }),
            Fragments.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endWildEncounterScheduleDate',
               placeholder: Strings.placeholders.scheduleEndDate,
               helpText: Strings.help.endScheduleToday,
            }),
            Fragments.createActions({
               submitId: 'submitEndWildEncounterSchedule',
            }),
            Fragments.createStatus({
               statusId: 'endWildEncounterScheduleStatus',
            }),
         ],
      });
   }
}
