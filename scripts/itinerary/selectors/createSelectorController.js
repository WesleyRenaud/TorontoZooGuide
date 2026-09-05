import { ResultRenderer } from './base/resultRenderer.js';
import { SelectionState } from './base/selectionState.js';
import { SelectorControllerConfig } from './selectorControllerConfig.js';
import { SelectorControllerElements } from './selectorControllerElements.js';
import { SelectorSearchRunner } from './selectorSearchRunner.js';
import { APP_STRINGS } from '../../strings.js';

export function createItinerarySelectorController({
   mountEl,

   onPrev,
   onNext,
   onFinish,
   onClose,
   hideNextButton = false,

   storageKey,
   migrateSelected = SelectorControllerConfig.defaultMigrateSelected,

   searchEndpoint = '/search',
   buildSearchPayload = query => ({ query }),
   extractRows,

   getContext = null,

   getId,
   getTitle = () => '',
   getSubtitle = () => '',
   getImageSrc = () => null,
   getInfoLink = () => null,
   onTitleClick = null,
   shouldEnableTitleClick = null,

   makeSelection = row => ({ id: getId(row) }),

   topTitle = APP_STRINGS.itinerary.selectors.builderTitle,
   h1 = APP_STRINGS.itinerary.selectors.defaultTitle,
   subtitle = APP_STRINGS.itinerary.selectors.defaultSubtitle,
   emptyText = APP_STRINGS.itinerary.emptyText.results,

   renderRowLeft,
   renderExtraControls = null,

   onBeforeToggleAdd = null,

   deps = {},
} = {}) {
   const {
      buildElements = SelectorControllerElements.createSelectorElements,
      createSearchRunner = SelectorSearchRunner.createSelectorSearchRunner,
   } = deps;

   SelectorControllerConfig.validateSelectorConfig({
      storageKey,
      getId,
      extractRows,
   });

   let elements = null;

   const selectionState = SelectionState.createSelectorSelectionState({
      storageKey,
      migrateSelected,
      getId,
      makeSelection,
   });

   const resolvedRenderRowLeft = renderRowLeft
      || ResultRenderer.createDefaultSelectorRowLeftRenderer({
         getTitle,
         getSubtitle,
         getImageSrc,
         getInfoLink: onTitleClick ? () => null : getInfoLink,
         onTitleClick,
         shouldEnableTitleClick,
      });

   function getSelectionSnapshot() {
      return selectionState.getSelectedSnapshot();
   }

   function renderRows(rows) {
      if (!elements?.resultsEl) {
         return;
      }

      ResultRenderer.renderSelectorResults({
         resultsEl: elements.resultsEl,
         rows,
         emptyText,
         getId,
         isSelected: selectionState.isSelected,
         renderRowLeft: resolvedRenderRowLeft,
         onToggle: selectionState.toggleRow,
         onBeforeToggleAdd,
      });
   }

   const searchRunner = createSearchRunner({
      searchEndpoint,
      buildSearchPayload,
      extractRows,
      getContext,
      getQuery: () => elements?.inputEl?.value ?? '',
      onRows: renderRows,
   });

   let selectionFingerprintAtShow = '';

   function shouldSkipClosingSelectionSync() {
      return SelectorControllerConfig.buildSelectionFingerprint(selectionState.getSelectedSnapshot())
         === selectionFingerprintAtShow;
   }

   function handlePrev() {
      onPrev?.(getSelectionSnapshot());
   }

   function handleNext() {
      onNext?.(getSelectionSnapshot());
   }

   function handleFinish() {
      onFinish?.(getSelectionSnapshot());
   }

   function handleClose() {
      onClose?.();
   }

   function bindEvents() {
      elements?.inputEl?.addEventListener('input', searchRunner.scheduleCurrentQuery);
      elements?.prevButtonEl?.addEventListener('click', handlePrev);
      elements?.nextButtonEl?.addEventListener('click', handleNext);
      elements?.finishButtonEl?.addEventListener('click', handleFinish);
      elements?.closeButtonEl?.addEventListener('click', handleClose);
   }

   function renderExtraUi() {
      if (typeof renderExtraControls !== 'function' || !elements) {
         return;
      }

      renderExtraControls({
         rootEl: elements.rootEl,
         bodyEl: elements.bodyEl,
         inputEl: elements.inputEl,
         resultsEl: elements.resultsEl,
         rerunSearch: () => {
            void searchRunner.runCurrentQuery();
         },
      });
   }

   function ensureBuilt() {
      if (elements) {
         return;
      }

      elements = buildElements({
         topTitle,
         h1,
         subtitle,
         hideNextButton,
      });

      renderExtraUi();
      bindEvents();
   }

   function resetInput() {
      if (!elements?.inputEl) {
         return;
      }

      elements.inputEl.value = '';
   }

   function mountRoot() {
      if (!mountEl || !elements?.rootEl) {
         return;
      }

      mountEl.replaceChildren(elements.rootEl);
   }

   function show() {
      if (!mountEl) {
         return;
      }

      ensureBuilt();
      selectionState.reload();
      selectionFingerprintAtShow = SelectorControllerConfig.buildSelectionFingerprint(
         selectionState.getSelectedSnapshot()
      );
      mountRoot();
      resetInput();
      void searchRunner.runCurrentQuery();
   }

   function hide() {
      if (!mountEl) {
         return;
      }

      mountEl.replaceChildren();
   }

   return {
      show,
      hide,
      getSelectionSnapshot,
      shouldSkipClosingSelectionSync,
   };
}
