import { AnimalsClient } from '../api/animalsClient.js';
import { GuardiansTalkLinkedAnimalNormalizer } from '../guardians/guardiansTalkLinkedAnimalNormalizer.js';
import { AnimalIdentity } from '../itinerary/animalIdentity.js';
import { SpeciesOverlayBuilder } from './speciesOverlayBuilder.js';
import { SpeciesOverlayModal } from './speciesOverlayModal.js';
import { Strings } from '../strings.js';

export class SpeciesFragment {
   static speciesOverlayController = null;

   static initSpeciesOverlay() {
      if (SpeciesFragment.speciesOverlayController) {
         return SpeciesFragment.speciesOverlayController;
      }

      let boundOverlay = null;
      let boundCloseButton = null;
      const state = {
         linkedAnimals: [],
         index: 0,
         isNavigating: false,
         navigationToken: 0,
      };

      const modal = SpeciesOverlayModal.createSpeciesOverlayModal({
         getOverlay: () => SpeciesOverlayBuilder.resolveOverlayElements().overlay,
         getDialog: () => SpeciesOverlayBuilder.resolveOverlayElements().card,
      });

      function isOpen() {
         const { overlay } = SpeciesOverlayBuilder.resolveOverlayElements();

         return Boolean(overlay) && !overlay.classList.contains('hidden');
      }

      function close() {
         const { overlay } = SpeciesOverlayBuilder.resolveOverlayElements();

         modal.deactivate();
         overlay?.classList.add('hidden');
      }

      function handleDocumentKeydown(event) {
         modal.handleKeydown(event);

         if (event.key !== 'Escape' || !isOpen()) {
            return;
         }

         event.preventDefault();
         event.stopPropagation();
         close();
      }

      globalThis.document?.addEventListener?.('keydown', handleDocumentKeydown, true);
      modal.install();

      function bindShell({ overlay, closeButton }) {
         if (boundOverlay !== overlay) {
            boundOverlay = overlay;
            overlay.addEventListener('click', (event) => {
               if (event.target === overlay) {
                  close();
               }
            });
         }

         if (!closeButton || boundCloseButton === closeButton) {
            return;
         }

         boundCloseButton = closeButton;
         closeButton.type = 'button';
         closeButton.setAttribute('aria-label', Strings.common.close);
         closeButton.textContent = Strings.common.closeSymbol;
         closeButton.addEventListener('click', (event) => {
            event.stopPropagation();
            close();
         });
      }

      function render(animal, { preferredFocusSelector = null } = {}) {
         const { overlay, content, closeButton } = SpeciesOverlayBuilder.resolveOverlayElements();

         if (!overlay || !content || !animal) {
            return;
         }

         bindShell({ overlay, closeButton });
         content.replaceChildren(
            SpeciesOverlayBuilder.createOverlayHeader({
               linkedAnimals: state.linkedAnimals,
               index: state.index,
               onNavigate: (delta) => {
                  void navigate(delta);
               },
            }),
            SpeciesOverlayBuilder.createOverlayScrollContent(animal)
         );
         overlay.classList.remove('hidden');

         if (modal.isActive()) {
            modal.activate();
            modal.focusIfLost(
               preferredFocusSelector ? content.querySelector(preferredFocusSelector) : null
            );
         }
      }

      async function navigate(delta) {
         if (state.isNavigating || state.linkedAnimals.length < 2) {
            return;
         }

         const nextIndex = (
            state.index + delta + state.linkedAnimals.length
         ) % state.linkedAnimals.length;
         const token = ++state.navigationToken;

         state.isNavigating = true;

         try {
            const animal = await AnimalsClient.getAnimalInformation(
               state.linkedAnimals[nextIndex]
            );

            if (token !== state.navigationToken || !animal) {
               return;
            }

            state.index = nextIndex;
            render(animal, {
               preferredFocusSelector: delta < 0
                  ? '.species-overlay-nav-prev'
                  : '.species-overlay-nav-next',
            });
         }
         finally {
            if (token === state.navigationToken) {
               state.isNavigating = false;
            }
         }
      }

      function openFromAnimal(animal, options = {}) {
         if (!animal) {
            return;
         }

         state.linkedAnimals = GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(
            options.linkedAnimals
         );
         const matchedIndex = SpeciesOverlayBuilder.findLinkedAnimalIndex(state.linkedAnimals, animal);
         state.index = matchedIndex >= 0 ? matchedIndex : 0;
         state.isNavigating = false;
         state.navigationToken += 1;
         render(animal);

         if (isOpen()) {
            modal.activate({ returnFocusFallback: options.returnFocusFallback ?? null });
         }
      }

      SpeciesFragment.speciesOverlayController = { openFromAnimal, close, isOpen };
      return SpeciesFragment.speciesOverlayController;

   }

   static openAnimalSpeciesOverlay(animal, options = {}) {
      const { species } = AnimalIdentity.normalizeAnimalIdentityFields(animal);

      if (!species) {
         return;
      }

      SpeciesFragment.initSpeciesOverlay().openFromAnimal(animal, options);
   }
}
