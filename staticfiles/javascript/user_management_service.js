
(function () {
  'use strict';

  angular
    .module('crowdresearch.user_management.services')
    .factory('User Management', UserManagement);

  UserManagement.$inject = ['$cookies', '$http'];

  /**
  * @namespace UserManagement
  * @returns {Factory}
  */
  function UserManagement($cookies, $http) {
    /**
    * @name UserManagement
    * @desc The Factory to be returned
    */
    var UserManagement = {
        register: register,
        login: login,
        profile: profile,
        forgot_password: forgot_password,
        reset_password: reset_password,
        account_activation: account_acctivation
    };

    return UserManagement;

    ////////////////////

        function login(username, password){
            return $http.post('/api/user_management/login', {
                username: username,
                password: password
            });
        }
        function register(newUser) {
            return $http.post('/api/v1/accounts/', {
                user: newUser
            });
        }

        function profile(userId){
          return $http.get('/api/user_management/profile', {
              userId: userId
          });
        }

      function forgot_password(email){
          return $http('/api/user_management/forgot_password', {
              email: email
          });
      }

      function reset_password(email){
          return $http('/api/user_management/reset_password', {
              email: email
          });
      }
  }
})();