import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { normalizeItineraryDraft } from '../draftStorage.js';
import {
   isItineraryEmpty,
   saveItinerary,
} from '../itineraryService.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import { el } from '../panel/dom.js';
import { showSaveIssuesProceedConfirmation } from './saveIssuesProceedConfirmation.js';
import {
   canSelectConflictItem,
   conflictItemRequiresTrimOverride,
   createConflictSelection,
   hasAnyAdditionalSelectableConflictItems,
   isConflictItemSelected,
   toggleConflictItemSelection,
} from './scheduleConflictCompatibility.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import { buildScheduledOccurrenceTimeRange } from '../scheduledOccurrenceTimeRange.js';
import { showScheduleOverrideSelectionConfirmation } from './scheduleOverrideSelectionConfirmation.js';
import {
   createSelectorRowContent,
   createSelectorTextColumn,
} from '../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../strings.js';
import {
   buildItineraryWithSelectedConflictResolutions,
   getSelectedConflictItems,
   hasUnresolvedWildEncounterConflictGroups,
   hasWildEncounterConflictSelection,
   isGuardiansTalkConflictItem,
   sortWildEncounterConflictIssuesByStartTime,
} from './wildEncounterConflictResolution.js';
import { showItineraryWizardPopup } from './wizardPopup.js';

const WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict';

const EMPTY_SELECTION_POPUP_CONFIG = Object.freeze({
   title: APP_STRINGS.itinerary.noItemsSelected.title,
   message: APP_STRINGS.itinerary.noItemsSelected.message,
   buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
});

function clearWizardMount(mountEl) {
   mountEl?.replaceChildren();
}

function createFinalItineraryDraft(draft = {}) {
   return normalizeItineraryDraft(draft);
}

function shouldBlockEmptyFinish(finalItinerary, allowEmpty = false) {
   return !allowEmpty && isItineraryEmpty(finalItinerary);
}

function showEmptySelectionPopup(mountEl) {
   showItineraryWizardPopup({
      mountEl,
      ...EMPTY_SELECTION_POPUP_CONFIG,
   });
}

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

function createSaveIssuesContent(issues) {
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

function showSaveIssuesPopup(savedItinerary) {
   const issues = savedItinerary.saveIssues;

   if (!issues.length) {
      return;
   }

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
            onConfirm: close,
         });
      },
      onConfirm: async ({ close } = {}) => {
         const selectedConflictItems = getSelectedConflictItems(conflictGroups);

         if (!hasWildEncounterConflictSelection(conflictGroups)) {
            showSaveIssuesProceedConfirmation({
               title: APP_STRINGS.itinerary.confirmation
                  .proceedWithoutConflictSelectionTitle,
               message: APP_STRINGS.itinerary.confirmation
                  .proceedWithoutConflictSelectionMessage,
               onConfirm: close,
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
                  await saveFinalItinerary(
                     buildItineraryWithSelectedConflictResolutions(
                        savedItinerary,
                        selectedConflictItems
                     ),
                     { overridingConflictingGuardiansTalks: true },
                  );
                  close();
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
                  await saveFinalItinerary(
                     buildItineraryWithSelectedConflictResolutions(
                        savedItinerary,
                        selectedConflictItems
                     ),
                     { overridingConflictingGuardiansTalks: true },
                  );
                  close();
               },
            });

            return false;
         }

         await saveFinalItinerary(
            buildItineraryWithSelectedConflictResolutions(
               savedItinerary,
               selectedConflictItems
            ),
            { overridingConflictingGuardiansTalks: true },
         );
      },
   });
}

function saveFinalItinerary(
   finalItinerary,
   { overridingConflictingGuardiansTalks = false } = {},
) {
   return saveItinerary(finalItinerary, {
      overridingConflictingGuardiansTalks,
   });
}

export async function finalizeItineraryWizard(
   draft = {},
   mountEl,
   { onDone, allowEmpty = false } = {}
) {
   const finalItinerary = createFinalItineraryDraft(draft);

   if (shouldBlockEmptyFinish(finalItinerary, allowEmpty)) {
      showEmptySelectionPopup(mountEl);
      return null;
   }

   const savedItinerary = await saveFinalItinerary(finalItinerary);

   if (savedItinerary.saveIssues?.length) {
      showSaveIssuesPopup(savedItinerary);
   }

   clearWizardMount(mountEl);

   onDone?.();

   return savedItinerary;
}
