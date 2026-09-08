import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class DrinkingFountainsClosedView {
   static createDrinkingFountainsClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         bodyChildren: [
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'drinkingFountainsClosedStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'drinkingFountainsClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened(
                  'drinking fountains'
               ),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'drinkingFountainsClosedMessage',
               placeholder: Strings.textareas.drinkingFountainsClosedMessage,
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitDrinkingFountainsClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'drinkingFountainsClosedStatus',
            }),
         ],
      });
   }
}
