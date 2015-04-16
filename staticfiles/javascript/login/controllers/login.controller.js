/**
 * Created by dmorina on 16/04/15.
 */
(function () {
  'use strict';

  angular
    .module('crowdresearch.login.controllers')
      .controller('LoginController', LoginController)
    LoginController.$inject = ['$location', '$scope', 'UserManagement'];


    function LoginController($location, $scope, UserManagement) {
    var vm = this;

    vm.login = login;


    function login() {
      UserManagement.Login(vm.username, vm.password);
    }
  }

})();