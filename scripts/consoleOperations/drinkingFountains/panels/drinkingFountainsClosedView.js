import { GlobalAmenityStatusPanelBuilder } from '../../forms/globalAmenityStatusPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class DrinkingFountainsClosedView {
   static createDrinkingFountainsClosedPanel() {
      return GlobalAmenityStatusPanelBuilder.createPanel({
         panelId: 'drinkingFountainsClosedPanel',
         title: Strings.panelTitles.drinkingFountainsClosed,
         idPrefix: 'drinkingFountainsClosed',
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('drinking fountains'),
         includeMessage: true,
         messageLabel: Strings.labels.reason,
         messagePlaceholder: Strings.textareas.drinkingFountainsClosedForSeasonReason,
         submitId: 'submitDrinkingFountainsClosed',
         statusId: 'drinkingFountainsClosedStatus',
      });
   }
}
