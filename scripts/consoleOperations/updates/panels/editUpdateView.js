import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateFieldBuilder } from '../../templates/consoleDateFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class EditUpdateView {
   static createEditUpdatePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'editUpdatePanel',
         title: Strings.panelTitles.editUpdate,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.update,
               inputId: 'editUpdateKey',
               emptyOptionLabel: Strings.placeholders.update,
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.description,
               inputId: 'editUpdateDescription',
               placeholder: Strings.textareas.currentDescription,
            }),
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.labels.type,
               inputId: 'editUpdateType',
               emptyOptionLabel: Strings.placeholders.option,
               options: [
                  ...Strings.updateTypes,
                  { value: Strings.labels.departure },
               ],
            }),
            ConsoleDateFieldBuilder.createDateField({
               label: Strings.labels.stopsBeingOfferedOn,
               inputId: 'editUpdateEndDate',
               placeholder: Strings.placeholders.newEndDate,
               helpText: Strings.help.keepUpdateActiveWithoutEndDate,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitEditUpdate',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'editUpdateStatus',
            }),
         ],
      });
   }
}
