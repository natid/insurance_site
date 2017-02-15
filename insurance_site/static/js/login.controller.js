(function () {
    'use strict';

    angular
        .module('insurance_crm.demo')
        .controller('LoginController',
            ['$scope', '$location', 'Login', LoginController])

    function LoginController($scope, $location, Login) {
        $scope.login = function() {
            Login.login($scope.user)
                .then(function () {
                    $location.url('/');
                },
                function () {
                    $scope.login_error="Invalid username/password combination";
                });
        }

        $scope.signup = function() {
            Login.signup($scope.user)
                .then(function () {
                    $scope.login = "true";
                    $scope.login_after_signup = "User created successfully! You are ready to login.";
                },
                function (err) {
                    if (err.status === 409 ) {
                        $scope.login_error="User already exists";
                    }
                });
        }

        if (Login.isLoggedIn()) {
            $location.url('/');
        }

    }
})();