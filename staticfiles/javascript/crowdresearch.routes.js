/**
 * Created by dmorina on 16/04/15.
 */
(function () {
      'use strict';

      angular
        .module('crowdresearch.routes')
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
          templateUrl: '/templates/registration/register.html'
        }).when('/login', {
          controller: 'LoginController',
          controllerAs: 'lc',
          templateUrl: '/templates/login.html'
        }).otherwise('/');
      }
})();