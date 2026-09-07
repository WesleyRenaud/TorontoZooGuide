import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class GiftShopClosedPanel {
   static createGiftShopClosedPanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'giftShopClosedPanel',
         title: Strings.panelTitles.giftShopClosed,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopClosedGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'giftShopClosedStartDate',
               endDateId: 'giftShopClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('gift shop'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'giftShopClosedMessage',
               placeholder: Strings.textareas.closedMessage('gift shop'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitGiftShopClosed',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'giftShopClosedStatus',
            }),
         ],
      });
   }
}
