import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';
import { ConsoleTextInputFieldBuilder } from '../../templates/consoleTextInputFieldBuilder.js';

export class CreateUpdateView {
   static createCreateUpdatePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'createUpdatePanel',
         title: Strings.panelTitles.createUpdate,
         bodyChildren: [
            ConsoleTextInputFieldBuilder.createTextInputField({
               label: Strings.labels.title,
               inputId: 'createUpdateTitle',
               placeholder: Strings.textareas.updateTitleExample,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.description,
               inputId: 'createUpdateDescription',
               placeholder: Strings.textareas.updateDescription,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.type,
               inputId: 'createUpdateType',
               emptyOptionLabel: Strings.placeholders.type,
               options: [
                  ...Strings.updateTypes,
                  { value: Strings.labels.departure },
               ],
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'createUpdateStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'createUpdateEndDate',
               endHelpText: Strings.help.keepUpdateActiveWithoutEndDate,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitCreateUpdate',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'createUpdateStatus',
            }),
         ],
      });
   }
}
