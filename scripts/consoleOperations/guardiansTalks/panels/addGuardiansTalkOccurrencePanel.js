import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class AddGuardiansTalkOccurrencePanel {
   static createAddGuardiansTalkOccurrencePanel() {
      return Fragments.createPanelShell({
         panelId: 'addGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.addGuardiansTalkOccurrence,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.labels.location,
               inputId: 'addGuardiansTalkOccurrenceLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            Fragments.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'addGuardiansTalkOccurrenceTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            Fragments.createDateField({
               label: Strings.labels.date,
               inputId: 'addGuardiansTalkOccurrenceDate',
               placeholder: Strings.placeholders.startDate,
            }),
            Fragments.createDateField({
               label: Strings.labels.talkTime,
               inputId: 'addGuardiansTalkOccurrenceTime',
               placeholder: Strings.placeholders.time,
            }),
            Fragments.createActions({
               submitId: 'submitAddGuardiansTalkOccurrence',
            }),
            Fragments.createStatus({
               statusId: 'addGuardiansTalkOccurrenceStatus',
            }),
         ],
      });
   }
}
