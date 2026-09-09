import { CancelOccurrencePanelBuilder } from '../../forms/cancelOccurrencePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class CancelGuardiansTalkOccurrenceView {
   static createCancelGuardiansTalkOccurrencePanel() {
      return CancelOccurrencePanelBuilder.createPanel({
         panelId: 'cancelGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.cancelGuardiansTalkOccurrence,
         locationLabel: Strings.labels.location,
         locationInputId: 'cancelGuardiansTalkOccurrenceLocation',
         locationEmptyOptionLabel: Strings.placeholders.location,
         talkLabel: Strings.labels.talkName,
         talkInputId: 'cancelGuardiansTalkOccurrenceTalkName',
         talkEmptyOptionLabel: Strings.placeholders.talk,
         dateLabel: Strings.labels.date,
         dateInputId: 'cancelGuardiansTalkOccurrenceDate',
         dateEmptyOptionLabel: Strings.placeholders.date,
         timesLabel: Strings.labels.talkTimes,
         timesInputId: 'cancelGuardiansTalkOccurrenceTimes',
         timesHelpText: Strings.help.cancelOccurrenceTimes,
         submitId: 'submitCancelGuardiansTalkOccurrence',
         statusId: 'cancelGuardiansTalkOccurrenceStatus',
      });
   }
}
