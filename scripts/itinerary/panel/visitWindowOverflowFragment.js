import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { Strings } from '../../strings.js';
import { VisitWindowOverflowView } from './visitWindowOverflowView.js';

export class VisitWindowOverflowFragment {
   static showVisitWindowOverflowConfirmation({
      issues = [],
      onConfirm,
      onCancel,
   } = {}) {
      const { content, getKeptItems } = VisitWindowOverflowView.createContent(issues);

      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.visitWindowOverflowTitle,
         bodyContent: content,
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl()
            ?? document.body,
         onConfirm: () => {
            onConfirm?.({
               keptVisitWindowOverflowItems: getKeptItems(),
            });
         },
         onCancel,
      });
   }
}
