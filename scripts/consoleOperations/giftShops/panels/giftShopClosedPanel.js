import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export class GiftShopClosedPanel {
   static createGiftShopClosedPanel() {
      return createPanelShell({
         panelId: 'giftShopClosedPanel',
         title: APP_STRINGS.panelTitles.giftShopClosed,
         bodyChildren: [
            createSelectField({
               label: APP_STRINGS.entityLabels.giftShop,
               inputId: 'giftShopClosedGiftShop',
               emptyOptionLabel: APP_STRINGS.placeholders.giftShop,
            }),
            createDateRangeFields({
               startDateId: 'giftShopClosedStartDate',
               endDateId: 'giftShopClosedEndDate',
               endHelpText: APP_STRINGS.help.continueUntilReopened('gift shop'),
            }),
            createTextareaField({
               label: APP_STRINGS.labels.closedMessage,
               inputId: 'giftShopClosedMessage',
               placeholder: APP_STRINGS.textareas.closedMessage('gift shop'),
            }),
            createActions({
               submitId: 'submitGiftShopClosed',
            }),
            createStatus({
               statusId: 'giftShopClosedStatus',
            }),
         ],
      });
   }
}
