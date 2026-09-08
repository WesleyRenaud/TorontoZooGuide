import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class AddGuardiansTalkOccurrenceView {
   static createAddGuardiansTalkOccurrencePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'addGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.addGuardiansTalkOccurrence,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.location,
               inputId: 'addGuardiansTalkOccurrenceLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'addGuardiansTalkOccurrenceTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.date,
               inputId: 'addGuardiansTalkOccurrenceDate',
               placeholder: Strings.placeholders.startDate,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.talkTime,
               inputId: 'addGuardiansTalkOccurrenceTime',
               placeholder: Strings.placeholders.time,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitAddGuardiansTalkOccurrence',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'addGuardiansTalkOccurrenceStatus',
            }),
         ],
      });
   }
}
