import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { ExploreEventView } from '../../../scripts/updates/exploreEventView.js';
import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdateView } from '../../../scripts/updates/exploreUpdateView.js';
import { ExploreUpdatesHelper } from '../../../scripts/updates/exploreUpdatesHelper.js';
import { ExploreUpdatesView } from '../../../scripts/updates/exploreUpdatesView.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _installExploreStubs({
   updates = [{ title: 'Notice' }, { title: 'Alert' }],
   events = [{ name: 'Concert' }],
   resolveActive = (_active, nextUpdates) => (
      nextUpdates.length ? ExploreFragment.EXPLORE_TAB.UPDATES : ExploreFragment.EXPLORE_TAB.EVENTS
   ),
} = {}) {
   const visibility = [];
   const tabs = [];
   const collapsed = [];
   const navs = [];
   const toggleEl = document.createElement('button');
   const updatesTabEl = document.createElement('button');
   const eventsTabEl = document.createElement('button');
   const originals = {
      visibility: ExploreUpdatesView.setExploreSectionVisibility,
      tabs: ExploreUpdatesView.syncExploreTabs,
      collapsed: ExploreUpdatesView.syncExploreCollapsedState,
      nav: ExploreUpdatesView.renderExploreNav,
      clear: ExploreUpdatesView.clearExploreNav,
      header: ExploreUpdatesView.getExploreHeaderEl,
      toggle: ExploreUpdatesView.getExploreToggleEl,
      tab: ExploreUpdatesView.getExploreTabEl,
      resolve: ExploreUpdatesHelper.resolveActiveTab,
      payload: ExploreUpdatesHelper.buildTodayDatePayload,
      updateCard: ExploreUpdateView.createUpdateCard,
      eventCard: ExploreEventView.createEventCard,
      updates: MapClient.getUpdates,
      events: MapClient.getEvents,
   };

   ExploreUpdatesView.setExploreSectionVisibility = (...args) => {
      visibility.push(args);
   };
   ExploreUpdatesView.syncExploreTabs = (options) => {
      tabs.push(options);
   };
   ExploreUpdatesView.syncExploreCollapsedState = (options) => {
      collapsed.push(options);
   };
   ExploreUpdatesView.renderExploreNav = (options) => {
      navs.push(options);
   };
   ExploreUpdatesView.clearExploreNav = () => {};
   ExploreUpdatesView.getExploreHeaderEl = () => ({});
   ExploreUpdatesView.getExploreToggleEl = () => toggleEl;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === ExploreFragment.EXPLORE_TAB.UPDATES ? updatesTabEl : eventsTabEl
   );
   ExploreUpdatesHelper.resolveActiveTab = resolveActive;
   ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: 'JUN', day: 1, year: 2026 });
   ExploreUpdateView.createUpdateCard = (update, active) => {
      const el = document.createElement('div');
      el.textContent = `${update.title}:${active}`;
      return el;
   };
   ExploreEventView.createEventCard = (event, active) => {
      const el = document.createElement('div');
      el.textContent = `${event.name}:${active}`;
      return el;
   };
   MapClient.getUpdates = async () => updates;
   MapClient.getEvents = async () => events;

   return {
      visibility,
      tabs,
      collapsed,
      navs,
      toggleEl,
      updatesTabEl,
      eventsTabEl,
      restore() {
         ExploreUpdatesView.setExploreSectionVisibility = originals.visibility;
         ExploreUpdatesView.syncExploreTabs = originals.tabs;
         ExploreUpdatesView.syncExploreCollapsedState = originals.collapsed;
         ExploreUpdatesView.renderExploreNav = originals.nav;
         ExploreUpdatesView.clearExploreNav = originals.clear;
         ExploreUpdatesView.getExploreHeaderEl = originals.header;
         ExploreUpdatesView.getExploreToggleEl = originals.toggle;
         ExploreUpdatesView.getExploreTabEl = originals.tab;
         ExploreUpdatesHelper.resolveActiveTab = originals.resolve;
         ExploreUpdatesHelper.buildTodayDatePayload = originals.payload;
         ExploreUpdateView.createUpdateCard = originals.updateCard;
         ExploreEventView.createEventCard = originals.eventCard;
         MapClient.getUpdates = originals.updates;
         MapClient.getEvents = originals.events;
      },
   };
}


test('Test_CreateExploreUpdates_TestMissingList_ExpectNull', () => {
   const controller = ExploreFragment.createExploreUpdates({});

   assert.equal(controller, null);
});


test('Test_CreateExploreUpdates_TestMissingOptions_ExpectNull', () => {
   const controller = ExploreFragment.createExploreUpdates();

   assert.equal(controller, null);
});


test('Test_CreateExploreUpdates_TestMissingDate_ExpectHidden', async () => {
   const stubs = _installExploreStubs();

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: null, day: null, year: null });
      await controller.refresh();

      assert.ok(stubs.visibility.some((entry) => entry.at(Position.SECOND) === false));
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestRefresh_ExpectCards', async () => {
   const stubs = _installExploreStubs();
   const expectedCount = 3;

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();

      assert.equal(listEl.children.length, expectedCount);
      assert.equal(stubs.tabs.at(Position.LAST).updatesCount, 2);
      assert.equal(stubs.navs.at(Position.LAST).itemCount, 2);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestStepAndTabs_ExpectActive', async () => {
   const stubs = _installExploreStubs();

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();
      stubs.navs.at(Position.LAST).onStep(1);
      const alertActive = listEl.children.at(Position.SECOND).textContent;
      stubs.eventsTabEl.click();
      stubs.updatesTabEl.click();
      stubs.toggleEl.click();

      assert.match(alertActive, /Alert:true/);
      assert.equal(stubs.collapsed.at(Position.LAST).isCollapsed, true);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestEventsRefresh_ExpectParade', async () => {
   const stubs = _installExploreStubs({
      updates: [],
      events: [{ name: 'Show' }, { name: 'Parade' }],
      resolveActive: () => ExploreFragment.EXPLORE_TAB.EVENTS,
   });

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();
      stubs.navs.at(Position.LAST).onStep(1);

      assert.equal(stubs.tabs.at(Position.LAST).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);
      assert.match(listEl.children.at(Position.SECOND).textContent, /Parade:true/);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestFetchFailure_ExpectCleared', async () => {
   const stubs = _installExploreStubs();

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      MapClient.getUpdates = async () => {
         throw new Error('fail');
      };
      await controller.refresh();

      assert.equal(listEl.children.length, Position.FIRST);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestTabGuardsAndSingleStep_ExpectNoop', async () => {
   const stubs = _installExploreStubs({
      updates: [{ title: 'Only' }],
      events: [],
      resolveActive: (tab) => tab,
   });
   ExploreUpdatesView.getExploreToggleEl = () => null;

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();
      const before = stubs.tabs.length;
      stubs.eventsTabEl.click();
      stubs.updatesTabEl.click();
      stubs.navs.at(Position.LAST).onStep(1);

      assert.equal(stubs.tabs.length, before);
      assert.equal(stubs.tabs.at(Position.LAST).activeTab, ExploreFragment.EXPLORE_TAB.UPDATES);
      assert.equal(listEl.children.length, Position.SECOND);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestEmptyUpdatesTab_ExpectNoop', async () => {
   const stubs = _installExploreStubs({
      updates: [],
      events: [{ name: 'Show' }],
      resolveActive: () => ExploreFragment.EXPLORE_TAB.EVENTS,
   });
   ExploreUpdatesView.getExploreToggleEl = () => null;

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();
      const before = stubs.tabs.length;
      stubs.updatesTabEl.click();

      assert.equal(stubs.tabs.length, before);
      assert.equal(stubs.tabs.at(Position.LAST).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);
   } finally {
      stubs.restore();
   }
});


test('Test_CreateExploreUpdates_TestInvalidTab_ExpectNoop', async () => {
   const originalUpdatesTab = ExploreFragment.EXPLORE_TAB.UPDATES;
   let updatesTabReads = 0;
   let allowInvalidReads = false;
   Object.defineProperty(ExploreFragment.EXPLORE_TAB, 'UPDATES', {
      configurable: true,
      get() {
         updatesTabReads += 1;
         if (!allowInvalidReads || updatesTabReads === Position.SECOND) {
            return originalUpdatesTab;
         }

         return '__invalid__';
      },
   });
   const stubs = _installExploreStubs({
      updates: [{ title: 'Notice' }],
      events: [{ name: 'Show' }],
      resolveActive: () => ExploreFragment.EXPLORE_TAB.EVENTS,
   });
   ExploreUpdatesView.getExploreToggleEl = () => null;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === originalUpdatesTab ? stubs.updatesTabEl : stubs.eventsTabEl
   );

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();
      allowInvalidReads = true;
      updatesTabReads = 0;
      const before = stubs.tabs.length;
      stubs.updatesTabEl.click();

      assert.equal(stubs.tabs.length, before);
      assert.equal(stubs.tabs.at(Position.LAST).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);
   } finally {
      Object.defineProperty(ExploreFragment.EXPLORE_TAB, 'UPDATES', {
         configurable: true,
         value: originalUpdatesTab,
      });
      stubs.restore();
   }
});
