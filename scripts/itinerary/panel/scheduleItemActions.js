import {
   scheduleItineraryItemRequest,
   setItineraryRequest,
} from '../../api/itineraryApi.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
} from '../itineraryErrorTypes.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import {
   cloneItineraryDraft,
   normalizeItineraryDraft,
   toSetItineraryPayload,
} from '../itineraryShape.js';
import {
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from './scheduleItemSearch.js';
import {
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   SCHEDULE_ITEM_MODULE_TYPES,
} from './scheduleItemTypes.js';
import {
   getAnimalExhibit,
   getAnimalSpecies,
} from '../selectors/animalSelector/model.js';
import { getAttractionName } from '../selectors/attractionSelector/model.js';
import { SELECTED_EXHIBITS_KEY } from '../storageKeys.js';

function animalKey(species, exhibit) {
   return `${species}||${exhibit}`;
}

function itineraryHasAnimal(itinerary, species, exhibit) {
   return (itinerary?.animals ?? []).some((animal) => (
      animalKey(animal.species, animal.exhibit) === animalKey(species, exhibit)
   ));
}

function itineraryHasAttraction(itinerary, name) {
   return (itinerary?.attractions ?? []).some((attraction) => (
      String(attraction) === name
   ));
}

export function buildAnimalDraftEntry(row) {
   const species = getAnimalSpecies(row);
   const exhibit = getAnimalExhibit(row);

   if (!species || !exhibit) {
      return null;
   }

   return { species, exhibit };
}

export function buildAttractionDraftEntry(row) {
   const name = getAttractionName(row);

   return name || null;
}

export function buildScheduleItemRequest(selection, selectedRow, eventTypes = []) {
   if (isScheduleItemEventType(selection, eventTypes)) {
      return {
         itemType: selection,
         key: '',
      };
   }

   if (!isScheduleItemSearchEnabled(selection, eventTypes) || !selectedRow) {
      return null;
   }

   return {
      itemType: getScheduleItemRowKind(selectedRow),
      key: getScheduleItemRowId(selectedRow),
   };
}

function loadSelectedExhibits() {
   try {
      const selectedExhibits = JSON.parse(
         localStorage.getItem(SELECTED_EXHIBITS_KEY) || '[]'
      );

      return Array.isArray(selectedExhibits)
         ? selectedExhibits
            .map((exhibit) => String(exhibit ?? '').trim())
            .filter(Boolean)
         : [];
   }
   catch {
      return [];
   }
}

async function saveItineraryDraft(draft) {
   const savePayload = toSetItineraryPayload(draft);
   const { temp } = await getItineraryDateSearchContext({ date: savePayload.date });

   return setItineraryRequest({
      ...savePayload,
      selectedExhibits: loadSelectedExhibits(),
      temp,
   });
}

async function ensureScheduleItemOnItinerary(
   itinerary,
   selection,
   selectedRow,
   eventTypes = []
) {
   const successType = getItineraryErrorTypes()?.SUCCESS ?? 'success';

   if (!isScheduleItemSearchEnabled(selection, eventTypes) || !selectedRow) {
      return { errorType: successType };
   }

   if (getScheduleItemRowKind(selectedRow) === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
      const name = buildAttractionDraftEntry(selectedRow);

      if (!name || itineraryHasAttraction(itinerary, name)) {
         return { errorType: successType };
      }

      const draft = cloneItineraryDraft(normalizeItineraryDraft(itinerary));
      draft.attractions.push(name);

      const saveResult = await saveItineraryDraft(draft);

      return { errorType: saveResult.errorType };
   }

   const entry = buildAnimalDraftEntry(selectedRow);

   if (!entry || itineraryHasAnimal(itinerary, entry.species, entry.exhibit)) {
      return { errorType: successType };
   }

   const draft = cloneItineraryDraft(normalizeItineraryDraft(itinerary));
   draft.animals.push(entry);

   const saveResult = await saveItineraryDraft(draft);

   return { errorType: saveResult.errorType };
}

export async function scheduleSelectedItineraryItem(
   itinerary,
   selection,
   selectedRow,
   eventTypes = []
) {
   const effectiveSelection = resolveEffectiveScheduleItemSelection(
      selection,
      selectedRow
   );

   const ensureResult = await ensureScheduleItemOnItinerary(
      itinerary,
      effectiveSelection,
      selectedRow,
      eventTypes
   );

   if (!isItinerarySuccess(ensureResult.errorType)) {
      return ensureResult;
   }

   const request = buildScheduleItemRequest(
      effectiveSelection,
      selectedRow,
      eventTypes
   );

   if (!request) {
      return {
         errorType: getItineraryErrorTypes()?.SAVE_FAILED ?? 'saveFailed',
      };
   }

   return scheduleItineraryItemRequest(request);
}
