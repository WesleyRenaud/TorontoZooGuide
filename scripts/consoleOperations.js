import { createAnimalOffDisplayController } from './consoleOperations/animalOffDisplay.js';
import { createAnimalOnDisplayController } from './consoleOperations/animalOnDisplay.js';
import { createAnimalSpeciesAutocompleteController } from './consoleOperations/animalSpeciesAutocomplete.js';

const offDisplayPanel = document.getElementById('offDisplayPanel');
const onDisplayPanel = document.getElementById('onDisplayPanel');

const offDisplaySpeciesEl = document.getElementById('offDisplaySpecies');
const onDisplaySpeciesEl = document.getElementById('onDisplaySpecies');

const offDisplaySpeciesResults = document.getElementById('offDisplaySpeciesResults');
const onDisplaySpeciesResults = document.getElementById('onDisplaySpeciesResults');

const offDisplayExhibitEl = document.getElementById('offDisplayExhibit');
const onDisplayExhibitEl = document.getElementById('onDisplayExhibit');

function activatePanel(panelEl) {
   document
      .querySelectorAll('.console-operations-panel')
      .forEach(panel => panel.classList.remove('active'));

   panelEl?.classList.add('active');

   document
      .querySelectorAll('.console-operations-menu-btn')
      .forEach((button) => {
         button.classList.toggle(
            'active',
            button.dataset.panelTarget === panelEl?.id
         );
      });
}

function hidePanels() {
   document
      .querySelectorAll('.console-operations-panel')
      .forEach(panel => panel.classList.remove('active'));

   document
      .querySelectorAll('.console-operations-menu-btn')
      .forEach(button => button.classList.remove('active'));
}

createAnimalSpeciesAutocompleteController({
   inputEl: offDisplaySpeciesEl,
   resultsEl: offDisplaySpeciesResults,
   exhibitEl: offDisplayExhibitEl,
});

createAnimalSpeciesAutocompleteController({
   inputEl: onDisplaySpeciesEl,
   resultsEl: onDisplaySpeciesResults,
   exhibitEl: onDisplayExhibitEl,
});

createAnimalOffDisplayController({
   showButtonEl: document.getElementById('showOffDisplayForm'),
   panelEl: offDisplayPanel,
   cancelButtonEl: null,
   submitButtonEl: document.getElementById('submitOffDisplay'),
   statusEl: document.getElementById('offDisplayStatus'),
   speciesEl: offDisplaySpeciesEl,
   exhibitEl: offDisplayExhibitEl,
   messageEl: document.getElementById('offDisplayMessage'),
   activatePanel,
   hidePanels,
});

createAnimalOnDisplayController({
   showButtonEl: document.getElementById('showOnDisplayForm'),
   panelEl: onDisplayPanel,
   cancelButtonEl: null,
   submitButtonEl: document.getElementById('submitOnDisplay'),
   statusEl: document.getElementById('onDisplayStatus'),
   speciesEl: onDisplaySpeciesEl,
   exhibitEl: onDisplayExhibitEl,
   activatePanel,
   hidePanels,
});