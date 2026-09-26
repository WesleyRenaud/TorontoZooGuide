import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdatesChromeHelper } from '../../../scripts/updates/exploreUpdatesChromeHelper.js';
import { ExploreUpdatesView } from '../../../scripts/updates/exploreUpdatesView.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';


function _buildExploreDom() {
   const section = document.createElement('section');
   section.className = 'explore-updates';

   const header = document.createElement('div');
   header.className = 'explore-updates-header';

   const toggle = document.createElement('button');
   toggle.className = 'explore-updates-toggle';

   const updatesTab = document.createElement('button');
   updatesTab.id = 'exploreUpdatesTab';

   const eventsTab = document.createElement('button');
   eventsTab.id = 'exploreEventsTab';

   const listEl = document.createElement('div');
   listEl.className = 'explore-updates-list';

   header.append(toggle, updatesTab, eventsTab);
   section.append(header, listEl);
   document.body.appendChild(section);

   return { section, header, toggle, updatesTab, eventsTab, listEl };
}

installDomTestHooks();


test('Test_GetExploreSectionAndHeader_TestClosest_ExpectNodes', () => {
   const { section, header, toggle, listEl } = _buildExploreDom();

   const foundSection = ExploreUpdatesView.getExploreSectionEl(listEl);
   const foundHeader = ExploreUpdatesView.getExploreHeaderEl(listEl);
   const foundToggle = ExploreUpdatesView.getExploreToggleEl(listEl);

   assert.equal(foundSection, section);
   assert.equal(foundHeader, header);
   assert.equal(foundToggle, toggle);
});


test('Test_GetExploreSectionEl_TestUnrelated_ExpectNull', () => {
   const section = ExploreUpdatesView.getExploreSectionEl(document.createElement('div'));

   assert.equal(section, null);
});


test('Test_GetExploreTabEl_TestUpdates_ExpectButton', () => {
   const { updatesTab, listEl } = _buildExploreDom();

   const tab = ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.UPDATES);

   assert.equal(tab, updatesTab);
});


test('Test_GetExploreTabEl_TestEvents_ExpectButton', () => {
   const { eventsTab, listEl } = _buildExploreDom();

   const tab = ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.EVENTS);

   assert.equal(tab, eventsTab);
});


test('Test_GetExploreTabEl_TestMissing_ExpectNull', () => {
   const tab = ExploreUpdatesView.getExploreTabEl(
      document.createElement('div'),
      ExploreFragment.EXPLORE_TAB.UPDATES
   );

   assert.equal(tab, null);
});


test('Test_SetExploreSectionVisibility_TestHidden_ExpectTrue', () => {
   const { section, listEl } = _buildExploreDom();

   ExploreUpdatesView.setExploreSectionVisibility(listEl, false);

   assert.equal(section.hidden, true);
});


test('Test_SetExploreSectionVisibility_TestVisible_ExpectFalse', () => {
   const { section, listEl } = _buildExploreDom();

   ExploreUpdatesView.setExploreSectionVisibility(listEl, true);

   assert.equal(section.hidden, false);
});


test('Test_SetExploreSectionVisibility_TestMissingSection_ExpectNoOp', () => {
   const set = () => ExploreUpdatesView.setExploreSectionVisibility(document.createElement('div'), true);

   assert.doesNotThrow(set);
});


test('Test_RenderExploreNav_TestSingleItem_ExpectNoNav', () => {
   const { header, listEl } = _buildExploreDom();

   ExploreUpdatesView.renderExploreNav({
      listEl,
      itemCount: Position.SECOND,
      activeTab: ExploreFragment.EXPLORE_TAB.UPDATES,
      onStep: () => {},
   });

   assert.equal(header.querySelector('.explore-update-nav'), null);
});


test('Test_RenderExploreNav_TestMultipleItems_ExpectNav', () => {
   const { header, listEl } = _buildExploreDom();
   const steps = [];
   const originalCreate = ExploreUpdatesChromeHelper.createArrowButton;
   ExploreUpdatesChromeHelper.createArrowButton = ({ onClick, label }) => {
      const button = document.createElement('button');
      button.textContent = label;
      button.addEventListener('click', onClick);
      return button;
   };

   try {
      ExploreUpdatesView.renderExploreNav({
         listEl,
         itemCount: 3,
         activeTab: ExploreFragment.EXPLORE_TAB.UPDATES,
         onStep: (delta) => steps.push(delta),
      });
      const nav = header.querySelector('.explore-update-nav');
      nav.children.at(Position.FIRST).click();
      nav.children.at(Position.SECOND).click();

      assert.ok(nav);
      assert.equal(nav.children.length, 2);
      assert.deepEqual(steps, [Position.LAST, Position.SECOND]);
   } finally {
      ExploreUpdatesChromeHelper.createArrowButton = originalCreate;
   }
});


test('Test_ClearExploreNav_TestExisting_ExpectRemoved', () => {
   const { header, listEl } = _buildExploreDom();
   const originalCreate = ExploreUpdatesChromeHelper.createArrowButton;
   ExploreUpdatesChromeHelper.createArrowButton = ({ onClick, label }) => {
      const button = document.createElement('button');
      button.textContent = label;
      button.addEventListener('click', onClick);
      return button;
   };

   try {
      ExploreUpdatesView.renderExploreNav({
         listEl,
         itemCount: 3,
         activeTab: ExploreFragment.EXPLORE_TAB.UPDATES,
         onStep: () => {},
      });
      ExploreUpdatesView.clearExploreNav(header);

      assert.equal(header.querySelector('.explore-update-nav'), null);
   } finally {
      ExploreUpdatesChromeHelper.createArrowButton = originalCreate;
   }
});


test('Test_SyncExploreCollapsedState_TestCollapsed_ExpectAria', () => {
   const { section, toggle, listEl } = _buildExploreDom();

   ExploreUpdatesView.syncExploreCollapsedState({ listEl, isCollapsed: true });

   assert.equal(section.classList.contains('is-collapsed'), true);
   assert.equal(toggle.getAttribute('aria-label'), Strings.map.showUpdates);
   assert.equal(toggle.getAttribute('aria-expanded'), 'false');
});


test('Test_SyncExploreCollapsedState_TestExpanded_ExpectAria', () => {
   const { section, toggle, listEl } = _buildExploreDom();

   ExploreUpdatesView.syncExploreCollapsedState({ listEl, isCollapsed: false });

   assert.equal(section.classList.contains('is-collapsed'), false);
   assert.equal(toggle.getAttribute('aria-label'), Strings.map.hideUpdates);
   assert.equal(toggle.getAttribute('aria-expanded'), 'true');
});


test('Test_SyncExploreCollapsedState_TestMissingToggle_ExpectSectionOnly', () => {
   const section = document.createElement('section');
   section.className = 'explore-updates';
   const listEl = document.createElement('div');
   section.appendChild(listEl);
   document.body.appendChild(section);

   ExploreUpdatesView.syncExploreCollapsedState({ listEl, isCollapsed: true });

   assert.equal(section.classList.contains('is-collapsed'), true);
});


test('Test_SyncExploreTabs_TestActiveAndDisabled_ExpectState', () => {
   const { updatesTab, eventsTab, listEl } = _buildExploreDom();

   ExploreUpdatesView.syncExploreTabs({
      listEl,
      activeTab: ExploreFragment.EXPLORE_TAB.EVENTS,
      updatesCount: Position.FIRST,
      eventsCount: 2,
   });

   assert.equal(updatesTab.classList.contains('is-active'), false);
   assert.equal(eventsTab.classList.contains('is-active'), true);
   assert.equal(updatesTab.getAttribute('aria-selected'), 'false');
   assert.equal(eventsTab.getAttribute('aria-selected'), 'true');
   assert.equal(updatesTab.disabled, true);
   assert.equal(eventsTab.disabled, false);
});
