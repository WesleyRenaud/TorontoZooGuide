import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestaurantClosedView {
   static createRestaurantClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'restaurantClosedPanel',
         title: Strings.panelTitles.restaurantClosed,
         entityLabel: Strings.entityLabels.restaurant,
         emptyOptionLabel: Strings.placeholders.restaurant,
         idPrefix: 'restaurantClosed',
         entityFieldName: 'Restaurant',
         endHelpText: Strings.help.continueUntilReopened('restaurant'),
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.closedMessage('restaurant'),
         submitId: 'submitRestaurantClosed',
         statusId: 'restaurantClosedStatus',
      });
   }
}
