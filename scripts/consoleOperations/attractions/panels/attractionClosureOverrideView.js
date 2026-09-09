import { AmenityClosureOverridePanelBuilder } from '../../forms/amenityClosureOverridePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class AttractionClosureOverrideView {
   static createAttractionClosureOverridePanel() {
      return AmenityClosureOverridePanelBuilder.createPanel({
         panelId: 'attractionClosureOverridePanel',
         title: Strings.panelTitles.attractionClosureOverride,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionClosureOverride',
         entityFieldName: 'Attraction',
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('attraction'),
         messageLabel: Strings.labels.closureMessage,
         messagePlaceholder: Strings.textareas.closureMessage,
         submitId: 'submitAttractionClosureOverride',
         statusId: 'attractionClosureOverrideStatus',
      });
   }
}
