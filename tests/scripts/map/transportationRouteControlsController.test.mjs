import assert from 'node:assert/strict';
import test from 'node:test';

import { MapClient } from '../../../scripts/api/mapClient.js';
import { TransportationRouteControlsController } from '../../../scripts/map/transportationRouteControlsController.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_RenderTransportationRouteControls_TestRoutes_ExpectRadios', () => {
   const container = createDomNode('div');
   const transportation = 'Zoomobile';
   const summer = 'summer';
   const winter = 'winter';

   TransportationRouteControlsController.renderTransportationRouteControls(container, [
      {
         name: transportation,
         routes: [summer, winter],
      },
   ]);
   const section = container.children.at(Position.FIRST);
   const title = section.children.at(Position.FIRST);
   const options = section.children.at(Position.SECOND);
   const values = options.children.map((option) => option.children.at(Position.FIRST).value);
   const labels = options.children.map((option) => option.children.at(Position.SECOND).textContent);
   const names = options.children.map((option) => option.children.at(Position.FIRST).name);

   assert.equal(container.children.length, Position.SECOND);
   assert.equal(section.className, 'transportation-route');
   assert.equal(section.dataset.transportation, transportation);
   assert.equal(title.className, 'transportation-route-title');
   assert.equal(title.textContent, Strings.map.transportationRoute.title(transportation));
   assert.equal(options.className, 'transportation-route-options');
   assert.equal(options.children.length, 4);
   assert.deepEqual(values, ['none', 'current', summer, winter]);
   assert.deepEqual(names, [
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
      'transportationRoute-zoomobile',
   ]);
   assert.equal(options.children.at(Position.FIRST).children.at(Position.FIRST).checked, true);
   assert.deepEqual(labels, [
      Strings.map.transportationRoute.none,
      Strings.map.transportationRoute.current,
      Strings.map.transportationRoute.route(summer),
      Strings.map.transportationRoute.route(winter),
   ]);
});


test('Test_RenderTransportationRouteControls_TestMissingContainer_ExpectNoOp', () => {
   const render = () => {
      TransportationRouteControlsController.renderTransportationRouteControls(null, [
         { name: 'Zoomobile', routes: ['summer'] },
      ]);
   };

   assert.doesNotThrow(render);
});


test('Test_InitTransportationRouteControls_TestRoutes_ExpectRenderedAndReturned', async () => {
   const originalGet = MapClient.getTransportationRoutes;
   const container = createDomNode('div');
   const transportation = 'Zoomobile';
   const routes = [{ name: transportation, routes: ['summer'] }];
   MapClient.getTransportationRoutes = async () => routes;

   try {
      const result = await TransportationRouteControlsController.initTransportationRouteControls(
         container,
      );

      assert.equal(result, routes);
      assert.equal(container.children.length, Position.SECOND);
      assert.equal(container.children.at(Position.FIRST).dataset.transportation, transportation);
   } finally {
      MapClient.getTransportationRoutes = originalGet;
   }
});
