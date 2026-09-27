import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
import { RowPresenter } from './rowPresenter.js';
import { ResultRenderer } from '../selectors/base/resultRenderer.js';
import { ItinerarySaveIssueItemType } from '../../shared/enums/itinerarySaveIssueItemType.js';
import { ItineraryVisitWindowOverflowEnd } from '../../shared/enums/itineraryVisitWindowOverflowEnd.js';
import { Strings } from '../../strings.js';
import { VisitWindowOverflowKeepItems } from './visitWindowOverflowKeepItems.js';

export class VisitWindowOverflowView {
   static imageDirectoryForItem(item = {}) {
      if (item.item_type === ItinerarySaveIssueItemType.ATTRACTION) {
         return 'attractions';
      }

      if (item.item_type === ItinerarySaveIssueItemType.WILD_ENCOUNTER) {
         return 'wild-encounters';
      }

      return 'guardians-talks';
   }


   static buildItemImageSrc(item) {
      return RowPresenter.buildImageSrc(
         VisitWindowOverflowView.imageDirectoryForItem(item),
         item?.name
      );
   }


   static overflowEndLabel(item = {}, strings = Strings) {
      const confirmation = strings.itinerary.confirmation;

      if (item.overflow_end === ItineraryVisitWindowOverflowEnd.ARRIVAL) {
         return confirmation.visitWindowOverflowArrivalEnd;
      }

      if (item.overflow_end === ItineraryVisitWindowOverflowEnd.DEPARTURE) {
         return confirmation.visitWindowOverflowDepartureEnd;
      }

      if (item.overflow_end === ItineraryVisitWindowOverflowEnd.BOTH) {
         return confirmation.visitWindowOverflowBothEnds;
      }

      return '';
   }


   static createItemSubtitle(item, strings = Strings) {
      const subtitle = ItineraryPanelHelper.el('div', 'animal-result-exhibit');
      const time = ItineraryPanelHelper.el(
         'span',
         'itin-panel-time-conflict',
         RowPresenter.buildScheduledTimeFieldLine(item)
      );
      const overflowEndLabel = VisitWindowOverflowView.overflowEndLabel(item, strings);

      subtitle.append(time);

      if (overflowEndLabel) {
         subtitle.append(
            strings.format.bulletSeparator,
            overflowEndLabel
         );
      }

      return subtitle;
   }


   static applyKeepButtonState(button, keptItemKeys, item, strings = Strings) {
      const kept = VisitWindowOverflowKeepItems.isKept(keptItemKeys, item);

      button.classList.toggle('is-added', kept);
      button.textContent = kept
         ? strings.itinerary.actions.remove
         : strings.itinerary.actions.addSymbol;
      button.setAttribute(
         'aria-label',
         kept
            ? strings.itinerary.aria.removeFromItinerary
            : strings.itinerary.aria.addToItinerary
      );
   }


   static createKeepButton({
      item,
      keptItemKeys,
      buttons,
      strings = Strings,
   } = {}) {
      const button = ItineraryPanelHelper.el(
         'button',
         'itin-add-btn itin-save-issue-select-btn is-added',
         strings.itinerary.actions.remove
      );

      button.type = 'button';
      VisitWindowOverflowView.applyKeepButtonState(button, keptItemKeys, item, strings);
      button.addEventListener('click', () => {
         VisitWindowOverflowKeepItems.toggleKeep(keptItemKeys, item);
         buttons.forEach((keepButton) => {
            VisitWindowOverflowView.applyKeepButtonState(
               keepButton.button,
               keptItemKeys,
               keepButton.item,
               strings
            );
         });
      });

      return button;
   }


   static createItemRow({
      item,
      keptItemKeys,
      buttons,
      strings = Strings,
   } = {}) {
      const row = ItineraryPanelHelper.el('div', 'animal-result itin-save-issue-conflict-row');
      const button = VisitWindowOverflowView.createKeepButton({
         item,
         keptItemKeys,
         buttons,
         strings,
      });
      const content = ResultRenderer.createSelectorRowContent({
         imageSrc: VisitWindowOverflowView.buildItemImageSrc(item),
         imageAlt: strings.itinerary.itemImage(item.name),
         textColumnEl: ResultRenderer.createSelectorTextColumn({
            title: item.name,
            subtitleNode: VisitWindowOverflowView.createItemSubtitle(item, strings),
            infoLink: item.link,
         }),
      });

      row.append(content, button);
      buttons.push({ button, item });
      return row;
   }


   static createContent(issues = [], strings = Strings) {
      const items = VisitWindowOverflowKeepItems.overflowItemsFromIssues(issues);
      const keptItemKeys = VisitWindowOverflowKeepItems.createKeptItemKeys(items);
      const content = ItineraryPanelHelper.el('div', 'itin-save-issues');
      const buttons = [];

      content.appendChild(
         ItineraryPanelHelper.el(
            'p',
            'itin-save-issue-conflict-message',
            strings.itinerary.confirmation.visitWindowOverflowMessage
         )
      );

      items.forEach((item) => {
         content.appendChild(
            VisitWindowOverflowView.createItemRow({
               item,
               keptItemKeys,
               buttons,
               strings,
            })
         );
      });

      return {
         content,
         getKeptItems: () => VisitWindowOverflowKeepItems.keptWiresFromKeys(
            items,
            keptItemKeys
         ),
      };
   }
}
