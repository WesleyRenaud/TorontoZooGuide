import { AmenityOpeningSchedulePanelBuilder } from '../../forms/amenityOpeningSchedulePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestaurantOpeningScheduleView {
   static createRestaurantOpeningSchedulePanel() {
      return AmenityOpeningSchedulePanelBuilder.createPanel({
         panelId: 'restaurantOpeningSchedulePanel',
         title: Strings.panelTitles.restaurantOpeningSchedule,
         entityLabel: Strings.entityLabels.restaurant,
         emptyOptionLabel: Strings.placeholders.restaurant,
         idPrefix: 'restaurantOpeningSchedule',
         entityFieldName: 'Restaurant',
         scheduleMessagePlaceholder: Strings.textareas.scheduledClosedMessage('restaurant'),
         submitId: 'submitRestaurantOpeningSchedule',
         statusId: 'restaurantOpeningScheduleStatus',
      });
   }
}
