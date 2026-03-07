// scripts/pages/itineraryWizard/builder.js
import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';

import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';

import { safeParseJSON } from './storage.js';
import {
   ITIN_KEY,
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   TALKS_KEY,
   WILD_KEY,
} from './keys.js';
import { finalizeItinerary } from './flow.js';

function loadArray( key ) {
   try {
      const raw = localStorage.getItem( key );
      const arr = JSON.parse( raw || '[]' );
      return Array.isArray( arr ) ? arr : [];
   } catch {
      return [];
   }
}

function getDraftState() {
   return {
      dateISO: localStorage.getItem( DATE_KEY ) || '',
      animals: loadArray( ANIMALS_KEY ),
      attractions: loadArray( ATTRACTIONS_KEY ),
      guardiansTalks: loadArray( TALKS_KEY ),
      wildEncounters: loadArray( WILD_KEY ),
   };
}

function snapshotStorage() {
   return {
      [ ITIN_KEY ]: localStorage.getItem( ITIN_KEY ),
      [ DATE_KEY ]: localStorage.getItem( DATE_KEY ),
      [ ANIMALS_KEY ]: localStorage.getItem( ANIMALS_KEY ),
      [ ATTRACTIONS_KEY ]: localStorage.getItem( ATTRACTIONS_KEY ),
      [ TALKS_KEY ]: localStorage.getItem( TALKS_KEY ),
      [ WILD_KEY ]: localStorage.getItem( WILD_KEY ),
   };
}

function restoreStorageSnapshot( snapshot ) {
   Object.entries( snapshot ).forEach( ( [ key, value ] ) => {
      if ( value == null ) {
         localStorage.removeItem( key );
      } else {
         localStorage.setItem( key, value );
      }
   } );
}

function closeBuilder( mountEl, onDone ) {
   if ( mountEl ) {
      mountEl.innerHTML = '';
   }

   onDone?.();
}

export function openItineraryBuilder({ mountEl, startAt = 'date', onDone } = {}) {
   if ( !mountEl ) return;

   const existing = safeParseJSON( localStorage.getItem( ITIN_KEY ) || '', null ) || {};
   let selectedAnimals = Array.isArray( existing.animals ) ? existing.animals : [];
   let selectedAttractions = Array.isArray( existing.attractions ) ? existing.attractions : [];
   let selectedGuardiansTalks = Array.isArray( existing.guardiansTalks ) ? existing.guardiansTalks : [];
   let selectedWildEncounters = Array.isArray( existing.wildEncounters ) ? existing.wildEncounters : [];

   const initialStorageSnapshot = snapshotStorage();
   const initialDraftStateJSON = JSON.stringify( getDraftState() );

   function hasUnsavedChanges() {
      return JSON.stringify( getDraftState() ) !== initialDraftStateJSON;
   }

   function discardAndClose() {
      restoreStorageSnapshot( initialStorageSnapshot );
      closeBuilder( mountEl, onDone );
   }

   const finish = ( override = {} ) =>
      finalizeItinerary(
         {
            animals: override.animals ?? selectedAnimals,
            attractions: override.attractions ?? selectedAttractions,
            guardiansTalks: override.guardiansTalks ?? selectedGuardiansTalks,
            wildEncounters: override.wildEncounters ?? selectedWildEncounters,
         },
         mountEl,
         { onDone }
      );

   function saveDraftAndClose() {
      const draft = getDraftState();

      selectedAnimals = draft.animals;
      selectedAttractions = draft.attractions;
      selectedGuardiansTalks = draft.guardiansTalks;
      selectedWildEncounters = draft.wildEncounters;

      finalizeItinerary(
         {
            animals: draft.animals,
            attractions: draft.attractions,
            guardiansTalks: draft.guardiansTalks,
            wildEncounters: draft.wildEncounters,
         },
         mountEl,
         { onDone }
      );
   }

   function handleClose() {
      if ( !hasUnsavedChanges() ) {
         closeBuilder( mountEl, onDone );
         return;
      }

      showItineraryConfirmPopup({
         title: 'Save Changes?',
         message: 'You have unsaved itinerary changes. Would you like to save them before closing?',
         confirmText: 'Save',
         cancelText: 'Discard',
         onConfirm: () => {
            saveDraftAndClose();
         },
         onCancel: () => {
            discardAndClose();
         },
      });
   }

   const wildEncounterSelector = createItineraryWildEncounterSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => guardiansTalkSelector.show(),
      onFinish: ( wildEncounters ) => {
         selectedWildEncounters = Array.isArray( wildEncounters ) ? wildEncounters : [];
         finish({ wildEncounters: selectedWildEncounters });
      },
   });

   const guardiansTalkSelector = createItineraryGuardiansTalkSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => attractionSelector.show(),
      onNext: ( talks ) => {
         selectedGuardiansTalks = Array.isArray( talks ) ? talks : [];
         wildEncounterSelector.show();
      },
      onFinish: ( talks ) => {
         selectedGuardiansTalks = Array.isArray( talks ) ? talks : [];
         finish({ guardiansTalks: selectedGuardiansTalks });
      },
   });

   const attractionSelector = createItineraryAttractionSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => animalSelector.show(),
      onNext: ( attractions ) => {
         selectedAttractions = Array.isArray( attractions ) ? attractions : [];
         guardiansTalkSelector.show();
      },
      onFinish: ( attractions ) => {
         selectedAttractions = Array.isArray( attractions ) ? attractions : [];
         finish({ attractions: selectedAttractions });
      },
   });

   const animalSelector = createItineraryAnimalSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => dateSelector.show(),
      onNext: ( animals ) => {
         selectedAnimals = Array.isArray( animals ) ? animals : [];
         attractionSelector.show();
      },
      onFinish: ( animals ) => {
         selectedAnimals = Array.isArray( animals ) ? animals : [];
         finish({ animals: selectedAnimals });
      },
   });

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onClose: handleClose,
      onSave: () => animalSelector.show(),
      onFinish: () => finish(),
   });

   switch ( startAt ) {
      case 'animals':
         return animalSelector.show();
      case 'attractions':
         return attractionSelector.show();
      case 'guardiansTalks':
         return guardiansTalkSelector.show();
      case 'wildEncounters':
         return wildEncounterSelector.show();
      case 'date':
      default:
         return dateSelector.show();
   }
}