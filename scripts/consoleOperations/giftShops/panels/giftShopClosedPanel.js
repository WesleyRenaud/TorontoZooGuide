import { Strings } from '../../../strings.js';
import { Fragments } from '../../templates/fragments.js';

export class GiftShopClosedPanel {
   static createGiftShopClosedPanel() {
      return Fragments.createPanelShell({
         panelId: 'giftShopClosedPanel',
         title: Strings.panelTitles.giftShopClosed,
         bodyChildren: [
            Fragments.createSelectField({
               label: Strings.entityLabels.giftShop,
               inputId: 'giftShopClosedGiftShop',
               emptyOptionLabel: Strings.placeholders.giftShop,
            }),
            Fragments.createDateRangeFields({
               startDateId: 'giftShopClosedStartDate',
               endDateId: 'giftShopClosedEndDate',
               endHelpText: Strings.help.continueUntilReopened('gift shop'),
            }),
            Fragments.createTextareaField({
               label: Strings.labels.closedMessage,
               inputId: 'giftShopClosedMessage',
               placeholder: Strings.textareas.closedMessage('gift shop'),
            }),
            Fragments.createActions({
               submitId: 'submitGiftShopClosed',
            }),
            Fragments.createStatus({
               statusId: 'giftShopClosedStatus',
            }),
         ],
      });
   }
}
