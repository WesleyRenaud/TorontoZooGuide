import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
import { RowPresenter } from './rowPresenter.js';
import { ScheduledOccurrenceSorter } from '../scheduledOccurrenceSorter.js';
import { ScheduleTimeConflictButtonStore } from './scheduleTimeConflictButtonStore.js';
import { ScheduleTimeConflictView } from './scheduleTimeConflictView.js';
import { ResultRenderer } from '../selectors/base/resultRenderer.js';
import { Strings } from '../../strings.js';
import { ScheduleConflictChecker } from '../wizard/scheduleConflictChecker.js';
import { ScheduleOverrideSelectionFragment } from '../wizard/scheduleOverrideSelectionFragment.js';

export class ScheduleTimeConflictContentBuilder {
   static refreshConflictSelectionButtons(buttonEntries, selection) {
      buttonEntries.forEach(({ button, item }) => {
         ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState(
            button,
            ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, item)
         );
      });
   }

   static handleConflictItemButtonClick(selection, item, buttonEntries) {
      if (ScheduleConflictChecker.isConflictItemSelected(selection, item)) {
         ScheduleConflictChecker.toggleConflictItemSelection(selection, item);
         ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
         return;
      }

      if (ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, item)) {
         ScheduleOverrideSelectionFragment.showScheduleOverrideSelectionConfirmation({
            onConfirm: () => {
               ScheduleConflictChecker.toggleConflictItemSelection(selection, item);
               ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
            },
         });
         return;
      }

      ScheduleConflictChecker.toggleConflictItemSelection(selection, item);
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
   }

   static createWildEncounterSelectButton({
      item,
      selection,
      buttonEntries,
   } = {}) {
      const button = ItineraryPanelHelper.el(
         'button',
         'itin-add-btn itin-save-issue-select-btn',
         Strings.itinerary.actions.addSymbol
      );

      button.type = 'button';
      button.setAttribute(
         'aria-label',
         Strings.itinerary.aria.addToItinerary
      );

      button.addEventListener('click', () => {
         ScheduleTimeConflictContentBuilder.handleConflictItemButtonClick(selection, item, buttonEntries);
      });

      return button;
   }

   static createScheduleConflictSubtitle(item) {
      const subtitle = ItineraryPanelHelper.el('div', 'animal-result-exhibit');
      const time = ItineraryPanelHelper.el(
         'span',
         'itin-panel-time-conflict',
         RowPresenter.buildScheduledTimeFieldLine(item)
      );
      const locationLabel = ScheduleConflictChecker.isGuardiansTalkConflictItem(item)
         ? Strings.labels.location
         : Strings.itinerary.selectors.meetingSpot;
      const locationValue = ScheduleConflictChecker.isGuardiansTalkConflictItem(item)
         ? item.location
         : item.meeting_spot;

      subtitle.append(
         `${locationLabel}: ${locationValue} • `,
         time
      );

      return subtitle;
   }

   static createWildEncounterConflictRow({
      item,
      selection,
      buttonEntries,
   } = {}) {
      const row = ItineraryPanelHelper.el('div', 'animal-result itin-save-issue-conflict-row');
      const content = ResultRenderer.createSelectorRowContent({
         imageSrc: ScheduleTimeConflictView.buildConflictItemImageSrc(item),
         imageAlt: Strings.itinerary.itemImage(item.name),
         textColumnEl: ResultRenderer.createSelectorTextColumn({
            title: item.name,
            subtitleNode: ScheduleTimeConflictContentBuilder.createScheduleConflictSubtitle(item),
            infoLink: item.link,
         }),
      });
      const button = ScheduleTimeConflictContentBuilder.createWildEncounterSelectButton({
         item,
         selection,
         buttonEntries,
      });

      row.append(content, button);
      return {
         row,
         button,
         item,
      };
   }

   static createWildEncounterConflictBlock(issue) {
      const selection = ScheduleConflictChecker.createConflictSelection();
      const block = ItineraryPanelHelper.el('div', 'itin-save-issue-conflict');
      const buttonEntries = [];
      const items = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(issue.items);

      block.appendChild(
         ItineraryPanelHelper.el(
            'p',
            'itin-save-issue-conflict-message',
            Strings.itinerary.confirmation.scheduleConflictsMessage
         )
      );

      items.forEach((item) => {
         const { row, button, item: rowItem } = ScheduleTimeConflictContentBuilder.createWildEncounterConflictRow({
            item,
            selection,
            buttonEntries,
         });

         buttonEntries.push({ button, item: rowItem });
         block.appendChild(row);
      });

      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);

      return {
         block,
         selection,
      };
   }

   static createWildEncounterConflictSection(issues) {
      const section = ItineraryPanelHelper.el('section', 'itin-save-issue-section');
      const conflictGroups = [];

      section.appendChild(
         ItineraryPanelHelper.el(
            'h3',
            'itin-save-issue-section-title',
            Strings.itinerary.confirmation.scheduleConflictsTitle
         )
      );

      issues.forEach((issue) => {
         const {
            block,
            selection,
         } = ScheduleTimeConflictContentBuilder.createWildEncounterConflictBlock(issue);

         section.appendChild(block);
         conflictGroups.push({
            selection,
            items: issue.items,
         });
      });

      return {
         section,
         conflictGroups,
      };
   }
}
