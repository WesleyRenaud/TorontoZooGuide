import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdatesChromeHelper } from '../../../scripts/updates/exploreUpdatesChromeHelper.js';
import { ExploreUpdatesView } from '../../../scripts/updates/exploreUpdatesView.js';
import { Strings } from '../../../scripts/strings.js';
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

   assert.equal(ExploreUpdatesView.getExploreSectionEl(listEl), section);
   assert.equal(ExploreUpdatesView.getExploreHeaderEl(listEl), header);
   assert.equal(ExploreUpdatesView.getExploreToggleEl(listEl), toggle);
   assert.equal(ExploreUpdatesView.getExploreSectionEl(document.createElement('div')), null);
});

test('Test_GetExploreTabEl_TestTabs_ExpectButtons', () => {
   const { updatesTab, eventsTab, listEl } = _buildExploreDom();

   assert.equal(
      ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.UPDATES),
      updatesTab
   );
   assert.equal(
      ExploreUpdatesView.getExploreTabEl(listEl, ExploreFragment.EXPLORE_TAB.EVENTS),
      eventsTab
   );
   assert.equal(
      ExploreUpdatesView.getExploreTabEl(document.createElement('div'), ExploreFragment.EXPLORE_TAB.UPDATES),
      null
   );
});

test('Test_SetExploreSectionVisibility_TestFlag_ExpectHidden', () => {
   const { section, listEl } = _buildExploreDom();

   ExploreUpdatesView.setExploreSectionVisibility(listEl, false);
   assert.equal(section.hidden, true);
   ExploreUpdatesView.setExploreSectionVisibility(listEl, true);
   assert.equal(section.hidden, false);
   ExploreUpdatesView.setExploreSectionVisibility(document.createElement('div'), true);
});

test('Test_RenderExploreNav_TestItemCount_ExpectNavOrCleared', () => {
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
         itemCount: 1,
         activeTab: ExploreFragment.EXPLORE_TAB.UPDATES,
         onStep: (delta) => steps.push(delta),
      });
      assert.equal(header.querySelector('.explore-update-nav'), null);

      ExploreUpdatesView.renderExploreNav({
         listEl,
         itemCount: 3,
         activeTab: ExploreFragment.EXPLORE_TAB.UPDATES,
         onStep: (delta) => steps.push(delta),
      });

      const nav = header.querySelector('.explore-update-nav');
      assert.ok(nav);
      assert.equal(nav.children.length, 2);
      nav.children[0].click();
      nav.children[1].click();
      assert.deepEqual(steps, [-1, 1]);

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

   ExploreUpdatesView.syncExploreCollapsedState({ listEl, isCollapsed: false });
   assert.equal(section.classList.contains('is-collapsed'), false);
   assert.equal(toggle.getAttribute('aria-label'), Strings.map.hideUpdates);
   assert.equal(toggle.getAttribute('aria-expanded'), 'true');
});

test('Test_SyncExploreTabs_TestActiveAndDisabled_ExpectState', () => {
   const { updatesTab, eventsTab, listEl } = _buildExploreDom();

   ExploreUpdatesView.syncExploreTabs({
      listEl,
      activeTab: ExploreFragment.EXPLORE_TAB.EVENTS,
      updatesCount: 0,
      eventsCount: 2,
   });

   assert.equal(updatesTab.classList.contains('is-active'), false);
   assert.equal(eventsTab.classList.contains('is-active'), true);
   assert.equal(updatesTab.getAttribute('aria-selected'), 'false');
   assert.equal(eventsTab.getAttribute('aria-selected'), 'true');
   assert.equal(updatesTab.disabled, true);
   assert.equal(eventsTab.disabled, false);
});
