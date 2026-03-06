// scripts/itinerary/animalSelector.js
import { normalizeParameter } from '../utils/normalize.js';
import { createItinerarySelectorController } from './selectors/createSelectorController.js';
import { getItineraryDateSearchContext } from './itinerarySearchContext.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';
const DATE_KEY = 'tzg.itineraryDateISO';

function getSpecies(row) {
   return row.SPECIES ?? row.species ?? '';
}

function getExhibit(row) {
   return row.EXHIBIT ?? row.exhibit ?? '';
}

function getSubtitle(row) {
   const exhibit = getExhibit(row);
   return exhibit ? `Exhibit: ${exhibit}` : '';
}

function buildAnimalImageSrc(row) {
   const exhibit = getExhibit(row);
   const species = getSpecies(row);

   const exhibitFile = normalizeParameter(exhibit || '');
   const speciesFile = normalizeParameter(species || '');

   if (!exhibitFile || !speciesFile) return null;
   return `../images/animals/${exhibitFile}/${speciesFile}.png`;
}

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   // Old format: ["Red Panda", "Amur Tiger"]
   if (arr.length > 0 && typeof arr[0] === 'string') {
      return arr
         .filter(Boolean)
         .map(species => ({ id: species, species, exhibit: '', imageSrc: null }));
   }

   return arr
      .filter(x => x && typeof x === 'object')
      .map(x => ({
         id: x.id ?? x.species ?? x.SPECIES ?? '',
         species: x.species ?? x.SPECIES ?? '',
         exhibit: x.exhibit ?? x.EXHIBIT ?? '',
         imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? null,
      }))
      .filter(x => x.id);
}

function makeSelection(row) {
   const species = getSpecies(row);
   const exhibit = getExhibit(row);
   const imageSrc = buildAnimalImageSrc(row);
   return { id: species, species, exhibit, imageSrc };
}

function getMonthDayContext() {
   const iso = localStorage.getItem(DATE_KEY) || '';
   if (!iso) return {};
   const { month, day } = dateISOToMonthDay(iso);
   return { month, day };
}

export function createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish } = {}) {
   return createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      // ✅ adds month/day onto the payload for date-dependent animal queries
      getContext: () => getItineraryDateSearchContext({ includeTemp: true }),

      buildSearchPayload: (query) => ({ query, includeAnimals: true }),
      extractRows: (response) =>
         (Array.isArray(response?.animals) ? response.animals :
          Array.isArray(response) ? response :
          response?.results) || [],

      getId: (row) => getSpecies(row),
      getTitle: (row) => getSpecies(row) || 'Animal',
      getSubtitle: (row) => getSubtitle(row),
      getImageSrc: (row) => buildAnimalImageSrc(row),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Animals',
      subtitle: 'Search and add animals to your plan.',
      emptyText: 'No animals found.',
   });
}