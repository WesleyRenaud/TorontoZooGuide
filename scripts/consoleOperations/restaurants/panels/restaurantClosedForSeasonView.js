import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestaurantClosedForSeasonView {
   static createRestaurantClosedForSeasonPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'restaurantClosedForSeasonPanel',
         title: Strings.panelTitles.restaurantClosedForSeason,
         entityLabel: Strings.entityLabels.restaurant,
         emptyOptionLabel: Strings.placeholders.restaurant,
         idPrefix: 'restaurantClosedForSeason',
         entityFieldName: 'Restaurant',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('restaurant'),
         messageLabel: Strings.labels.reason,
         messagePlaceholder: Strings.textareas.restaurantClosedForSeasonReason,
         submitId: 'submitRestaurantClosedForSeason',
         statusId: 'restaurantClosedForSeasonStatus',
      });
   }
}
