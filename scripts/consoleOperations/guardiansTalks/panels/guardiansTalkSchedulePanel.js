import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleWildEncounterScheduleRowsFieldBuilder } from '../../templates/consoleWildEncounterScheduleRowsFieldBuilder.js';

export class GuardiansTalkSchedulePanel {
   static createGuardiansTalkSchedulePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'guardiansTalkSchedulePanel',
         title: Strings.panelTitles.guardiansTalkSchedule,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.location,
               inputId: 'guardiansTalkScheduleLocation',
               emptyOptionLabel: Strings.placeholders.exhibit,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.talkName,
               inputId: 'guardiansTalkScheduleTalkName',
               emptyOptionLabel: Strings.placeholders.talk,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'guardiansTalkScheduleStartDate',
               endDateId: 'guardiansTalkScheduleEndDate',
               endHelpText: Strings.help.continueUntilScheduleEnded,
            }),
            ConsoleWildEncounterScheduleRowsFieldBuilder.createWildEncounterScheduleRowsField({
               label: Strings.labels.talkTimes,
               rowsId: 'guardiansTalkScheduleScheduleRows',
               addRowButtonId: 'guardiansTalkScheduleAddScheduleRow',
               helpText: Strings.help.talkScheduleRows,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.scheduleMessage,
               inputId: 'guardiansTalkScheduleMessage',
               placeholder: Strings.textareas.optionalScheduleMessage('talk'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitGuardiansTalkSchedule',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'guardiansTalkScheduleStatus',
            }),
         ],
      });
   }
}
