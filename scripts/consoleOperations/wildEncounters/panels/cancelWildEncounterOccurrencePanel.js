import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class CancelWildEncounterOccurrencePanel {
   static createCancelWildEncounterOccurrencePanel() {
      return Fragments.createPanelShell({
         panelId: 'cancelWildEncounterOccurrencePanel',
         title: Strings.panelTitles.cancelWildEncounterOccurrence,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.wildEncounter,
               inputId: 'cancelWildEncounterOccurrenceName',
               emptyOptionLabel: Strings.placeholders.wildEncounter,
            }),
            Fragments.createSelectField({
               label: Strings.labels.date,
               inputId: 'cancelWildEncounterOccurrenceDate',
               emptyOptionLabel: Strings.placeholders.date,
            }),
            Fragments.createScheduleTimesCheckboxField({
               label: Strings.labels.encounterTimes,
               inputId: 'cancelWildEncounterOccurrenceTimes',
               helpText: Strings.help.cancelOccurrenceTimes,
            }),
            Fragments.createActions({
               submitId: 'submitCancelWildEncounterOccurrence',
            }),
            Fragments.createStatus({
               statusId: 'cancelWildEncounterOccurrenceStatus',
            }),
         ],
      });
   }
}
