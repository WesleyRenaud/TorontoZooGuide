import { APP_STRINGS } from '../../../strings.js';
import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
   createTextareaField,
} from '../../templates/fragments.js';

export function createGiftShopClosureOverridePanel() {
   return createPanelShell({
      panelId: 'giftShopClosureOverridePanel',
      title: APP_STRINGS.panelTitles.giftShopClosureOverride,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.giftShop,
            inputId: 'giftShopClosureOverrideGiftShop',
            emptyOptionLabel: APP_STRINGS.placeholders.giftShop,
         }),
         createDateRangeFields({
            startDateId: 'giftShopClosureOverrideStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'giftShopClosureOverrideEndDate',
            endHelpText: APP_STRINGS.help.continueUntilReopened('gift shop'),
         }),
         createTextareaField({
            label: APP_STRINGS.labels.closedMessage,
            inputId: 'giftShopClosureOverrideMessage',
            placeholder: APP_STRINGS.textareas.closedMessage('gift shop'),
         }),
         createActions({
            submitId: 'submitGiftShopClosureOverride',
         }),
         createStatus({
            statusId: 'giftShopClosureOverrideStatus',
         }),
      ],
   });
}
