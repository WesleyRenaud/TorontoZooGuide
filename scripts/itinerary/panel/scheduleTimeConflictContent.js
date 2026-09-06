import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { Dom } from './dom.js';
import { RowPresentation } from './rowPresentation.js';
import { ScheduledOccurrenceSort } from '../scheduledOccurrenceSort.js';
import { ScheduleTimeConflictButtonState } from './scheduleTimeConflictButtonState.js';
import { ResultRenderer } from '../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../strings.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';
import { ScheduleOverrideSelectionConfirmation } from '../wizard/scheduleOverrideSelectionConfirmation.js';
import { WildEncounterConflictResolution } from '../wizard/wildEncounterConflictResolution.js';

function refreshConflictSelectionButtons(buttonEntries, selection) {
   buttonEntries.forEach(({ button, item }) => {
      ScheduleTimeConflictButtonState.applyConflictSelectionButtonState(
         button,
         ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, item)
      );
   });
}

function handleConflictItemButtonClick(selection, item, buttonEntries) {
   if (ScheduleConflictCompatibility.isConflictItemSelected(selection, item)) {
      ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
      refreshConflictSelectionButtons(buttonEntries, selection);
      return;
   }

   if (ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, item)) {
      ScheduleOverrideSelectionConfirmation.showScheduleOverrideSelectionConfirmation({
         onConfirm: () => {
            ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
            refreshConflictSelectionButtons(buttonEntries, selection);
         },
      });
      return;
   }

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, item);
   refreshConflictSelectionButtons(buttonEntries, selection);
}

function createWildEncounterSelectButton({
   item,
   selection,
   buttonEntries,
} = {}) {
   const button = Dom.el(
      'button',
      'itin-add-btn itin-save-issue-select-btn',
      APP_STRINGS.itinerary.actions.addSymbol
   );

   button.type = 'button';
   button.setAttribute(
      'aria-label',
      APP_STRINGS.itinerary.aria.addToItinerary
   );

   button.addEventListener('click', () => {
      handleConflictItemButtonClick(selection, item, buttonEntries);
   });

   return button;
}

function createScheduleConflictSubtitle(item) {
   const subtitle = Dom.el('div', 'animal-result-exhibit');
   const time = Dom.el(
      'span',
      'itin-panel-time-conflict',
      RowPresentation.buildScheduledTimeFieldLine(item)
   );
   const locationLabel = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
      ? APP_STRINGS.labels.location
      : APP_STRINGS.itinerary.selectors.meetingSpot;
   const locationValue = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
      ? item.location
      : item.meeting_spot;

   subtitle.append(
      `${locationLabel}: ${locationValue} • `,
      time
   );

   return subtitle;
}

function createWildEncounterConflictRow({
   item,
   selection,
   buttonEntries,
} = {}) {
   const row = Dom.el('div', 'animal-result itin-save-issue-conflict-row');
   const content = ResultRenderer.createSelectorRowContent({
      imageSrc: ScheduleTimeConflictContent.buildConflictItemImageSrc(item),
      imageAlt: APP_STRINGS.itinerary.itemImage(item.name),
      textColumnEl: ResultRenderer.createSelectorTextColumn({
         title: item.name,
         subtitleNode: createScheduleConflictSubtitle(item),
         infoLink: item.link,
      }),
   });
   const button = createWildEncounterSelectButton({
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

function createWildEncounterConflictBlock(issue) {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const block = Dom.el('div', 'itin-save-issue-conflict');
   const buttonEntries = [];
   const items = ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(issue.items);

   block.appendChild(
      Dom.el(
         'p',
         'itin-save-issue-conflict-message',
         APP_STRINGS.itinerary.confirmation.scheduleConflictsMessage
      )
   );

   items.forEach((item) => {
      const { row, button, item: rowItem } = createWildEncounterConflictRow({
         item,
         selection,
         buttonEntries,
      });

      buttonEntries.push({ button, item: rowItem });
      block.appendChild(row);
   });

   refreshConflictSelectionButtons(buttonEntries, selection);

   return {
      block,
      selection,
   };
}

function createWildEncounterConflictSection(issues) {
   const section = Dom.el('section', 'itin-save-issue-section');
   const conflictGroups = [];

   section.appendChild(
      Dom.el(
         'h3',
         'itin-save-issue-section-title',
         APP_STRINGS.itinerary.confirmation.scheduleConflictsTitle
      )
   );

   issues.forEach((issue) => {
      const {
         block,
         selection,
      } = createWildEncounterConflictBlock(issue);

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

export class ScheduleTimeConflictContent {
   static WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict';

   static buildConflictItemImageSrc(item) {
      const file = AssetKeyNormalizer.normalize(item?.name || '');

      if (!file) {
         return null;
      }

      const directory = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
         ? 'guardians-talks'
         : 'wild-encounters';

      return `images/details/${directory}/${file}.png`;

   }

   static createSaveIssuesContent(issues) {
      const content = Dom.el('div', 'itin-save-issues');
      const wildEncounterConflictIssues = issues.filter(
         issue => issue?.type === ScheduleTimeConflictContent.WILD_ENCOUNTER_TIME_CONFLICT
      );
      let conflictGroups = [];

      if (wildEncounterConflictIssues.length) {
         const sectionResult = createWildEncounterConflictSection(
            WildEncounterConflictResolution.sortWildEncounterConflictIssuesByStartTime(
               wildEncounterConflictIssues
            )
         );

         content.appendChild(sectionResult.section);
         conflictGroups = sectionResult.conflictGroups;
      }

      return {
         content,
         conflictGroups,
      };
   }
}
