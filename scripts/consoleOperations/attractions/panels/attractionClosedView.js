import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class AttractionClosedView {
   static createAttractionClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'attractionClosedPanel',
         title: Strings.panelTitles.attractionClosed,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionClosed',
         entityFieldName: 'Attraction',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
         messageLabel: Strings.labels.closureMessage,
         messagePlaceholder: Strings.textareas.closureMessage,
         submitId: 'submitAttractionClosed',
         statusId: 'attractionClosedStatus',
      });
   }
}
