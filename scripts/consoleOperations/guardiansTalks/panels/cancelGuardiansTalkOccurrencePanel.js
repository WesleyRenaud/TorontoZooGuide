import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class CancelGuardiansTalkOccurrencePanel {
   static createCancelGuardiansTalkOccurrencePanel() {
      return Fragments.createPanelShell({
         panelId: 'cancelGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.cancelGuardiansTalkOccurrence,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.location,
               inputId: 'cancelGuardiansTalkOccurrenceLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            Fragments.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'cancelGuardiansTalkOccurrenceTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            Fragments.createSelectField({
               label: Strings.labels.date,
               inputId: 'cancelGuardiansTalkOccurrenceDate',
               emptyOptionLabel: Strings.placeholders.date,
            }),
            Fragments.createScheduleTimesCheckboxField({
               label: Strings.labels.talkTimes,
               inputId: 'cancelGuardiansTalkOccurrenceTimes',
               helpText: Strings.help.cancelOccurrenceTimes,
            }),
            Fragments.createActions({
               submitId: 'submitCancelGuardiansTalkOccurrence',
            }),
            Fragments.createStatus({
               statusId: 'cancelGuardiansTalkOccurrenceStatus',
            }),
         ],
      });
   }
}
