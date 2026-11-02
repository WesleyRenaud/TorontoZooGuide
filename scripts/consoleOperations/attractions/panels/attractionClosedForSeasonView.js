import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class AttractionClosedForSeasonView {
   static createAttractionClosedForSeasonPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'attractionClosedForSeasonPanel',
         title: Strings.panelTitles.attractionClosedForSeason,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionClosedForSeason',
         entityFieldName: 'Attraction',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
         messageLabel: Strings.labels.reason,
         messagePlaceholder: Strings.textareas.attractionClosedForSeasonReason,
         submitId: 'submitAttractionClosedForSeason',
         statusId: 'attractionClosedForSeasonStatus',
      });
   }
}
