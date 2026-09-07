import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class EndGuardiansTalkSchedulePanel {
   static createEndGuardiansTalkSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'endGuardiansTalkSchedulePanel',
         title: Strings.panelTitles.endGuardiansTalkSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.location,
               inputId: 'endGuardiansTalkScheduleLocation',
               emptyOptionLabel: Strings.placeholders.location,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'endGuardiansTalkScheduleTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
               label: Strings.labels.talkTimes,
               inputId: 'endGuardiansTalkScheduleTimes',
               helpText: Strings.help.endScheduleTimes,
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.endDate,
               inputId: 'endGuardiansTalkScheduleEndDate',
               placeholder: Strings.placeholders.scheduleEndDate,
               helpText: Strings.help.endScheduleToday,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitEndGuardiansTalkSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'endGuardiansTalkScheduleStatus',
            }),
         ],
      });
   }
}
