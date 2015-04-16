/**
 * Created by dmorina on 16/04/15.
 */
(function () {
      'use strict';

      angular
        .module('thinkster.routes')
        .config(config);

      config.$inject = ['$routeProvider'];

      /**
      * @name config
      * @desc Define valid application routes
      */
      function config($routeProvider) {
        $routeProvider.when('/register', {
          controller: 'RegisterController',
          controllerAs: 'rc',
          templateUrl: '/templates/user_management/register.html'
        }).otherwise('/');
      }
})();