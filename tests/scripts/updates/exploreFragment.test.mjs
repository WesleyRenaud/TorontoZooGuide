import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { ExploreEventView } from '../../../scripts/updates/exploreEventView.js';
import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdateView } from '../../../scripts/updates/exploreUpdateView.js';
import { ExploreUpdatesHelper } from '../../../scripts/updates/exploreUpdatesHelper.js';
import { ExploreUpdatesView } from '../../../scripts/updates/exploreUpdatesView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateExploreUpdates_TestMissingList_ExpectNull', () => {
   assert.equal(ExploreFragment.createExploreUpdates({}), null);
   assert.equal(ExploreFragment.createExploreUpdates(), null);
});

test('Test_CreateExploreUpdates_TestRefreshStepAndTabs_ExpectRender', async () => {
   const visibility = [];
   const tabs = [];
   const collapsed = [];
   const navs = [];
   const toggleEl = document.createElement('button');
   const updatesTabEl = document.createElement('button');
   const eventsTabEl = document.createElement('button');

   const originalVisibility = ExploreUpdatesView.setExploreSectionVisibility;
   const originalTabs = ExploreUpdatesView.syncExploreTabs;
   const originalCollapsed = ExploreUpdatesView.syncExploreCollapsedState;
   const originalNav = ExploreUpdatesView.renderExploreNav;
   const originalClear = ExploreUpdatesView.clearExploreNav;
   const originalHeader = ExploreUpdatesView.getExploreHeaderEl;
   const originalToggle = ExploreUpdatesView.getExploreToggleEl;
   const originalTab = ExploreUpdatesView.getExploreTabEl;
   const originalResolve = ExploreUpdatesHelper.resolveActiveTab;
   const originalPayload = ExploreUpdatesHelper.buildTodayDatePayload;
   const originalUpdateCard = ExploreUpdateView.createUpdateCard;
   const originalEventCard = ExploreEventView.createEventCard;
   const originalUpdates = MapClient.getUpdates;
   const originalEvents = MapClient.getEvents;

   ExploreUpdatesView.setExploreSectionVisibility = (...args) => { visibility.push(args); };
   ExploreUpdatesView.syncExploreTabs = (options) => { tabs.push(options); };
   ExploreUpdatesView.syncExploreCollapsedState = (options) => { collapsed.push(options); };
   ExploreUpdatesView.renderExploreNav = (options) => { navs.push(options); };
   ExploreUpdatesView.clearExploreNav = () => {};
   ExploreUpdatesView.getExploreHeaderEl = () => ({});
   ExploreUpdatesView.getExploreToggleEl = () => toggleEl;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === ExploreFragment.EXPLORE_TAB.UPDATES ? updatesTabEl : eventsTabEl
   );
   ExploreUpdatesHelper.resolveActiveTab = (_active, updates) => (
      updates.length ? ExploreFragment.EXPLORE_TAB.UPDATES : ExploreFragment.EXPLORE_TAB.EVENTS
   );
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
   MapClient.getUpdates = async () => [{ title: 'Notice' }, { title: 'Alert' }];
   MapClient.getEvents = async () => [{ name: 'Concert' }];

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      assert.equal(typeof controller.refresh, 'function');

      ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: null, day: null, year: null });
      await controller.refresh();
      assert.ok(visibility.some((entry) => entry[1] === false));

      ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: 'JUN', day: 1, year: 2026 });
      await controller.refresh();
      assert.equal(listEl.children.length, 3);
      assert.equal(tabs.at(-1).updatesCount, 2);
      assert.equal(navs.at(-1).itemCount, 2);

      navs.at(-1).onStep(1);
      assert.match(listEl.children[1].textContent, /Alert:true/);

      eventsTabEl.click();
      assert.equal(tabs.at(-1).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);
      assert.match(listEl.children[2].textContent, /Concert:true/);

      updatesTabEl.click();
      assert.equal(tabs.at(-1).activeTab, ExploreFragment.EXPLORE_TAB.UPDATES);

      updatesTabEl.click();
      eventsTabEl.click();
      assert.equal(tabs.at(-1).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);

      toggleEl.click();
      assert.equal(collapsed.at(-1).isCollapsed, true);

      MapClient.getUpdates = async () => [];
      MapClient.getEvents = async () => [{ name: 'Show' }, { name: 'Parade' }];
      ExploreUpdatesHelper.resolveActiveTab = () => ExploreFragment.EXPLORE_TAB.EVENTS;
      await controller.refresh();
      assert.equal(tabs.at(-1).activeTab, ExploreFragment.EXPLORE_TAB.EVENTS);
      navs.at(-1).onStep(1);
      assert.match(listEl.children[1].textContent, /Parade:true/);

      MapClient.getUpdates = async () => { throw new Error('fail'); };
      await controller.refresh();
      assert.equal(listEl.children.length, 0);
   } finally {
      ExploreUpdatesView.setExploreSectionVisibility = originalVisibility;
      ExploreUpdatesView.syncExploreTabs = originalTabs;
      ExploreUpdatesView.syncExploreCollapsedState = originalCollapsed;
      ExploreUpdatesView.renderExploreNav = originalNav;
      ExploreUpdatesView.clearExploreNav = originalClear;
      ExploreUpdatesView.getExploreHeaderEl = originalHeader;
      ExploreUpdatesView.getExploreToggleEl = originalToggle;
      ExploreUpdatesView.getExploreTabEl = originalTab;
      ExploreUpdatesHelper.resolveActiveTab = originalResolve;
      ExploreUpdatesHelper.buildTodayDatePayload = originalPayload;
      ExploreUpdateView.createUpdateCard = originalUpdateCard;
      ExploreEventView.createEventCard = originalEventCard;
      MapClient.getUpdates = originalUpdates;
      MapClient.getEvents = originalEvents;
   }
});

test('Test_CreateExploreUpdates_TestTabGuardsAndSingleStep_ExpectNoop', async () => {
   const tabs = [];
   const navs = [];
   const updatesTabEl = document.createElement('button');
   const eventsTabEl = document.createElement('button');

   const originalTabs = ExploreUpdatesView.syncExploreTabs;
   const originalNav = ExploreUpdatesView.renderExploreNav;
   const originalVisibility = ExploreUpdatesView.setExploreSectionVisibility;
   const originalCollapsed = ExploreUpdatesView.syncExploreCollapsedState;
   const originalToggle = ExploreUpdatesView.getExploreToggleEl;
   const originalTab = ExploreUpdatesView.getExploreTabEl;
   const originalResolve = ExploreUpdatesHelper.resolveActiveTab;
   const originalPayload = ExploreUpdatesHelper.buildTodayDatePayload;
   const originalUpdateCard = ExploreUpdateView.createUpdateCard;
   const originalEventCard = ExploreEventView.createEventCard;
   const originalUpdates = MapClient.getUpdates;
   const originalEvents = MapClient.getEvents;

   ExploreUpdatesView.syncExploreTabs = (options) => { tabs.push(options.activeTab); };
   ExploreUpdatesView.renderExploreNav = (options) => { navs.push(options); };
   ExploreUpdatesView.setExploreSectionVisibility = () => {};
   ExploreUpdatesView.syncExploreCollapsedState = () => {};
   ExploreUpdatesView.getExploreToggleEl = () => null;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === ExploreFragment.EXPLORE_TAB.UPDATES ? updatesTabEl : eventsTabEl
   );
   ExploreUpdatesHelper.resolveActiveTab = (tab) => tab;
   ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: 'JUN', day: 1, year: 2026 });
   ExploreUpdateView.createUpdateCard = () => document.createElement('div');
   ExploreEventView.createEventCard = () => document.createElement('div');
   MapClient.getUpdates = async () => [{ title: 'Only' }];
   MapClient.getEvents = async () => [];

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();

      const before = tabs.length;
      eventsTabEl.click();
      updatesTabEl.click();
      assert.equal(tabs.length, before);
      assert.equal(tabs.at(-1), ExploreFragment.EXPLORE_TAB.UPDATES);

      navs.at(-1).onStep(1);
      assert.equal(listEl.children.length, 1);
   } finally {
      ExploreUpdatesView.syncExploreTabs = originalTabs;
      ExploreUpdatesView.renderExploreNav = originalNav;
      ExploreUpdatesView.setExploreSectionVisibility = originalVisibility;
      ExploreUpdatesView.syncExploreCollapsedState = originalCollapsed;
      ExploreUpdatesView.getExploreToggleEl = originalToggle;
      ExploreUpdatesView.getExploreTabEl = originalTab;
      ExploreUpdatesHelper.resolveActiveTab = originalResolve;
      ExploreUpdatesHelper.buildTodayDatePayload = originalPayload;
      ExploreUpdateView.createUpdateCard = originalUpdateCard;
      ExploreEventView.createEventCard = originalEventCard;
      MapClient.getUpdates = originalUpdates;
      MapClient.getEvents = originalEvents;
   }
});

test('Test_CreateExploreUpdates_TestEmptyUpdatesTab_ExpectNoop', async () => {
   const tabs = [];
   const updatesTabEl = document.createElement('button');
   const eventsTabEl = document.createElement('button');

   const originalTabs = ExploreUpdatesView.syncExploreTabs;
   const originalNav = ExploreUpdatesView.renderExploreNav;
   const originalVisibility = ExploreUpdatesView.setExploreSectionVisibility;
   const originalCollapsed = ExploreUpdatesView.syncExploreCollapsedState;
   const originalToggle = ExploreUpdatesView.getExploreToggleEl;
   const originalTab = ExploreUpdatesView.getExploreTabEl;
   const originalResolve = ExploreUpdatesHelper.resolveActiveTab;
   const originalPayload = ExploreUpdatesHelper.buildTodayDatePayload;
   const originalUpdateCard = ExploreUpdateView.createUpdateCard;
   const originalEventCard = ExploreEventView.createEventCard;
   const originalUpdates = MapClient.getUpdates;
   const originalEvents = MapClient.getEvents;

   ExploreUpdatesView.syncExploreTabs = (options) => { tabs.push(options.activeTab); };
   ExploreUpdatesView.renderExploreNav = () => {};
   ExploreUpdatesView.setExploreSectionVisibility = () => {};
   ExploreUpdatesView.syncExploreCollapsedState = () => {};
   ExploreUpdatesView.getExploreToggleEl = () => null;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === ExploreFragment.EXPLORE_TAB.UPDATES ? updatesTabEl : eventsTabEl
   );
   ExploreUpdatesHelper.resolveActiveTab = () => ExploreFragment.EXPLORE_TAB.EVENTS;
   ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: 'JUN', day: 1, year: 2026 });
   ExploreUpdateView.createUpdateCard = () => document.createElement('div');
   ExploreEventView.createEventCard = () => document.createElement('div');
   MapClient.getUpdates = async () => [];
   MapClient.getEvents = async () => [{ name: 'Show' }];

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();

      const before = tabs.length;
      updatesTabEl.click();
      assert.equal(tabs.length, before);
      assert.equal(tabs.at(-1), ExploreFragment.EXPLORE_TAB.EVENTS);
   } finally {
      ExploreUpdatesView.syncExploreTabs = originalTabs;
      ExploreUpdatesView.renderExploreNav = originalNav;
      ExploreUpdatesView.setExploreSectionVisibility = originalVisibility;
      ExploreUpdatesView.syncExploreCollapsedState = originalCollapsed;
      ExploreUpdatesView.getExploreToggleEl = originalToggle;
      ExploreUpdatesView.getExploreTabEl = originalTab;
      ExploreUpdatesHelper.resolveActiveTab = originalResolve;
      ExploreUpdatesHelper.buildTodayDatePayload = originalPayload;
      ExploreUpdateView.createUpdateCard = originalUpdateCard;
      ExploreEventView.createEventCard = originalEventCard;
      MapClient.getUpdates = originalUpdates;
      MapClient.getEvents = originalEvents;
   }
});

test('Test_CreateExploreUpdates_TestInvalidTab_ExpectNoop', async () => {
   const tabs = [];
   const updatesTabEl = document.createElement('button');
   const eventsTabEl = document.createElement('button');
   const originalUpdatesTab = ExploreFragment.EXPLORE_TAB.UPDATES;
   let updatesTabReads = 0;
   let allowInvalidReads = false;

   Object.defineProperty(ExploreFragment.EXPLORE_TAB, 'UPDATES', {
      configurable: true,
      get() {
         updatesTabReads += 1;

         if (!allowInvalidReads || updatesTabReads === 1) {
            return originalUpdatesTab;
         }

         return '__invalid__';
      },
   });

   const originalTabs = ExploreUpdatesView.syncExploreTabs;
   const originalNav = ExploreUpdatesView.renderExploreNav;
   const originalVisibility = ExploreUpdatesView.setExploreSectionVisibility;
   const originalCollapsed = ExploreUpdatesView.syncExploreCollapsedState;
   const originalToggle = ExploreUpdatesView.getExploreToggleEl;
   const originalTab = ExploreUpdatesView.getExploreTabEl;
   const originalResolve = ExploreUpdatesHelper.resolveActiveTab;
   const originalPayload = ExploreUpdatesHelper.buildTodayDatePayload;
   const originalUpdateCard = ExploreUpdateView.createUpdateCard;
   const originalEventCard = ExploreEventView.createEventCard;
   const originalUpdates = MapClient.getUpdates;
   const originalEvents = MapClient.getEvents;

   ExploreUpdatesView.syncExploreTabs = (options) => { tabs.push(options.activeTab); };
   ExploreUpdatesView.renderExploreNav = () => {};
   ExploreUpdatesView.setExploreSectionVisibility = () => {};
   ExploreUpdatesView.syncExploreCollapsedState = () => {};
   ExploreUpdatesView.getExploreToggleEl = () => null;
   ExploreUpdatesView.getExploreTabEl = (_list, tab) => (
      tab === originalUpdatesTab ? updatesTabEl : eventsTabEl
   );
   ExploreUpdatesHelper.resolveActiveTab = () => ExploreFragment.EXPLORE_TAB.EVENTS;
   ExploreUpdatesHelper.buildTodayDatePayload = () => ({ month: 'JUN', day: 1, year: 2026 });
   ExploreUpdateView.createUpdateCard = () => document.createElement('div');
   ExploreEventView.createEventCard = () => document.createElement('div');
   MapClient.getUpdates = async () => [{ title: 'Notice' }];
   MapClient.getEvents = async () => [{ name: 'Show' }];

   try {
      const listEl = document.createElement('div');
      const controller = ExploreFragment.createExploreUpdates({ listEl });
      await controller.refresh();

      allowInvalidReads = true;
      updatesTabReads = 0;

      const before = tabs.length;
      updatesTabEl.click();
      assert.equal(tabs.length, before);
      assert.equal(tabs.at(-1), ExploreFragment.EXPLORE_TAB.EVENTS);
   } finally {
      Object.defineProperty(ExploreFragment.EXPLORE_TAB, 'UPDATES', {
         configurable: true,
         value: originalUpdatesTab,
      });
      ExploreUpdatesView.syncExploreTabs = originalTabs;
      ExploreUpdatesView.renderExploreNav = originalNav;
      ExploreUpdatesView.setExploreSectionVisibility = originalVisibility;
      ExploreUpdatesView.syncExploreCollapsedState = originalCollapsed;
      ExploreUpdatesView.getExploreToggleEl = originalToggle;
      ExploreUpdatesView.getExploreTabEl = originalTab;
      ExploreUpdatesHelper.resolveActiveTab = originalResolve;
      ExploreUpdatesHelper.buildTodayDatePayload = originalPayload;
      ExploreUpdateView.createUpdateCard = originalUpdateCard;
      ExploreEventView.createEventCard = originalEventCard;
      MapClient.getUpdates = originalUpdates;
      MapClient.getEvents = originalEvents;
   }
});
