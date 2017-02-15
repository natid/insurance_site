(function () {
    'use strict';

     angular
        .module('insurance_crm.demo')
        .service('Login', ['$http', '$location', Login]);

     function Login($http, $location) {
        this.login = login;
        this.isLoggedIn = isLoggedIn;
        this.logout = logout;
        this.redirectIfNotLoggedIn = redirectIfNotLoggedIn;
        this.signup = signup;

        function login(credentials) {
            return $http.post('/auth_api/login/', credentials)
                .then (function (response) {
                   localStorage.currentUser = JSON.stringify(response.data);
                });
        }

        function signup(userData) {
            return $http.post('/auth_api/signup/', userData);
        }

        function isLoggedIn () {
            return !!localStorage.currentUser;
        }

        function logout () {
            delete localStorage.currentUser;
            $http.get('/auth_api/logout/').then(function() {
                $location.url('/login');
            });
        }

        function redirectIfNotLoggedIn () {
            if (!isLoggedIn()) {
                $location.url('/login');
            }
        }
     }
})();