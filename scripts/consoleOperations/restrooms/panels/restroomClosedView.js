import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class RestroomClosedView {
   static createRestroomClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'restroomClosedPanel',
         title: Strings.panelTitles.restroomClosed,
         entityLabel: Strings.entityLabels.restroom,
         emptyOptionLabel: Strings.placeholders.restroom,
         idPrefix: 'restroomClosed',
         entityFieldName: 'Restroom',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.continueUntilReopened('restroom'),
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.closedMessage('restroom'),
         submitId: 'submitRestroomClosed',
         statusId: 'restroomClosedStatus',
      });
   }
}
