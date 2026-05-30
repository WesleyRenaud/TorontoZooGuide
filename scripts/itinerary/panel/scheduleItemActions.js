import { saveItinerary } from '../itineraryService.js';
import {
   cloneItineraryDraft,
   normalizeItineraryDraft,
} from '../itineraryShape.js';
import {
   getAnimalExhibit,
   getAnimalSpecies,
} from '../selectors/animalSelector/model.js';
import { getAttractionName } from '../selectors/attractionSelector/model.js';

function animalKey(animal) {
   return `${animal.species}||${animal.exhibit}`;
}

function itineraryHasAnimal(draft, species, exhibit) {
   return draft.animals.some((animal) => (
      animalKey(animal) === `${species}||${exhibit}`
   ));
}

function itineraryHasAttraction(draft, name) {
   return draft.attractions.some((attraction) => (
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

export async function addAnimalToItinerary(itinerary, row) {
   const entry = buildAnimalDraftEntry(row);

   if (!entry) {
      return itinerary;
   }

   const draft = cloneItineraryDraft(normalizeItineraryDraft(itinerary));

   if (itineraryHasAnimal(draft, entry.species, entry.exhibit)) {
      return saveItinerary(draft);
   }

   draft.animals.push(entry);

   return saveItinerary(draft);
}

export async function addAttractionToItinerary(itinerary, row) {
   const name = buildAttractionDraftEntry(row);

   if (!name) {
      return itinerary;
   }

   const draft = cloneItineraryDraft(normalizeItineraryDraft(itinerary));

   if (itineraryHasAttraction(draft, name)) {
      return saveItinerary(draft);
   }

   draft.attractions.push(name);

   return saveItinerary(draft);
}
