(function () {
  'use strict';

  angular
    .module('crowdresearch.user_management.controllers')
      .controller('RegisterController', RegisterController)
      .controller('LoginController', LoginController)
      .controller('ProfileController', ProfileController)
      .controller('ForgotPasswordController', ForgotPasswordController)
      .controller('ResetPasswordController', ResetPasswordController);

    RegisterController.$inject = ['$location', '$scope', 'UserManagement'];
    LoginController.$inject = ['$location', '$scope', 'UserManagement'];
    ProfileController.$inject = ['$location', '$scope', 'UserManagement'];
    ForgotPasswordController.$inject = ['$location', '$scope', 'UserManagement'];
    ResetPasswordController.$inject = ['$location', '$scope', 'UserManagement'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, UserManagement) {
    var vm = this;

    vm.register = register;


    function register() {
      UserManagement.register(vm);
    }
  }


    function LoginController($location, $scope, UserManagement) {
    var vm = this;

    vm.login = login;


    function login() {
      UserManagement.Login(vm.username, vm.password);
    }
  }


    function ProfileController($location, $scope, UserManagement) {
    var vm = this;

    vm.profile = profile;


    function profile() {
      UserManagement.profile(vm.userId);
    }
  }

    function ForgotPasswordController($location, $scope, UserManagement) {
    var vm = this;

    vm.profile = forgot_password;


    function forgot_password() {
      UserManagement.forgot_password(vm.email);
    }
  }


    function ResetPasswordController($location, $scope, UserManagement) {
    var vm = this;

    vm.profile = reset_password;


    function reset_password() {
      UserManagement.reset_password(vm.email);
    }
  }

})();