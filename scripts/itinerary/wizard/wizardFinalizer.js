import { normalizeItineraryDraft } from '../draftStorage.js';
import {
   isItineraryEmpty,
   saveItinerary,
} from '../itineraryService.js';
import { showItineraryNoticePopup } from '../panel/components/noticePopup.js';
import { el } from '../panel/dom.js';
import { buildWildRows } from '../panel/rows.js';
import { APP_STRINGS } from '../../strings.js';
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

function createWildEncounterConflictBlock(issue) {
   const block = el('div', 'itin-save-issue-conflict');

   block.append(...buildWildRows(issue.items, true));

   return block;
}

function createWildEncounterConflictSection(issues) {
   const section = el('section', 'itin-save-issue-section');
   section.appendChild(
      el(
         'h3',
         'itin-save-issue-section-title',
         APP_STRINGS.itinerary.confirmation.wildEncounterConflictsTitle
      )
   );

   issues.forEach((issue) => {
      section.appendChild(createWildEncounterConflictBlock(issue));
   });

   return section;
}

function createSaveIssuesContent(issues) {
   const content = el('div', 'itin-save-issues');
   const wildEncounterConflictIssues = issues.filter(
      issue => issue?.type === WILD_ENCOUNTER_TIME_CONFLICT
   );

   if (wildEncounterConflictIssues.length) {
      content.appendChild(
         createWildEncounterConflictSection(wildEncounterConflictIssues)
      );
   }

   return content;
}

function showSaveIssuesPopup(issues = []) {
   if (!issues.length) {
      return;
   }

   showItineraryNoticePopup({
      title: APP_STRINGS.itinerary.confirmation.saveIssuesTitle,
      bodyContent: createSaveIssuesContent(issues),
      buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
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
      showSaveIssuesPopup(savedItinerary.saveIssues);
   }

   clearWizardMount(mountEl);

   onDone?.();

   return savedItinerary;
}
