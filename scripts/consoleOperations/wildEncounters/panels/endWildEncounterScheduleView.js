import { EndRecurringSchedulePanelBuilder } from '../../forms/endRecurringSchedulePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class EndWildEncounterScheduleView {
   static createEndWildEncounterSchedulePanel() {
      return EndRecurringSchedulePanelBuilder.createPanel({
         panelId: 'endWildEncounterSchedulePanel',
         title: Strings.panelTitles.endWildEncounterSchedule,
         entityLabel: Strings.entityLabels.wildEncounter,
         entityInputId: 'endWildEncounterScheduleName',
         entityEmptyOptionLabel: Strings.placeholders.wildEncounter,
         timesLabel: Strings.labels.encounterTimes,
         timesInputId: 'endWildEncounterScheduleTimes',
         timesHelpText: Strings.help.endScheduleTimes,
         endDateLabel: Strings.labels.stopsBeingOfferedOn,
         endDateInputId: 'endWildEncounterScheduleDate',
         endDatePlaceholder: Strings.placeholders.stopsBeingOfferedOn,
         endDateHelpText: Strings.help.endScheduleToday,
         submitId: 'submitEndWildEncounterSchedule',
         statusId: 'endWildEncounterScheduleStatus',
      });
   }
}
