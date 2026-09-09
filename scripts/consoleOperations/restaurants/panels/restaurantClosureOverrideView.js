import { AmenityClosureOverridePanelBuilder } from '../../forms/amenityClosureOverridePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestaurantClosureOverrideView {
   static createRestaurantClosureOverridePanel() {
      return AmenityClosureOverridePanelBuilder.createPanel({
         panelId: 'restaurantClosureOverridePanel',
         title: Strings.panelTitles.restaurantClosureOverride,
         entityLabel: Strings.entityLabels.restaurant,
         emptyOptionLabel: Strings.placeholders.restaurant,
         idPrefix: 'restaurantClosureOverride',
         entityFieldName: 'Restaurant',
         endHelpText: Strings.help.continueUntilReopened('restaurant'),
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.closedMessage('restaurant'),
         submitId: 'submitRestaurantClosureOverride',
         statusId: 'restaurantClosureOverrideStatus',
      });
   }
}
