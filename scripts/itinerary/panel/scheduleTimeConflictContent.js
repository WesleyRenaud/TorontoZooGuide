import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { el } from './dom.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import {
   applyConflictSelectionButtonState,
   getConflictSelectionButtonState,
} from './scheduleTimeConflictButtonState.js';
import {
   createSelectorRowContent,
   createSelectorTextColumn,
} from '../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../strings.js';
import {
   conflictItemRequiresTrimOverride,
   createConflictSelection,
   isConflictItemSelected,
   toggleConflictItemSelection,
} from '../wizard/scheduleConflictCompatibility.js';
import { showScheduleOverrideSelectionConfirmation } from '../wizard/scheduleOverrideSelectionConfirmation.js';
import {
   isGuardiansTalkConflictItem,
   sortWildEncounterConflictIssuesByStartTime,
} from '../wizard/wildEncounterConflictResolution.js';

export const WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict';

function refreshConflictSelectionButtons(buttonEntries, selection) {
   buttonEntries.forEach(({ button, item }) => {
      applyConflictSelectionButtonState(
         button,
         getConflictSelectionButtonState(selection, item)
      );
   });
}

function handleConflictItemButtonClick(selection, item, buttonEntries) {
   if (isConflictItemSelected(selection, item)) {
      toggleConflictItemSelection(selection, item);
      refreshConflictSelectionButtons(buttonEntries, selection);
      return;
   }

   if (conflictItemRequiresTrimOverride(selection, item)) {
      showScheduleOverrideSelectionConfirmation({
         onConfirm: () => {
            toggleConflictItemSelection(selection, item);
            refreshConflictSelectionButtons(buttonEntries, selection);
         },
      });
      return;
   }

   toggleConflictItemSelection(selection, item);
   refreshConflictSelectionButtons(buttonEntries, selection);
}

export function buildConflictItemImageSrc(item) {
   const file = normalizeAssetKey(item?.name || '');

   if (!file) {
      return null;
   }

   const directory = isGuardiansTalkConflictItem(item)
      ? 'guardians-talks'
      : 'wild-encounters';

   return `images/details/${directory}/${file}.png`;
}

function createWildEncounterSelectButton({
   item,
   selection,
   buttonEntries,
} = {}) {
   const button = el(
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
   const subtitle = el('div', 'animal-result-exhibit');
   const time = el(
      'span',
      'itin-panel-time-conflict',
      `Time: ${buildScheduledOccurrenceTimeRange(item)}`
   );
   const locationLabel = isGuardiansTalkConflictItem(item)
      ? APP_STRINGS.labels.location
      : APP_STRINGS.itinerary.selectors.meetingSpot;
   const locationValue = isGuardiansTalkConflictItem(item)
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
   const row = el('div', 'animal-result itin-save-issue-conflict-row');
   const content = createSelectorRowContent({
      imageSrc: buildConflictItemImageSrc(item),
      imageAlt: APP_STRINGS.itinerary.itemImage(item.name),
      textColumnEl: createSelectorTextColumn({
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
   const selection = createConflictSelection();
   const block = el('div', 'itin-save-issue-conflict');
   const buttonEntries = [];
   const items = sortScheduledOccurrencesByStartTime(issue.items);

   block.appendChild(
      el(
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
   const section = el('section', 'itin-save-issue-section');
   const conflictGroups = [];

   section.appendChild(
      el(
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

export function createSaveIssuesContent(issues) {
   const content = el('div', 'itin-save-issues');
   const wildEncounterConflictIssues = issues.filter(
      issue => issue?.type === WILD_ENCOUNTER_TIME_CONFLICT
   );
   let conflictGroups = [];

   if (wildEncounterConflictIssues.length) {
      const sectionResult = createWildEncounterConflictSection(
         sortWildEncounterConflictIssuesByStartTime(
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
