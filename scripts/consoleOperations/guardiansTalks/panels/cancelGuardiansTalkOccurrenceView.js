import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class CancelGuardiansTalkOccurrenceView {
   static createCancelGuardiansTalkOccurrencePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'cancelGuardiansTalkOccurrencePanel',
         title: Strings.panelTitles.cancelGuardiansTalkOccurrence,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.location,
               inputId: 'cancelGuardiansTalkOccurrenceLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'cancelGuardiansTalkOccurrenceTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.date,
               inputId: 'cancelGuardiansTalkOccurrenceDate',
               emptyOptionLabel: Strings.placeholders.date,
            }),
            ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
               label: Strings.labels.talkTimes,
               inputId: 'cancelGuardiansTalkOccurrenceTimes',
               helpText: Strings.help.cancelOccurrenceTimes,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitCancelGuardiansTalkOccurrence',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'cancelGuardiansTalkOccurrenceStatus',
            }),
         ],
      });
   }
}
