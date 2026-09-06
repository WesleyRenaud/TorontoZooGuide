import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class GiftShopClosureOverridePanel {
   static createGiftShopClosureOverridePanel() {
      return Fragments.createPanelShell({
         panelId: 'giftShopClosureOverridePanel',
         title: Strings.panelTitles.giftShopClosureOverride,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopClosureOverrideGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'giftShopClosureOverrideStartDate',
               startHelpText: Strings.help.startImmediately,
               endDateId: 'giftShopClosureOverrideEndDate',
               endHelpText: Strings.help.continueUntilReopened('gift shop'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'giftShopClosureOverrideMessage',
               placeholder: Strings.textareas.closedMessage('gift shop'),
            }),
            Fragments.createActions({
               submitId: 'submitGiftShopClosureOverride',
            }),
            Fragments.createStatus({
               statusId: 'giftShopClosureOverrideStatus',
            }),
         ],
      });
   }
}
