import { Strings } from '../../../strings.js';
import { ConsoleActionsBuilder } from '../../templates/consoleActionsBuilder.js';
import { ConsoleDateRangeFieldsBuilder } from '../../templates/consoleDateRangeFieldsBuilder.js';
import { ConsolePanelShellBuilder } from '../../templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../templates/consoleStatusBuilder.js';
import { ConsoleTextareaFieldBuilder } from '../../templates/consoleTextareaFieldBuilder.js';

export class GiftShopClosureOverrideView {
   static createGiftShopClosureOverridePanel() {
      return ConsolePanelShellBuilder.createPanelShell({
         panelId: 'giftShopClosureOverridePanel',
         title: Strings.panelTitles.giftShopClosureOverride,
         bodyChildren: [
            ConsoleSelectFieldBuilder.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopClosureOverrideGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            ConsoleDateRangeFieldsBuilder.createDateRangeFields({
               startDateId: 'giftShopClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'giftShopClosureOverrideEndDate',
               endHelpText: Strings.help.continueUntilReopened('gift shop'),
            }),
            ConsoleTextareaFieldBuilder.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'giftShopClosureOverrideMessage',
               placeholder: Strings.textareas.closedMessage('gift shop'),
            }),
            ConsoleActionsBuilder.createActions({
               submitId: 'submitGiftShopClosureOverride',
            }),
            ConsoleStatusBuilder.createStatus({
               statusId: 'giftShopClosureOverrideStatus',
            }),
         ],
      });
   }
}
