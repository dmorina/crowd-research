/**
 * Created by dmorina on 16/04/15.
 */
(function () {
  'use strict';

  angular
    .module('crowdresearch.config')
    .config(config);

  config.$inject = ['$locationProvider'];

  /**
  * @name config
  * @desc Enable HTML5 routing
  */
  function config($locationProvider) {
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
  }
})();