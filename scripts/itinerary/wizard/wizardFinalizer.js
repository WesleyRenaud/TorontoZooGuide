import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { normalizeItineraryDraft } from '../draftStorage.js';
import {
   isItineraryEmpty,
   saveItinerary,
} from '../itineraryService.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import { el } from '../panel/dom.js';
import { formatClockTime } from '../panel/format.js';
import { sortScheduledOccurrencesByStartTime } from '../scheduledOccurrenceSort.js';
import {
   createSelectorRowContent,
   createSelectorTextColumn,
} from '../selectors/base/resultRenderer.js';
import { APP_STRINGS } from '../../strings.js';
import {
   buildItineraryWithSelectedWildEncounters,
   getSelectedWildEncounters,
   hasUnresolvedWildEncounterConflictGroups,
   hasWildEncounterConflictSelection,
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

function updateConflictSelectionButtons(buttons, selectedButton) {
   buttons.forEach((button) => {
      const selected = button === selectedButton;

      if (button === selectedButton) {
         button.disabled = false;
      }
      else {
         button.disabled = Boolean(selectedButton);
      }

      button.classList.toggle('is-added', selected);
      button.textContent = selected
         ? APP_STRINGS.itinerary.actions.remove
         : APP_STRINGS.itinerary.actions.addSymbol;
   });
}

function buildWildEncounterImageSrc(name) {
   const file = normalizeAssetKey(name || '');

   return file ? `images/details/wild-encounters/${file}.png` : null;
}

function createWildEncounterSelectButton({
   item,
   selection,
   getButtons,
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
      if (selection.item === item) {
         selection.item = null;
         updateConflictSelectionButtons(getButtons(), null);
         return;
      }

      selection.item = item;
      updateConflictSelectionButtons(getButtons(), button);
   });

   return button;
}

function createWildEncounterConflictSubtitle(item) {
   const subtitle = el('div', 'animal-result-exhibit');
   const time = el(
      'span',
      'itin-panel-time-conflict',
      `Time: ${formatClockTime(item.start_time)}`
   );

   subtitle.append(
      `Meeting Spot: ${item.meeting_spot} • `,
      time
   );

   return subtitle;
}

function createWildEncounterConflictRow({
   item,
   selection,
   getButtons,
} = {}) {
   const row = el('div', 'animal-result itin-save-issue-conflict-row');
   const content = createSelectorRowContent({
      imageSrc: buildWildEncounterImageSrc(item.name),
      imageAlt: APP_STRINGS.itinerary.itemImage(item.name),
      textColumnEl: createSelectorTextColumn({
         title: item.name,
         subtitleNode: createWildEncounterConflictSubtitle(item),
         infoLink: item.link,
      }),
   });
   const button = createWildEncounterSelectButton({
      item,
      selection,
      getButtons,
   });

   row.append(content, button);
   return {
      row,
      button,
   };
}

function createWildEncounterConflictBlock(issue) {
   const selection = { item: null };
   const block = el('div', 'itin-save-issue-conflict');
   const buttons = [];
   const items = sortScheduledOccurrencesByStartTime(issue.items);

   block.appendChild(
      el(
         'p',
         'itin-save-issue-conflict-message',
         APP_STRINGS.itinerary.confirmation.wildEncounterConflictsMessage
      )
   );

   items.forEach((item) => {
      const {
         row,
         button,
      } = createWildEncounterConflictRow({
         item,
         selection,
         getButtons: () => buttons,
      });

      buttons.push(button);
      block.appendChild(row);
   });

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
         APP_STRINGS.itinerary.confirmation.wildEncounterConflictsTitle
      )
   );

   issues.forEach((issue) => {
      const {
         block,
         selection,
      } = createWildEncounterConflictBlock(issue);

      section.appendChild(block);
      conflictGroups.push({ selection });
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

function showConflictProceedConfirmation({
   title,
   message,
   onConfirm,
} = {}) {
   showItineraryConfirmPopup({
      title,
      message,
      confirmText: APP_STRINGS.itinerary.confirmation.saveIssuesButton,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm,
   });
}

function showProceedWithoutConflictSelectionConfirmation({
   title,
   onConfirm,
} = {}) {
   showConflictProceedConfirmation({
      title,
      message: APP_STRINGS.itinerary.confirmation
         .proceedWithoutConflictSelectionMessage,
      onConfirm,
   });
}

function showProceedWithUnresolvedConflictsConfirmation({
   onConfirm,
} = {}) {
   showConflictProceedConfirmation({
      title: APP_STRINGS.itinerary.confirmation
         .proceedWithUnresolvedConflictsTitle,
      message: APP_STRINGS.itinerary.confirmation
         .proceedWithUnresolvedConflictsMessage,
      onConfirm,
   });
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
         showProceedWithoutConflictSelectionConfirmation({
            title: APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle,
            onConfirm: close,
         });
      },
      onConfirm: async ({ close } = {}) => {
         const selectedWildEncounters = getSelectedWildEncounters(conflictGroups);

         if (!hasWildEncounterConflictSelection(conflictGroups)) {
            showProceedWithoutConflictSelectionConfirmation({
               title: APP_STRINGS.itinerary.confirmation
                  .proceedWithoutConflictSelectionTitle,
               onConfirm: close,
            });

            return false;
         }

         if (hasUnresolvedWildEncounterConflictGroups(conflictGroups)) {
            showProceedWithUnresolvedConflictsConfirmation({
               onConfirm: async () => {
                  await saveFinalItinerary(
                     buildItineraryWithSelectedWildEncounters(
                        savedItinerary,
                        selectedWildEncounters
                     )
                  );
                  close();
               },
            });

            return false;
         }

         await saveFinalItinerary(
            buildItineraryWithSelectedWildEncounters(
               savedItinerary,
               selectedWildEncounters
            )
         );
      },
   });
}

function saveFinalItinerary(finalItinerary) {
   return saveItinerary({
      ...finalItinerary,
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
