import { CancelOccurrencePanelBuilder } from '../../forms/cancelOccurrencePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class CancelWildEncounterOccurrenceView {
   static createCancelWildEncounterOccurrencePanel() {
      return CancelOccurrencePanelBuilder.createPanel({
         panelId: 'cancelWildEncounterOccurrencePanel',
         title: Strings.panelTitles.cancelWildEncounterOccurrence,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId: 'cancelWildEncounterOccurrenceName',
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         dateLabel: Strings.labels.date,
         dateInputId: 'cancelWildEncounterOccurrenceDate',
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId: 'cancelWildEncounterOccurrenceTimes',
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId: 'submitCancelWildEncounterOccurrence',
         statusId: 'cancelWildEncounterOccurrenceStatus',
      });
   }
}
