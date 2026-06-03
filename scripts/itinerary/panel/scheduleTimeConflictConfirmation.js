import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { showItineraryNoticePopup } from './components/noticePopup.js';
import { el } from './dom.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import {
   createSelectorRowContent,
   createSelectorTextColumn,
} from '../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../strings.js';
import { showSaveIssuesProceedConfirmation } from '../wizard/saveIssuesProceedConfirmation.js';
import {
   canSelectConflictItem,
   conflictItemRequiresTrimOverride,
   createConflictSelection,
   hasAnyAdditionalSelectableConflictItems,
   isConflictItemSelected,
   toggleConflictItemSelection,
} from '../wizard/scheduleConflictCompatibility.js';
import { showScheduleOverrideSelectionConfirmation } from '../wizard/scheduleOverrideSelectionConfirmation.js';
import {
   getSelectedConflictItems,
   hasUnresolvedWildEncounterConflictGroups,
   hasWildEncounterConflictSelection,
   isGuardiansTalkConflictItem,
   sortWildEncounterConflictIssuesByStartTime,
} from '../wizard/wildEncounterConflictResolution.js';

export const WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict';

function refreshConflictSelectionButtons(buttonEntries, selection) {
   buttonEntries.forEach(({ button, item }) => {
      const selected = isConflictItemSelected(selection, item);
      const selectable = canSelectConflictItem(selection, item);
      const requiresTrimOverride = conflictItemRequiresTrimOverride(selection, item);

      button.disabled = !selected && !selectable;
      button.classList.toggle('is-added', selected);
      button.classList.toggle(
         'requires-trim-override',
         requiresTrimOverride
      );
      button.textContent = selected
         ? APP_STRINGS.itinerary.actions.remove
         : APP_STRINGS.itinerary.actions.addSymbol;
      button.setAttribute(
         'aria-label',
         selected
            ? (
               requiresTrimOverride
                  ? APP_STRINGS.itinerary.aria
                     .removeFromItineraryWithScheduleOverride
                  : APP_STRINGS.itinerary.aria.removeFromItinerary
            )
            : (
               requiresTrimOverride
                  ? APP_STRINGS.itinerary.aria
                     .addToItineraryWithScheduleOverride
                  : APP_STRINGS.itinerary.aria.addToItinerary
            )
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

function buildConflictItemImageSrc(item) {
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

async function resolveScheduleTimeConflictSelection(
   conflictGroups,
   onResolved,
) {
   const selectedConflictItems = getSelectedConflictItems(conflictGroups);

   if (!hasWildEncounterConflictSelection(conflictGroups)) {
      showSaveIssuesProceedConfirmation({
         title: APP_STRINGS.itinerary.confirmation
            .proceedWithoutConflictSelectionTitle,
         message: APP_STRINGS.itinerary.confirmation
            .proceedWithoutConflictSelectionMessage,
         onConfirm: () => {},
      });

      return false;
   }

   if (hasUnresolvedWildEncounterConflictGroups(conflictGroups)) {
      showSaveIssuesProceedConfirmation({
         title: APP_STRINGS.itinerary.confirmation
            .proceedWithUnresolvedConflictsTitle,
         message: APP_STRINGS.itinerary.confirmation
            .proceedWithUnresolvedConflictsMessage,
         onConfirm: async () => {
            await onResolved(selectedConflictItems);
         },
      });

      return false;
   }

   if (hasAnyAdditionalSelectableConflictItems(conflictGroups)) {
      showSaveIssuesProceedConfirmation({
         title: APP_STRINGS.itinerary.confirmation
            .proceedWithAdditionalSelectableActivitiesTitle,
         message: APP_STRINGS.itinerary.confirmation
            .proceedWithAdditionalSelectableActivitiesMessage,
         onConfirm: async () => {
            await onResolved(selectedConflictItems);
         },
      });

      return false;
   }

   await onResolved(selectedConflictItems);
   return true;
}

export function showScheduleTimeConflictConfirmation({
   issues = [],
   onConfirm,
   onCancel,
} = {}) {
   const {
      content,
      conflictGroups,
   } = createSaveIssuesContent(issues);

   showItineraryNoticePopup({
      title: APP_STRINGS.itinerary.confirmation.saveIssuesTitle,
      bodyContent: content,
      buttonText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
      showCloseButton: true,
      onClose: ({ close } = {}) => {
         showSaveIssuesProceedConfirmation({
            title: APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle,
            message: APP_STRINGS.itinerary.confirmation
               .proceedWithoutConflictSelectionMessage,
            onConfirm: () => {
               onCancel?.();
               close();
            },
         });
      },
      onConfirm: async ({ close } = {}) => {
         const resolved = await resolveScheduleTimeConflictSelection(
            conflictGroups,
            async (selectedConflictItems) => {
               await onConfirm?.(selectedConflictItems);
               close();
            }
         );

         if (!resolved) {
            return false;
         }

         return true;
      },
   });
}

export async function confirmSaveIssuesConflictSelection(conflictGroups, onResolved) {
   return resolveScheduleTimeConflictSelection(conflictGroups, onResolved);
}
