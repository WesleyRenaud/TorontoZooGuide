import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class ExhibitClosedView {
   static createExhibitClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'exhibitClosedPanel',
         title: Strings.panelTitles.exhibitClosed,
         entityLabel: Strings.entityLabels.exhibit,
         emptyOptionLabel: Strings.placeholders.exhibit,
         idPrefix: 'exhibitClosed',
         entityFieldName: 'Exhibit',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('exhibit'),
         messageLabel: Strings.labels.closureMessage,
         messagePlaceholder: Strings.textareas.closureMessage,
         submitId: 'submitExhibitClosed',
         statusId: 'exhibitClosedStatus',
      });
   }
}
