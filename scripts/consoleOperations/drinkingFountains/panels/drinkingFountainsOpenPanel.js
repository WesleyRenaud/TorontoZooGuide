import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';

export class DrinkingFountainsOpenPanel {
   static createDrinkingFountainsOpenPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'drinkingFountainsOpenPanel',
         title: Strings.panelTitles.drinkingFountainsOpen,
         bodyChildren: [
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'drinkingFountainsOpenStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'drinkingFountainsOpenEndDate',
               endHelpText: Strings.help.keepExplicitlyOpenUntilChanged('drinking fountains', 'they are'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitDrinkingFountainsOpen',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'drinkingFountainsOpenStatus',
            }),
         ],
      });
   }
}
