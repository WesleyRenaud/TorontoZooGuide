import { ItineraryPanelDom } from './itineraryPanelDom.js';
import { RowPresentation } from './rowPresentation.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { ScheduleTimeConflictButtonState } from './scheduleTimeConflictButtonState.js';
import { ScheduleTimeConflictContent } from './scheduleTimeConflictContent.js';
import { ResultRenderer } from '../selectors/base/resultRenderer.js';
import { Strings } from '../../strings.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';
import { ScheduleOverrideSelectionConfirmation } from '../wizard/scheduleOverrideSelectionConfirmation.js';

export class ScheduleTimeConflictContentBuilder {
   static refreshConflictSelectionButtons(buttonEntries, selection) {
      buttonEntries.forEach(({ button, item }) => {
         ScheduleTimeConflictButtonState.applyConflictSelectionButtonState(
            button,
            ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, item)
         );
      });
   }

   static handleConflictItemButtonClick(selection, item, buttonEntries) {
      if (ScheduleConflictCompatibility.isConflictItemSelected(selection, item)) {
         ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
         ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
         return;
      }

      if (ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, item)) {
         ScheduleOverrideSelectionConfirmation.showScheduleOverrideSelectionConfirmation({
            onConfirm: () => {
               ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
               ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
            },
         });
         return;
      }

      ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
      ScheduleTimeConflictContentBuilder.refreshConflictSelectionButtons(buttonEntries, selection);
   }

   static createWildEncounterSelectButton({
      item,
      selection,
      buttonEntries,
   } = {}) {
      const button = ItineraryPanelDom.el(
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
      const subtitle = ItineraryPanelDom.el('div', 'animal-result-exhibit');
      const time = ItineraryPanelDom.el(
         'span',
         'itin-panel-time-conflict',
         RowPresentation.buildScheduledTimeFieldLine(item)
      );
      const locationLabel = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
         ? Strings.labels.location
         : Strings.itinerary.selectors.meetingSpot;
      const locationValue = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
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
      const row = ItineraryPanelDom.el('div', 'animal-result itin-save-issue-conflict-row');
      const content = ResultRenderer.createSelectorRowContent({
         imageSrc: ScheduleTimeConflictContent.buildConflictItemImageSrc(item),
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
      const selection = ScheduleConflictCompatibility.createConflictSelection();
      const block = ItineraryPanelDom.el('div', 'itin-save-issue-conflict');
      const buttonEntries = [];
      const items = ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(issue.items);

      block.appendChild(
         ItineraryPanelDom.el(
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
      const section = ItineraryPanelDom.el('section', 'itin-save-issue-section');
      const conflictGroups = [];

      section.appendChild(
         ItineraryPanelDom.el(
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
