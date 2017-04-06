(function ()
{
    'use strict';

    angular
        .module('fuse')
        .service('AuthenticationService', AuthenticationService);
    //for production
    // var baseURL = 'https://poly-wizz.co.il';
   var baseURL = ''; // local with build
    // var baseURL = 'http://localhost:8000' // local with serve
    /** @ngInject */

    function AuthenticationService($http, $cookies, $rootScope, $timeout, $q) {
        var service = {};
 
        service.Login = Login;
        service.SetCredentials = SetCredentials;
        service.ClearCredentials = ClearCredentials;
 
        return service;
 
        function Login(username, password) {
 
            var d = $q.defer();
            $http.post('/auth_api/login/', { username: username, password: password })
                .then(function(response) {
                    d.resolve(response);
                }, function(response) {
                    d.reject(response);
                });
            return d.promise;
        }
 
        function SetCredentials(username, password) {
            var authdata = btoa(username + ':' + password);
 
            $rootScope.globals = {
                currentUser: {
                    username: username,
                    authdata: authdata
                }
            };
 
            // set default auth header for http requests
            $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata;
 
            // store user details in globals cookie that keeps user logged in for 1 week (or until they logout)
            var cookieExp = new Date();
            cookieExp.setDate(cookieExp.getDate() + 7);
            $cookies.putObject('globals', $rootScope.globals, { expires: cookieExp });
        }
 
        function ClearCredentials() {
            $rootScope.globals = {};
            $cookies.remove('globals');
            $http.defaults.headers.common.Authorization = 'Basic';
        }
    }


})();
