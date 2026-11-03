import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestaurantOpenForSeasonView {
   static createRestaurantOpenForSeasonPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'restaurantOpenForSeasonPanel',
         title: Strings.panelTitles.restaurantOpenForSeason,
         entityLabel: Strings.entityLabels.restaurant,
         emptyOptionLabel: Strings.placeholders.restaurant,
         idPrefix: 'restaurantOpenForSeason',
         entityFieldName: 'Restaurant',
         includeDateRange: false,
         submitId: 'submitRestaurantOpenForSeason',
         statusId: 'restaurantOpenForSeasonStatus',
      });
   }
}
