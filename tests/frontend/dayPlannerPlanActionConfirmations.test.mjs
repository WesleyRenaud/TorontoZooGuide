import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   showRebuildScheduleConfirmation,
} from '../../scripts/itinerary/panel/dayPlannerPlanActionConfirmations.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from './helpers/confirmPopupTestSetup.mjs';

test.describe('dayPlannerPlanActionConfirmations', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('showRebuildScheduleConfirmation mounts to the day planner view', () => {
      const dayPlannerView = createDomNode('div', 'itin-panel-day-planner-view');
      document.body.appendChild(dayPlannerView);

      showRebuildScheduleConfirmation({
         mountEl: dayPlannerView,
      });

      assert.ok(dayPlannerView.querySelector('.tzg-confirm'));
      assert.equal(document.querySelectorAll('.tzg-confirm').length, 1);
   });
});
