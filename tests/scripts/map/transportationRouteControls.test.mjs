import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteControls } from '../../../scripts/map/transportationRouteControls.js';
import { APP_STRINGS } from '../../../scripts/strings.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RenderTransportationRouteControls_TestRoutes_ExpectRadios', () => {
   const container = createDomNode('div');

   TransportationRouteControls.renderTransportationRouteControls(container, [
      {
         name: 'Zoomobile',
         routes: ['summer', 'winter'],
      },
   ]);

   assert.equal(container.children.length, 1);

   const section = container.children[0];
   assert.equal(section.className, 'transportation-route');
   assert.equal(section.dataset.transportation, 'Zoomobile');

   const [title, options] = section.children;
   assert.equal(title.className, 'transportation-route-title');
   assert.equal(
      title.textContent,
      APP_STRINGS.map.transportationRoute.title('Zoomobile'),
   );
   assert.equal(options.className, 'transportation-route-options');
   assert.equal(options.children.length, 4);

   const values = options.children.map((option) => option.children[0].value);
   const labels = options.children.map((option) => option.children[1].textContent);
   const names = options.children.map((option) => option.children[0].name);

   assert.deepEqual(values, ['none', 'current', 'summer', 'winter']);
   assert.deepEqual(names, [
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
   ]);
   assert.equal(options.children[0].children[0].checked, true);
   assert.deepEqual(labels, [
      APP_STRINGS.map.transportationRoute.none,
      APP_STRINGS.map.transportationRoute.current,
      APP_STRINGS.map.transportationRoute.route('summer'),
      APP_STRINGS.map.transportationRoute.route('winter'),
   ]);
});
