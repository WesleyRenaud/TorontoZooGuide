export const SELECTED_EXHIBITS_KEY = 'tzg.itinerarySelectedExhibits';
export const SELECTED_REGIONS_KEY = 'tzg.itinerarySelectedRegions';

export function loadSelectedNames(storageKey) {
   try {
      const raw = localStorage.getItem(storageKey);
      const parsed = JSON.parse(raw || '[]');
      return Array.isArray(parsed) ? parsed.filter(Boolean) : [];
   } catch {
      return [];
   }
}

export function saveSelectedNames(storageKey, names) {
   localStorage.setItem(storageKey, JSON.stringify(Array.from(names)));
}