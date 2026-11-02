import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class AttractionOpenForSeasonView {
   static createAttractionOpenForSeasonPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'attractionOpenForSeasonPanel',
         title: Strings.panelTitles.attractionOpenForSeason,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionOpenForSeason',
         entityFieldName: 'Attraction',
         includeDateRange: false,
         submitId: 'submitAttractionOpenForSeason',
         statusId: 'attractionOpenForSeasonStatus',
      });
   }
}
